import psutil
from threading import Thread, Event
from monitor.status import Status
from monitor.policy import MultiProcessPolicy

class Monitor:
    def __init__(self, policy: MultiProcessPolicy, update_period=1):
        self.processes_to_monitor = {}
        self.update_period = update_period
        self.thread = Thread(target=self.run_periodically)
        self.stop_event = Event()
        self.policy = policy
    
    def register_process(self, pid, name):
        self.processes_to_monitor[pid] = name

    def register_policy(self, name, policy):
        self.policy.set(name, policy)
    
    def run_periodically(self,):
        while not self.stop_event.wait(self.update_period):
            self.update()

    def update(self,):
        statuses = {}
        for pid,name in self.processes_to_monitor.items():
            status = Status(pid, name)
            status.update()
            statuses[name] =  status
        self.policy.update(statuses)
    
    def start(self,):
        self.thread.start()

    def join(self,):
        self.thread.join()