# coding: utf8
from subprocess import Popen, PIPE
from devtools.format import tostr
import os

__all__ = ['lxrun']

def lxrun(cmd, err=False, daemon=False):
    if daemon is True:
        Popen(cmd, shell=True, stdout=open(os.devnull, 'w'))
        return
        
    res = None
    p =  Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout = tostr(stdout)
    stderr = tostr(stderr)
    if err:
        return stdout, stderr
    else:
        return stdout

