from unittest import TestCase, main 
import os

from devtools.linux import lxrun, _py3_gen, pyrun
from devtools.format import strtodict
from devtools import pm, lxget, SPEC
from devtools.exception import mute


class ExceptionTestCase(TestCase):
    def test_mute(self):
        a = []
        @mute(True, 1)
        def f(a):
            return a[1]
        self.assertEqual(f(a), 1)

class LinuxTestCase(TestCase):
    def test_lxrun(self):
        foo = lxrun(['ls', '-al'])
        bar = lxrun('ls -al')
        self.assertEqual(foo, bar)

        foo = lxrun("ps -eo pid,command | grep -P '(aberaerc|PID)'").split('\n')
        self.assertEqual(len(foo), 3)
    
    def test_py3(self):
        _py3_gen().__next__()
        foo = pyrun('-c "print(2)"')
        self.assertEqual(foo, '2')
        
    def test_lxget(self):
        print(lxget(SPEC.MANUFACTURER))

class PmTestCase(TestCase):
    def test(self):
        pid = pm.pid_of_listen_port(22)
        proc = pm.Process(pid)
        self.assertEqual('sshd',  pm.Process(pid).name())

        pid = pm.getpid(cmd='sshd')
        cmd = proc.cmd()
        self.assertTrue('sshd' in cmd)

        pid = os.getpid()
        self.assertTrue(10 >= proc.cpu_percent() >= 0)
        self.assertTrue(10 >= proc.memory_percent() >= 0)
        

    def test_getpid(self):
        foo = pm.getpids('sshd')
        print(foo)
        foo = pm.getpid('python.*test\.py')
        pid = os.getpid()
        proc1 = pm.Process(foo)
        proc2 = pm.Process(pid)

        self.assertEqual(foo, os.getpid())
    
    def test_getpids(self):
        foo = pm.getpids('sshd')
        self.assertTrue(len(foo) >= 4)

    def test_getports(self):
        foo = pm.getports()
        self.assertTrue(22 in foo)

    def test_get_port_names(self):
        foo = pm.get_port_names()
        self.assertTrue(22 in foo.keys())
        foo = pm.get_port_names('s+hd?')
        self.assertTrue('sshd' in foo[22])
    
        pids = pm.getpids('sshd')
        res = {}
        for pid in pids:
            pns = pm.get_port_names(pid=pid)
            if pns: 
                res.update(pns)
        self.assertEqual(res[22], 'sshd')

        pids = pm.getpids('asd')
        res = {}
        for pid in pids:
            pns = pm.get_port_names(pid=pid)
            if pns: 
                res.update(pns)
        self.assertFalse(res)

    def test_kill(self):
        cmd = '-c "while True: pass"'
        ps = [pyrun(cmd, daemon=True) for _ in range(3)]
        foo = pm.kills('while True')
        self.assertEqual(foo, 3)
        foo = [p.wait(timeout=3) for p in ps]
        self.assertEqual(set(foo), set([-9]))

class MainTestCase(TestCase):
    
    def test_strtodict(self):
        text = 'k1, v1\nk2 ,v2'
        res = strtodict(text, 'c', ',')
        d = {'k1':'v1', 'k2':'v2'}
        self.assertEqual(res, d)

        text = '''k1, d1v1, d2v1
                  k2, d1v2, d2v2, d3v2,
                  k3, d1v3, d2v3
                '''
        res = strtodict(text, 'cs', ',', ',')
        self.assertEqual(res, [{'k1': 'd1v1', 'k2': 'd1v2', 'k3':'d1v3'}, {'k1': 'd2v1','k2':'d2v2', 'k3':'d2v3'},{'k2':'d3v2'}])

        text = 'k1 k2\nv1 v2 v3\n'
        res = strtodict(text, 'r', ' ')
        self.assertEqual(res, d)

class TomcatTestCase(TestCase):
    
    def testTomcat(self):
       from devtools.tomcat import Tomcat
       t = Tomcat(name='sshd', port=22)
       print(t.status())

main() 
