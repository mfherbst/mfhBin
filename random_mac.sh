#!/bin/bash

random_mac() {
	# generate a random mac address
	dd if=/dev/random bs=6 count=1 2>/dev/null | hexdump  -e '/1 "%02x:"' | sed 's/:$/\n/'
}
return 0 &> /dev/null
random_mac
