import sys
import json
import subprocess

def shell_command(command):
    '''
    Executes command as shell prompt, returns response
    '''
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    jsonOutput = json.loads(output)
    return jsonOutput


def select_cf_app():
    
    output = shell_command('cf curl /v2/apps')
    
    if len(output['resources']) > 1 :
        print('\n')
        print('Available Cloud Foundry Apps \n')
        for i in range(len(output['resources'])):
            print('\t' + str(i+1) + ': ' + output['resources'][i]['entity']['name'])
        selectedApp = int(input('\nPlease select an application to configure: ')) - 1
        print('\n')
    
    else :
        selectedApp = 0
    
    selectedAppName = output['resources'][selectedApp]['entity']['name']
    selectedAppGUID = output['resources'][selectedApp]['metadata']['guid']
    
    return selectedAppName, selectedAppGUID


def get_db_credentials():
    
    appName, appGUID = select_cf_app()
    
    appEnvVar = shell_command('cf curl /v2/apps/' + appGUID + '/env')
    
    try:
        dbCreds = appEnvVar['system_env_json']['VCAP_SERVICES']['aws-rds'][0]['credentials']
    except KeyError:
        print('-- ERROR: No aws-rds service associated with application')
        print('-- ERROR: Exiting')
        sys.exit(0)

    host = dbCreds['host']
    username = dbCreds['username']
    password = dbCreds['password']
    db_name = dbCreds['db_name']

    return appName, dbCreds

    
def setup_ssh_tunnel():
    
    appName, dbCreds = get_db_credentials()
    
    host = dbCreds['host']
    
    username = dbCreds['username']
    password = dbCreds['password']
    database = dbCreds['db_name']
    
    db_connection = "export PGPASSWORD='{}'; psql -U {} -h 0 -p 63306 -d {}".format(
        password,
        username,
        database
        )
    
    print('''
AWS-RDS service account identified
SSH Tunnel established on port 63303

Copy and paste the string below in another terminal window to launch psql

    {}

Press ctrl + c to close tunnel
    '''.format(db_connection))

    shell_command('cf ssh -N -L 63306:' + host + ':5432 ' + appName)


def set_cf_environment_variables_as_local_variables():
    
    pass 
    #applicationDetails = shell_command('cf curl /v2/apps/' + selectedAppGUID + '/env')
    

if __name__ == '__main__':
    try:
        setup_ssh_tunnel()
    except KeyboardInterrupt:
        sys.exit()
