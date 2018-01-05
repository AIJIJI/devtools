'''
    A simple process manager
'''

import re
from devtools.linux import lxrun

__all__ = ['getpid', 'get_command', 'kill', 'reboot']

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

def getpids(command):
    '''get pid list by command'''
    foo = "ps -eo pid,command | \
           grep -v -P '(sudo|grep|PID.*COMMAND)' | \
           grep -P '{0}'".format(command)
    foo = lxrun(foo).split('\n')
    
    p = re.compile(' *(\d+)')
    res = []
    for i in foo:
        m = p.match(i)
        if m:
            res.append(int(m.group(1)))
    return res

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
    
    p = 'tcp +\d+ +\d+ +[^ :]*:(\d+).+' + \
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

def getcmd(pid):
    res = lxrun('ps -eo pid,command | grep -P "^ *{0}"'.format(pid)).split('\n')
    res = [i for i in res if res and 'grep' not in res]
    if not res:
        return ''
    res = re.split(' +', res[0].strip(), 1) 
    if len(res) != 2
        return ''

    return res[1]

def kill(pid):
    _, err = lxrun('kill -9 {0}'.format(pid), err=True)
    if err:
        return False
    return True

def kills(command):
    res = 0
    for p in getpids(command):
        if kill(p):
            res += 1
    return res

def reboot(pid):
    cmd = get_command(pid)
    kill(pid)
    lxrun(cmd, daemon=True)
    pid = get_pid(pattern=cmd)
    return pid

if __name__ == '__main__':

    for pid in [0,1,2,100]:
        print(get_proc(pid))
    print('-' * 20)
    
    port = [12346, 0, 1, 80]
    for p in port:
        print('port at {0} is '.format(p) + str( _get_pid_by_port(p)))
    
    print('Pid of this is ' + get_pid(pattern='python.*pm\.py'))
    print('-'*20)
    pid = get_pid(port=12346)
    print('origin pid =', pid)
    cmd = get_command(pid)
    print('cmd =', repr(cmd))
    kill(pid)
    cmd2 = get_command(pid)
    print('killed cmd =', cmd2)
    lxrun(cmd, daemon=True)
    pid = get_pid(pattern=cmd)
    print('New pid:', pid)
    pid = reboot(pid)
    print('Another new pid', pid)
