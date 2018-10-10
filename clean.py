import subprocess
import sys
import re

cmds = "sed 's/\t/;/g' | cut -d ';' -f 2 | iconv -f utf8 -t ascii//TRANSLIT | sed -e 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/' | sort | uniq"

def split_pipes(arr):
     arrs = []
     temp = []
     pos = 0
     for pos in range(len(arr)):
         if arr[pos] != '|':
             temp.append(arr[pos])
         else:
             arrs.append(temp)
             temp = []
     return arrs

def separate_cmds(input, cmds_str):
    first = True
    cmds_str = cmds_str.replace("'", "")
    cmds_str = cmds_str.replace('"', "")

    # Faz split pelos espaços que não tenham uma \ antes
    cmds_sep = re.compile(r'(?<!\\) +').split(cmds_str)
    cmds = split_pipes(cmds_sep)
    pinit = subprocess.Popen(cmds[0], stdin=input, stdout=subprocess.PIPE)
    for cmd in cmds[1:]:
        if first:
            p = subprocess.Popen(cmd, stdin=pinit.stdout, stdout=subprocess.PIPE)
            first = False
        else:
            p = subprocess.Popen(cmd, stdin=p.stdout, stdout=subprocess.PIPE)
    pinit.stdout.close()
    output,err = p.communicate()
    words = output.decode().split("\n")[:-1]
    # fd.close()
    return words


# separate_cmds("test_files/words_utf8.txt", cmds)


# p1 = subprocess.Popen(["cat", "file.log"], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(["tail", "-1"], stdin=p1.stdout, stdout=subprocess.PIPE)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
# output,err = p2.communicate()
