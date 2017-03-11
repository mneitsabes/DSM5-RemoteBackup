#!/bin/sh

### Configuration
# Current path to the location of this script
CURR_PATH=/volume1/@appstore/remotebackup

# Path and prefix of logfiles : YYYY-MM-DD-HH-MM-SS
#  -> files logfile : YYYY-MM-DD-HH-MM-SS.files.log.gz
#  -> info logfile : YYYY-MM-DD-HH-MM-SS.info
PREFIX_LOGFILE=$CURR_PATH"/logs/"$(date +"%Y-%m-%d-%H-%M-%S")
LOGFILE_FILES=$PREFIX_LOGFILE.files.log
LOGFILE_INFO=$PREFIX_LOGFILE.info

### Backup
# Capture all output of commands above to the logfile
exec > $LOGFILE_FILES 2>&1

# Start time
BACKUPBEGIN=`date +"%d/%m/%Y %H:%M:%S"`
echo "--- REMOTE BACKUP BEGINS AT $BACKUPBEGIN ---"

# Start the backup
# A patched rsync version is used to add the support of the "--detect-renamed" argument.
# rsync-patched-cli is the same binary that rsync-patched-srv but the last one is owned by root and have a +s on it (to update files)
#   $CURR_PATH/rsync-patched-cli : execute the patched version of rsync
#   -a : archive mode (see man of rsync)
#   -v : verbose
#   -h : human readable
#   --deleter-after : delete files and directories which aren't on the source anymore
#   --detect-renamed : check if files or directories aren't renamed or moved. If it is, the file is just copied or moved directly on the server without re-upload
#   -e "ssh p ..." : use a customized port for SSH
#   --password-file=... : specify the file that contains the password for the remote rsync directory
#   --include-from=... : specify a text file which contains directories wich must be backuped
#   --excluse="*" : backup only what is specified on the --include-from file
#   /volume1/ : from the root of the volume1
#    Seb@remote.server.tld::BackupSeb/ : user "seb" on the SSH server which listen on the "remote.server.tld" host. The remote rsync direcotyr is named "BackupSeb"
$CURR_PATH/bin/rsync-patched-cli -a -v -h --delete-after --detect-renamed --rsync-path=$CURR_PATH/bin/rsync-patched-srv -e "ssh -p 20222" --password-file=$CURR_PATH/etc/rsync.passwd --include-from=$CURR_PATH/etc/rsync.includes --exclude="*" /volume1/ Seb@remote.server.tld:BackupSeb/

# Retrieve the result code
RC=$?

# Default message
MSG="RemoteBackup has been successfully executed"

# If the result code is not 0, a error occured
if [[ $RC != 0 ]] ; then
    MSG="Backup has failed, the return code of rsync is $RC"
fi
    
# Print the message
echo $MSG
    
# End time
BACKUPEND=`date +"%d/%m/%Y %H:%M:%S"`
    
echo "--- REMOTE BACKUP ENDS AT $BACKUPEND ---"
    
# Retrieve data from rsync's ouput if no error occured
TRANSFERT_DATA_SENT=0
TRANSFERT_DATA_RECEIVED=0
TRANSFERT_SPEED=0
TRANSFERT_NB_FILES_IMPACTED=0
REMOTE_BACKUP_SIZE=0
    
if [[ $RC == 0 ]] ; then
    # Output example : "sent 15.55M bytes  received 11 bytes  203.32K bytes/sec"
    # Regex "sent \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+received \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+\\([0-9]\+\.\?[0-9]*[KMG]\?\) bytes/sec"
    #    --> \([0-9]\+\.\?[0-9]*[KMG]\?\) :
    #       - [0-9]+ : the part before the dot
    #       - .?     : the dot if exists
    #       - [0-9]* : the decimal part if exists
    #       - [KMG]? : the letter for "KB", "MB" or "GB" if exists
    #
    # tail is use to speed up the access to these informations
    TMP_LINE_VALUES=`tail $LOGFILE_FILES | grep '^sent'`
    TRANSFERT_DATA_SENT=`echo $TMP_LINE_VALUES | sed -e "s|sent \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+received \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+\\([0-9]\+\.\?[0-9]*[KMG]\?\) bytes/sec|\1|"`
    TRANSFERT_DATA_RECEIVED=`echo $TMP_LINE_VALUES | sed -e "s|sent \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+received \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+\\([0-9]\+\.\?[0-9]*[KMG]\?\) bytes/sec|\2|"`
    TRANSFERT_SPEED=`echo $TMP_LINE_VALUES | sed -e "s|sent \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+received \([0-9]\+\.\?[0-9]*[KMG]\?\) bytes\s\+\\([0-9]\+\.\?[0-9]*[KMG]\?\) bytes/sec|\3|"`
                                            
    REMOTE_BACKUP_SIZE=`tail $LOGFILE_FILES | grep '^total size' | sed -e "s|total size is \([0-9]\+\.\?[0-9]*[KMG]\?\).*|\1|"`
                                    
    TRANSFERT_NB_FILES_IMPACTED=$((`wc -l $LOGFILE_FILES | sed -e "s|^\([0-9]\+\).*|\1|"` - 7))
fi
                                                                
# Compress files log
gzip $LOGFILE_FILES
                                                                
### Generate the info log file with
echo "BEGIN=$BACKUPBEGIN" > $LOGFILE_INFO
echo "END=$BACKUPEND" >> $LOGFILE_INFO
echo "RC=$RC" >> $LOGFILE_INFO
echo "TRANSFERT_DATA_SENT=$TRANSFERT_DATA_SENT" >> $LOGFILE_INFO
echo "TRANSFERT_DATA_RECEIVED=$TRANSFERT_DATA_RECEIVED" >> $LOGFILE_INFO
echo "TRANSFERT_SPEED=$TRANSFERT_SPEED" >> $LOGFILE_INFO
echo "TRANSFERT_NB_FILES_IMPACTED=$TRANSFERT_NB_FILES_IMPACTED" >> $LOGFILE_INFO
echo "REMOTE_BACKUP_SIZE=$REMOTE_BACKUP_SIZE" >> $LOGFILE_INFO
                                                            
# Link to latest backup logfiles
rm $CURR_PATH/logs/latest.files 2> /dev/null
rm $CURR_PATH/logs/latest.info 2> /dev/null

ln -s $LOGFILE_FILES.gz $CURR_PATH/logs/latest.files
ln -s $LOGFILE_INFO $CURR_PATH/logs/latest.info                                                                
