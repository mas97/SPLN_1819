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
    if temp != []:
        arrs.append(temp)
    return arrs

def clean_spaces(cmd):
    pos = 0
    for pos in range(len(cmd)):
        cmd[pos] = cmd[pos].replace("\ ", " ")
    return cmd

def separate_cmds(input, cmds_str):
    first = True
    cmds_str = cmds_str.replace("'", "")
    cmds_str = cmds_str.replace('"', "")
    cmds_str = cmds_str.replace('\n', "")

    # Faz split pelos espaços que não tenham uma \ antes
    cmds_sep = re.compile(r'(?<!\\) +').split(cmds_str)
    cmds = split_pipes(cmds_sep)
    cmds[0] = clean_spaces(cmds[0])
    pinit = subprocess.Popen(cmds[0], stdin=input, stdout=subprocess.PIPE)
    if (len(cmds) > 1):
        for cmd in cmds[1:]:
            cmd = clean_spaces(cmd)
            if first:
                p = subprocess.Popen(cmd, stdin=pinit.stdout, stdout=subprocess.PIPE)
                first = False
            else:
                p = subprocess.Popen(cmd, stdin=p.stdout, stdout=subprocess.PIPE)
    pinit.stdout.close()
    output,err = p.communicate()
    words = output.decode().split("\n")[:-1]
    return words
