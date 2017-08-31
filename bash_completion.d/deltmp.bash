_deltmp() {
	local cur prefix comp_classes I lastarg
	# the current word to be completed:
	cur=${COMP_WORDS[COMP_CWORD]}

	# The current completion reply
	COMPREPLY=()

	compclasses="n"
	# check if the completion is to complete classes
	# or to complete arguments

	if [ "$COMP_CWORD" -gt "1" ]; then
		for ((I=COMP_CWORD-1;I>=0;--I)); do
			lastarg="${COMP_WORDS[$I]}"
			if [[ "$lastarg" == "--exclude" \
				|| "$lastarg" == "--only" \
				|| "$lastarg" == "--include" \
				|| "$lastarg" == "-o" \
				|| "$lastarg" == "-e" \
				|| "$lastarg" == "-i" ]]; then
				compclasses="y"
				break
			fi
		done
	fi

	if [ "$compclasses" == "y" ]; then
		[ "$cur" == ":" ] && cur=""

		COMPREPLY=( $( compgen -W 'cobj mac orca nohup swp backup win pyobj' -- "$cur" ) )
		return 0
	else
		COMPREPLY=( $( compgen -o plusdirs -W '-h --help -r --recursive --force -f --only -o --exclude -e --include -i --list -l' -- "$cur" ) )
		return 0
	fi
	return 0
}

complete -F _deltmp deltmp
