# mfhBin
Helpful scripts for everyday work

## Setup
* Checkout the repo to a place you like.
* Source the file ``setPATH.sh`` from your ``~/.bashrc``, ``~/.profile`` or similar in order to have the scripts available in the shell.
* Source the file ``enable.bash_completion`` from the ``~/.bash_completion`` in order to enable tab completion for the scripts in this repository.

## Short description of contained scripts
### random_int.sh
Produces a random integer between 0 and the first argument

### delTmp
Delete temporary files. Commandline arguments allow to specify precisely what types of files are deleted (Windows, Mac, Programming, swp, ...)

### mountSSHFS
Convenience script around ``sshfhs`` and ``fusermount``. Mounts and unmounts a set of predefined remote locations with predefined parameters.
Also parses the user's ssh config file (usually ~/.ssh/config) and makes the Hosts configured there available for mounting with the predefined
parameters for ``sshfs``. Of cause the behaviour and the parameters can be configured.

### mvx
Swap the content of two files. 

### pdfcompress
Compress the file size of a ``pdf`` file. Works by the trick of converting ``pdf`` -> ``ps`` -> ``pdf``, which perhaps surprising reduces the file size quite drastically.
