import subprocess
import sys
import re

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
    return words
