#!/bin/sh
# Intended for running on the EC2 instance hosting the Django application.
#
# Installation:
# 1. Put this script into the home folder (/home/ec2-user/bin/musync.sh)
# 2.a Run from a connected terminal to the instance
# 2.b Run directly from your environment that has been initialized as
#     your ElasticBeanstalk environment,
#
#     eb ssh --command /home/ec2-user/bin/musync.sh

# Activate the virtual environment of the django application
source /opt/python/run/venv/bin/activate

# Set the environment variables for the application
source /opt/python/current/env

# Run our django command to process unpublished assets
python /opt/python/current/app/manage.py dbupdate

# If there are no unpublished assets dbupdate does nothing
