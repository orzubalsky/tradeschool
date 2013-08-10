#!/bin/bash

# Create ftp user, create folders and set permissions
# Usage: ./create_ftp_user.sh [username] "[password]"
#

NAME=$1
PASS=$2

echo "USAGE: create_ftp_user.sh [username] [password]"

# check input parameters
if [ -z "$NAME" ]; then
    echo "Error: username is not set"
    exit
fi

if [ -z "$PASS" ]; then
    echo "Error: password not set"
    exit
fi

# create system user
echo "Creating user: $NAME"
echo "With password: $PASS"

adduser -p `openssl passwd -1 $PASS` $NAME

# save to users log
echo "user: $NAME, pass: $PASS" >> new_ftp_users_list

# add user to ftp daemon list
echo "$NAME" >> /etc/vsftpd/chroot_list

# create user ftp dir
mkdir -p /home/$NAME/public_html

# Set Ownership
chown root:root /home/$NAME
chown -R $NAME:root /home/$NAME/public_html

# Set permissions
chmod -R 0777 /home/$NAME/public_html

# mount the branch html dir
mount --bind /opt/projects/tse/ts/apps/branches/$NAME /home/$NAME/public_html
echo "/opt/projects/tse/ts/apps/branches/$NAME /home/$NAME/public_html none bind 0 0" >> /etc/fstab

# restart vsftp daemon
service vsftpd restart
#/etc/init.d/vsftpd restart