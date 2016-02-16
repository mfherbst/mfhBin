#!/bin/sh
#
# execute a command blockingly inside a terminal
#
# BIG PHAT WARNING:
# This is script is really hackish and has loads of race conditions
# or situations where it may fail. It is only sensible and save to use
# when the called process is somehow blockingly access a resource, which 
# is mentioned on the commandline, like for example an editor editing a file.

# checkinterval controls how often we poll
# whether the process is still there
CHECKINTERVAL="0.5" # seconds

get_count() {
	# return the number of processes matching exactly this commandline
	pgrep -f -x -c "$*"
}

is_still_running() {
	# return 1 if the process is not running
	# return 0 if it is
	# return 2 if something else went wrong


	COUNT="$(get_count "$@")"

	if [ "$COUNT" -gt 1 ]; then
		# something is wrong a new process appeared ...
		echo "Something went wrong: The number of matching processes increased unexpectedly." >&2
		echo "Bailing out of blocking" >&2
		return 2
	fi

	# No process running:
	[ "$COUNT" -eq "0" ] && return 1

	# Case left: One is running
	return 0
}

open_in_terminal() {
	# try to find a sensible terminal and execute the command
	for terminal in $TERMINAL i3-sensible-terminal x-terminal-emulator urxvt rxvt terminator \
		Eterm aterm xterm gnome-terminal roxterm xfce4-terminal; do

		if which $terminal > /dev/null 2>&1; then
			# -e is understood by most terminal emulators afaik
			$terminal -e "$@"
			RES=$?
			break;
		fi
	done
	return $RES
}

# ----------------------------------------------------

# check that there are no processes like this running:
if [ "$(get_count "$@")" -gt 0 ]; then
	echo "There are already processes with commandline \"$@\" running." >&2
	echo "This script only works if there is exactly zero or one process" >&2
	echo "with this commandline the whole runtime of the system" >&2
	exit 1
fi

open_in_terminal "$@"
RES="$?"

# wait a while for things to settle
sleep 0.5

# check if process still there
if [ "$(get_count "$@")" -eq 0 ]; then
	# the terminal was probably blocking and the process
	# already ended, so we just exit
	exit "$?"
fi

# Some terminal like the gnome-terminal are not blocking, however.
# This is sh..., so try to fix it with this ugly workaround
while is_still_running "$@"; do
	sleep "$CHECKINTERVAL"
done
exit "$RES"
