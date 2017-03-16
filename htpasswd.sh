#!/bin/bash

if [ "$1" == "-h" ]; then
	echo "Script to generate hashes for htpasswd files."
	exit 0
fi

read -r -p "Input user name: " USER
read -r -s -p "Input password:  " PASSWORD
echo
read -r -s -p "Repeat password: " PASSWORD2
echo

if [ "$PASSWORD" != "$PASSWORD2" ]; then
	echo "Passwords do not agree" >&2
	exit 1
fi


SALT="$(openssl rand -base64 3)";
SHA1=$(echo -n "$PASSWORD$SALT" | openssl dgst -binary -sha1 | sed 's#$#'"$SALT"'#' | base64)
echo "$USER:{SSHA}$SHA1"
