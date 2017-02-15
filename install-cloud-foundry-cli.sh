#!/bin/bash

# Download and install Cloud Foundry CLI
# Based on Cloud.gov documentation - https://docs.cloudfoundry.org/cf-cli/install-go-cli.html#linux

curl -L "https://cli.run.pivotal.io/stable?release=linux64-binary&source=github" | tar -zx
mv cf /usr/local/bin
rm LICENSE NOTICE
cf --version

exit