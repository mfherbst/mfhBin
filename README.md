# mfhBin
Helpful scripts for everyday work

## Setup
* Checkout the repo to a place you like.
* Source the file ``setPATH.sh`` from your ``~/.bashrc``, ``~/.profile`` or similar in order to have the scripts available in the shell.
* Source the file ``enable.bash_completion`` from the ``~/.bash_completion`` in order to enable tab completion for the scripts in this repository.

## Short description of contained scripts
### delTmp
Find and delete temporary files. Commandline arguments allow to specify precisely what types of files are deleted (Windows, Mac, Programming, swp, ...)

### mountSSHFS
Convenience script around ``sshfhs`` and ``fusermount``. Mounts and unmounts a set of predefined remote locations with predefined parameters.
Also parses the user's ssh config file (usually ``~/.ssh/config``) and makes the Hosts configured there available for mounting with the predefined
parameters for ``sshfs``. Of cause the behaviour and the parameters can be configured.

### mvx
Swap the content of two files. 

### pdfcompress
Compress the file size of a ``pdf`` file. Works by the trick of converting ``pdf`` -> ``ps`` -> ``pdf``, which surprisingly reduces the file size quite drastically.

### random_int.sh
Produces a random integer between 0 and the first argument

### random_mac.sh
Produces a random mac address

### down_chaos_videos.py
Download videos or other media from CCC events (like the Chaos communication congress, MRMCD, Camp, ...)
By default the most recent chaos event is considered and high-quality ``webm`` files are downloaded.
This can, however, be changed using the flags ``--event`` and ``--format`` respectively. 
A list of configured events and available formats for a given event can be printed as well.

When downloading a talk the script will not only download the recording, but also some information from the Fahrplan as well.
This includes the attached files, the abstract and summary for the talk and the list of links and references.

In order to download talks, you just need to provide the script with a list of 4-digit talk ids. 
These should be listed line-by-line in a file, handed over to the script via ``--listfile``.
For example the file 
```
6258
# some crazy comment
6450
```
downloads the talks ``6258`` and ``6450``. 

The script can be configured for downloading other talks or media formats via a configuration file. 
If you want to personalise it, you should probably start by dumping the default configuration somewhere (use ``--config`` and ``--dump`` for this)

### open_shell_at.sh
Open a terminal at a specified working directory. 
Wrapper to substitute file managers like ``nautilus`` or ``thunar`` from graphical programs.
Currently the author uses it for udiskie.
Tries a couple of terminals to select a well-suited one, so does not assume a speciffic terminal emulator to be installed.

### vimwhich
Script to open the executable/script corresponding to a command in an editor (by default ``vim``). 
I.e. it looks up the full path of the command using ``which`` and then opens the result. 
The precise editor used is determined by the content of the ``EDITOR`` variable.
By default ``vim`` is used.
