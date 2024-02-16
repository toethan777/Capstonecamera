# Essential things

## Commands

### cd 
This is primary way you navigate through Linux folder directories.

By default, you will be in the root directory, also known as `~`. The root directory is where most of your things are (e.g. Pictures, Downloads, Documents, etc.). If you want to navigate to Downloads, type `cd Downloads` or the full path `cd ~/Downloads`. If you want to go back a directory, type `cd ..`. I sometimes get crazy with it, and do a command like `cd ../Pictures` fron the directory Downloads, but you can navigate one folder at a time.

Another thing to note is that the terminal always displays what directory you are in currently, but if you get lost, type `cd ~`!

### ls 
This command lists items in your current directory. It is helpful for finding all the folders and files you need. `ls -l` can display other attributes of files and folders

### cp
The copy command. Used for copying files and folders. This is usually formatted as `cp [file location] [file destination]`.

### mv
The move command. Used for moving files and folders. This is usually formatted as `mv [file location] [file destination]`.

### rm
The delete command. Used for deleting files and folders. Kinda dangerous. Especially `rm -rf [file location]`, also known as the recursive delete. DO NOT TYPE `rm -rf ~`, this will remove literally everything. We only have one server. Contact me if you do this.

### touch
Create a blank file.

### nano
Cool little file editor.

### man
Manual pages for specific Linux commands. For example, `man neofetch` will give you the manual for the Linux command for neofetch. This is important if you want to learn more about certain commands and operations. All the above commands have man pages; research them if you want!


## Cool Macros

`ctrl+l` -> clears terminal space, but does not remove the history of previous commands. I recommend this over the `clear` command.

`tab` -> command autocomplete. Usually if you are lazy like me. Say you are typing `cd ~/Downl`, you can press `tab`, and it autocompletes.

`ctrl+shift+c` -> terminal copy

`ctrl+shift+p` -> terminal paste
