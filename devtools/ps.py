import re
from linux import lxrun


# Internal
def _get_pid_by_port(port):
    pattern = '":{} | PID/P"'.format(port)
    res = lxrun('netstat -apn | grep -e {0}'.format(pattern)).strip()
    lines = res.split('\n')
    if len(lines) == 1:
        return None
    else:
        site = re.search('PID\/P', lines[0])
        pid = lines[1][site:].split('/')[0]
        if pid.isdigit():
            return pid
        else:
            return None


def get_pid(reg, port=None, debug=False):


    if port:
        return get_pid_by_port(port)

    res = lxrun('ps -ef | grep {0}'.format(reg)).split('\n')[0]
    if debug:
        print(res)
    pid = re.split(' +', res)[1]
    return pid

def get_command(pid):
    res = lxrun('ps p {0}| grep {0}'.format(pid)).strip()
    res = re.split(' +', res, 4) 
    res = res[-1]
    return res

def kill(pid):
    return lxrun('kill -9 {0}'.format(pid))

def reboot(pid):
    cmd = get_command(pid)
    kill(pid)
    lxrun(cmd, daemon=True)
    pid = get_pid(cmd)
    return pid

if __name__ == '__main__':
    print('Start testing.')
    print(_get_pid_by_port(80))
