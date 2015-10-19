#!/bin/bash
#sets the PATH variable properly to make all scripts accessible.

#DIR where this file is saved:
_mfhBin_DIR=`dirname ${BASH_SOURCE[0]}`

PATH="$PATH:$_mfhBin_DIR"

unset _mfhBin_DIR
