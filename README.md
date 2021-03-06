# mfhBin
Helpful scripts for everyday work

## Setup
* Checkout the repo to a place you like.
* Source the file ``setPATH.sh`` from your ``~/.bashrc``, ``~/.profile`` or similar in order to have the scripts available in the shell.
* Source the file ``enable.bash_completion`` from the ``~/.bash_completion`` in order to enable tab completion for the scripts in this repository.

## Short description of contained scripts
### cd2iso
Copy an iso9660 CD to an iso file on disk verifying the process with a checksum.

### deltmp
Find and delete temporary files. Commandline arguments allow to specify precisely what types of files are deleted (Windows, Mac, Programming, swp, ...) and wheather to ask before deleting anything or not.

### detect_agents.sh
Detect running ``ssh-agent`` instances and determine the appropriate environment variables such that ``ssh`` and other programs can make use of ``ssh-agent``.
Helpful if you want to connect to your agent from inside a ``screen`` session.
Just source the script from inside your ``screen`` session and be happy that you don't have to type your password.

### down_frab_videos.py
Now managed in [github.com/mfherbst/down-frab-videos](https://github.com/mfherbst/down-frab-videos).

### in_blocking_terminal.sh
Script to hack away the non-blocking feature of some terminals. 
Since a while ago ``gnome-terminal`` does not allow to start a terminal as a new process and keep blocking the current process until execution oth this ``gnome-terminal`` process is done.
The ``--disable-factory`` which used to exist for this pupose is not valid any more.
This script tries to re-implement the feature to some extent. 
Similar to ``i3-sensible-terminal`` and ``open_shell_at.sh`` I try to guess a terminal on the current system and execute the remaining commandline within it. I then use ``pgrep`` to check for the full commandline and keep ``sleep``ing until it cannot be found in the table of running processes any more.
**This is by no means save** and has tons of possible **race conditions**, but it works fine for cases where a file should be edited in a new terminal or similar. The author uses it with the ``termvim`` script below in order to allow ``vim`` in ``gnome-terminal`` to be used as an external editor from ``icedove``/``thunderbird``.
If anyone knows a better mechanism to achive this functionality apart from use a different terminal (I really like ``gnome-terminal``, actually) I would be happy to know.

### mountsshfs
Convenience script around ``sshfhs`` and ``fusermount``. Mounts and unmounts a set of predefined remote locations with predefined parameters.
Also parses the user's ssh config file (usually ``~/.ssh/config``) and makes the Hosts configured there available for mounting with the predefined
parameters for ``sshfs``. Of cause the behaviour and the parameters can be configured.

### mvx
Swap the content of two files. 

### open_shell_at.sh
Open a terminal at a specified working directory. 
Wrapper to substitute file managers like ``nautilus`` or ``thunar`` from graphical programs.
Currently the author uses it for udiskie.
Tries a couple of terminals to select a well-suited one, so does not assume a speciffic terminal emulator to be installed.

### pdfcompress
Compress the file size of a ``pdf`` file. Works by the trick of converting ``pdf`` -> ``ps`` -> ``pdf``, which surprisingly reduces the file size quite drastically.

### random_int.sh
Produces a random integer between 0 and the first argument

### random_mac.sh
Produces a random mac address

### termvim
Open the arguments in ``vim`` in a new, blocking terminal.

### this_path_on
Open the current working directory on a remote machine via ssh

### vimwhich
Script to open the executable/script corresponding to a command in an editor (by default ``vim``). 
I.e. it looks up the full path of the command using ``which`` and then opens the result. 
The precise editor used is determined by the content of the ``EDITOR`` variable.
By default ``vim`` is used.

