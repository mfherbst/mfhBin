#!/bin/bash
echo "htpasswd.sh is deprecated. Use htpasswd.py instead in the future." >&2
echo
read -p "Input user name: " USER
$(dirname $BASH_SOURCE)/htpasswd.py -n -m $USER
exit $?
