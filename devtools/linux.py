# coding: utf8
from subprocess import Popen, PIPE, DEVNULL
import os
import re

from .format import tostr


__all__ = ['lxrun']



def lxrun(cmd, err=False, bg=False, daemon=False):
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)

    if bg or daemon:
        p = Popen(cmd, shell=True, stdout=DEVNULL)
        return p 
        
    res = None
    p =  Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout = tostr(stdout).rstrip()
    stderr = tostr(stderr).rstrip()
    if err:
        return stdout, stderr
    else:
        return stdout


def pyrun(cmd, err=False, daemon=False):
    p = _py3_gen().__next__()
    cmd = ' '.join([p, cmd])
    return lxrun(cmd, err=err, daemon=daemon)

def _py3_gen():
    names = ['python3', 'python'] + ['python3.' + str(i) for i in range(8)]
    p = re.compile('is (/.*python3.*)|is aliased to \'(/.*python3.*)\'')
    for n in names:
        foo, err = lxrun('type ' + n, err=True)
        m = p.search(foo)
        if m:
            yield m.group(1)

    

