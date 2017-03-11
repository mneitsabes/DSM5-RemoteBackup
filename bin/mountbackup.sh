#!/bin/sh

# Mount an encrypted Synology folder
# Usage: mountbackup.sh <path/to/encrypted/backup> <path/to/mount/point>"
# This script must be executed as root

# Show error message to the stderr
echoerr() {
    echo "$@" 1>&2;
}

# Usage (and exit)
usage () {
    echoerr "USAGE: mountbackup.sh <path/to/encrypted/backup> <path/to/mount/poi                                                                                                                                                             nt>"
    exit
}

# Check if the script is running as root
if [ "$(id -u)" != "0" ]; then
    echoerr "This script must be run as root"
    exit
fi

# Two arguments needed
if [ $# -ne 2 ]; then
    usage
fi

# The first argument must be a directory
if [ ! -d "$1" ]; then
    echoerr "The path backup is not a directory..."
    usage
fi

# The second argument must be a directory
if [ ! -d "$2" ]; then
    echoerr "The mount point is not a directory..."
    usage
fi

# Execute the mount.ecryptfs, this binary will only ask the password (in a secure way) and mount if it's correct
/usr/syno/sbin/mount.ecryptfs $1 $2 -o key:passphrase,ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_passthrough=no,ecryptfs_enable_filename_crypto=yes,no_sig_cache