from multiprocessing import Process
import time

from monitor.monitor import Monitor
from monitor.policy import MultiProcessPolicy, SimplePolicy, CompositePolicy, AlwaysPolicy
from monitor.status import Status
from monitor.actions import log, kill

def test():
    temp = []
    while True:
        temp += [0] * 10000000
        time.sleep(1)


ps = Process(target=test)
ps.start()
print(ps.pid)
policy = CompositePolicy([AlwaysPolicy(log), SimplePolicy(kill, 1e9)])
policy = MultiProcessPolicy({"test": policy})
monitor = Monitor(policy)
monitor.start()
monitor.register_process(ps.pid, "test")
monitor.join()
    