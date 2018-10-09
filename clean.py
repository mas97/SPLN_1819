import subprocess
import sys
import re

cmds = "cat words.txt | sed 's/\ /;/g' | cut -d ';' -f 2 | iconv -f latin1 -t ascii//TRANSLIT | sed -e 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/' | sort | uniq"


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

def separate_cmds(cmds):
    # Faz split pelos espaços que não tenham uma \ antes
    cmd_sep = re.compile(r'(?<!\\) +').split(cmds)
    arrs = split_pipes(cmd_sep)
    print(arrs)

separate_cmds(cmds)


# p1 = subprocess.Popen(["cat", "file.log"], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(["tail", "-1"], stdin=p1.stdout, stdout=subprocess.PIPE)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
# output,err = p2.communicate()
