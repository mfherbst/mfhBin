#!/bin/bash

detect_gpg_agent() {
	# Tries to find a running gpg-agent instance
	# if found it returns 0 and sets the variables
	# GPG_AGENT_INFO, else it returns 1

	for BASE in /run/user/$UID; do
		if [ -S "$BASE/gnupg/S.gpg-agent" ]; then
			GPG_AGENT_INFO="$BASE/gnupg/S.gpg-agent:0:1"
			echo "Found gpg-agent in socket $GPG_AGENT_INFO"
			return 0
		fi
	done
	return 1
}

detect_ssh_agent() {
	# Tries to find a running ssh-agent instance
	# if that turns out to work, it returns 0 and
	# sets the variables SSH_AGENT_PID and SSH_AUTH_SOCK
	# else returns 1

	local PIDS
	if ! PIDS=$(pgrep -U $USER ssh-agent); then
		# found no ssh agent
		return 1
	fi

	local AUTH_SOCK folder pid ppid
	for folder in /tmp/ssh-*; do
		[ ! -d "$folder" ] && continue

		for pid in $PIDS; do
			# find parent pid:
			ppid=$(ps --pid $pid o ppid,pid | awk "/$pid\$/ { print \$1 }")
			
			if [ -S "$folder/agent.$ppid" ]; then
				echo "Found ssh-agent running on $pid"
				SSH_AGENT_PID=$pid
				SSH_AUTH_SOCK="$folder/agent.$ppid"
				return 0
			fi
		done
	done
	return 1
}

echo_finding() {
	# Echo the current value of $1 if that var exists
	# $1: varname
	[ -v "$1" ] && echo "    ${1}=${!1}"
}

echo_findings() {
	echo_finding "SSH_AGENT_PID"
	echo_finding "SSH_AUTH_SOCK"
	echo_finding "GPG_AGENT_INFO"
}

export_finding() {
	# Exports the current value of $1 if that var exists
	# $1: varname
	[ -v "$1" ] && export ${1}="${!1}"
}

export_findings() {
	export_finding "SSH_AGENT_PID"
	export_finding "SSH_AUTH_SOCK"
	export_finding "GPG_AGENT_INFO"
}

usage() {
	cat <<- EOF
	./detect_agents.sh [ -h ]

	Try to detect a running ssh-agent instance and set bash 
	environment variables such that ssh instances can make
	use of it.

	If executed, just prints the required settings, if
	sourced it actually sets the environment appropriately.
	EOF
}

#--------------------------------------------------------

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
	usage
	return 0 &> /dev/null || exit 0
fi


# Accumulate if we found something
FOUND_SOMETHING=n

# Search for agents
detect_ssh_agent && FOUND_SOMETHING=y
detect_gpg_agent && FOUND_SOMETHING=y

# Export what we found:
export_findings

# Exit if we got sourced
[ "$FOUND_SOMETHING" == "y" ]
return $? &> /dev/null

# If we are still here, we got executed:
if [ "$FOUND_SOMETHING" == "y" ]; then
	echo
	echo "Source the script in order to add the following variables"
	echo "to your environment."
	echo_findings
	exit 0
else
	echo "Could not detect any environment"
	exit 1
fi
exit 0
