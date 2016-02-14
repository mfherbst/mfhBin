#!/bin/sh
cd "$1"

call_if_exists() {
	if which $1 > /dev/null 2>&1; then
		$@
		exit $?
	fi
}

for term in $TERMINAL i3-sensible-terminal  urxvt rxvt terminator Eterm aterm xterm gnome-terminal roxterm xfce4-terminal; do
	call_if_exists $term
done
exit 1
