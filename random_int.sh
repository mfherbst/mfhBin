#!/bin/bash

random_int() {
	if [ -z "$1" ]; then
		echo "Please provide a number."	 >&2
		return 1
	fi
	if [[ "$1" == "-h" || "$1" == "--help" ]]; then
		echo "This function prints a random integer between 0 and \$1."	
		return 0
	fi

	local NUM=$1
	if (( NUM <= 32767 && NUM > 0 )); then
		echo $((RANDOM*(NUM+1)/32768))
		return 0
	else 
		echo "\$1 has to be between 0 and 32767" >&2
		return 1
	fi
}

return 0 &> /dev/null

random_int $@
