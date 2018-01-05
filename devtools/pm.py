'''
    A simple process manager
'''
import re
import warnings

from .linux import lxrun
from .exception import mute


__all__ = ['get', 'getpids', 'kill', 'reboot']


@mute(not __debug__, '')
def get(pid, spec):
    return lxrun('ps hp {0} -o {1}'.format(pid, spec)).strip()
    


@mute(not __debug__, [])
def getpids(cmd):
    '''get pids list by command'''
    foo = "ps -eo pid,command | \
           grep -v -P '(sudo|grep|PID.*COMMAND)' | \
           grep -P '{0}'".format(cmd)
    foo = lxrun(foo).split('\n')
    
    p = re.compile(' *(\d+)')
    return [int(p.match(i).group(1)) for i in foo if p.match(i)]
    

def kill(pid):
    _, err = lxrun('kill -9 {0}'.format(pid), err=True)
    if err:
        return False
    return True

def kills(cmd):
    res = 0
    for p in getpids(cmd):
        if kill(p):
            res += 1
    return res

@mute(not __debug__, 0.0)
def getwa():
    foo = lxrun('top -b -n 1 | grep wa')
    p = re.compile(' *([0-9.]*) *wa')
    m = p.search(foo)
    return float(m.group(1))
    

# Internal
def _get_pid_by_port(port):
    pattern = ':{} | PID\/P'.format(port)
    res = lxrun('netstat -apn | grep -E "{0}"'.format(pattern)).strip()
    lines = res.split('\n')
    if len(lines) == 1:
        return None
    else:
        site = re.search('PID\/P', lines[0]).start()
        pid = lines[1][site:].split('/')[0]
        if pid.isdigit():
            return pid
        else:
            return None


def getpid(pattern=None, port=None, command=None):
    if sum(map(lambda x: 0 if x is None else 1, locals().values())) != 1:
        raise TypeError('getpid() takes excatly one argument.')

    if port is not None:
        return _get_pid_by_port(port)

    if command is not None:
        foo = getpids(command)
        if foo:
            return foo[0]
        return 0

    if pattern is not None:
        pattern = '^.*(:[0-9]{{2}}){{2}} (?!sudo).*{}.*'.format(pattern)
        cmd = "ps -ef | grep -P '{0}'".format(pattern)
        res = lxrun(cmd)
        res = res.strip()
        if not res:
            return 0
        else:
            res = res.split('\n')
            res = filter(lambda x: 'grep' not in x, res)
            res = list(res)
            pid = re.split(' +', res[0])[1]
            return int(pid)

def getports(command=''):
    return get_port_names(command).keys()

def get_port_names(command='', pid=-1):
    '''get tcp listening port and names'''
    foo = lxrun("netstat -plnt")
    foo = foo.split('\n')
    
    p = 'tcp +\d+ +\d+ +[^ ]*:(\d+) .+' + \
        (str(pid) if pid>=0 else '\d+') + '/' + \
        '([^ ]*{0}[^ ]*)'.format(command)

    p = re.compile(p)
    res = {}
    for i in foo:
        m = p.match(i)
        if m:
            k, v= m.groups()
            if re.search(command, v):
                k = int(k)
                res[k] = v.strip()
    return res


def get_proc(pid):
    res = lxrun('ps p {0}| grep {0}'.format(pid)).strip()
    if not res:
        return None
    return res



def reboot(pid):
    cmd = get_command(pid)
    kill(pid)
    lxrun(cmd, daemon=True)
    pid = get_pid(pattern=cmd)
    return pid


# Old version API
def getcmd(pid):
    warnings.warn("pm.getcmd(pid) will be deleted in the futur.\nUse pm.get(pid, 'cmd') instead.", DeprecationWarning)
    return get(pid, 'cmd')
