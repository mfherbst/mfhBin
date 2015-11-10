_delTmp() {
	local cur prev prefix
	# the current word to be completed:
	cur=${COMP_WORDS[COMP_CWORD]}
	prev=${COMP_WORDS[$((COMP_CWORD-1))]}

	COMPREPLY=()

	if [[ "$prev" == "--exclude" || "$prev" == "--only" ]]; then
		#TODO this part does not yet work properly
		prefix=${cur%:*}
		[ "$prefix" ] && prefix="$prefix:"

		cur=${cur##*:}
		COMPREPLY=( $( compgen -P "$prefix" -W 'comp mac nohup swp tilde win' -- "$cur" ) )
		return 0
	fi

	if [[ "$cur" == -* ]]; then
		COMPREPLY=( $( compgen -o plusdirs -W '-h --help -r --recursive --force -f -y --yes --dry-run -n --simulate, -s --only --exclude --list -l' -- "$cur" ) )
		return 0
	fi
}

#complete -o plusdirs -F _delTmp delTmp
complete -F _delTmp delTmp
