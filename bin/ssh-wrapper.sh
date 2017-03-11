#!/bin/sh

# Source: http://www.wallix.org/2011/10/18/restricting-remote-commands-over-ssh/

# This SSH wrapper is executed when specific client open a remote SSH connection.
# The user can only execute commands that are allowed.
# By default, no shell can be executed

set $SSH_ORIGINAL_COMMAND

# $1 is the executed command  
case "$1" in
     "/volume1/@appstore/remotebackup/bin/rsync-patched-srv")  # Accept the execution of rsync-patched-srv
     ;;
     
     *) # Deny all other command (and log)
         logger -s -t restricted-command -- "Invalid command $@"
         exit 1
     ;;
esac
                            
# Execute and log the command
logger -t restricted-command -- "Executing $@"
exec "$@"
