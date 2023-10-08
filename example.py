"""
An example for the application of the resource-monitor
"""
from multiprocessing import Process
import time

from monitor.monitor import Monitor
from monitor.policy import MultiProcessPolicy, SimplePolicy, CompositePolicy, AlwaysPolicy, IsDeadPolicy
from monitor.status import Status
from monitor.actions import log, kill

def test():
    temp = []
    
    while True:
        temp += [0] * 10000000
        time.sleep(1)

def died_reaction(status):
    monitor.remove_process(status.pid)
    new_test()

def new_test():
    ps = Process(target=test, daemon=True)
    ps.start()
    monitor.register_process(ps.pid, "test")

policy = CompositePolicy([AlwaysPolicy(log), SimplePolicy(kill, 1e9), IsDeadPolicy(died_reaction)])
policy = MultiProcessPolicy({"test": policy})
monitor = Monitor(policy)
monitor.start()
new_test()
monitor.join()
    