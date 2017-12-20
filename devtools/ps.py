from _linux import lxrun


def get_pid_from_port(port):
    res = lxrun('netstat -apn | grep {0}'.format(port)).strip()
    res = re.split(' +', res, 7)
    pid = res[-1].split('/')[0]
    return pid

def get_pid(reg, debug=False):
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
    lxrun(cmd, daemon=True))
    pid = get_pid(cmd)
    return pid

