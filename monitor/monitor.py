"""
The resource-monitor
"""
from threading import Thread, Event
from monitor.status import Status
from monitor.policy import MultiProcessPolicy

class Monitor:
    """
    Create a monitor with the specified policy.
    Polls information every <update-period>.
    """
    def __init__(self, policy: MultiProcessPolicy, update_period=1):
        self.processes_to_monitor = {}
        self.update_period = update_period
        self.thread = Thread(target=self.run_periodically)
        self.stop_event = Event()
        self.policy = policy

    def remove_process(self,pid):
        """
        Remove a PID from monitoring
        """
        self.processes_to_monitor.pop(pid)

    def register_process(self, pid, name):
        """
        Register a process to monitor
            pid - process id to monitor
            name - logical name of the process
        """
        self.processes_to_monitor[pid] = name

    def register_policy(self, name, policy):
        """
        Add a <policy> the will be applied to logical process <name>
        """
        self.policy.set(name, policy)
    
    def run_periodically(self,):
        """
        Runs <self.update> every <self.update_period>s
        
        call <self.stop> to stop.
        """
        while not self.stop_event.wait(self.update_period):
            self.update()

    def update(self,):
        """
        Get the status of all registered PIDs.
        And check the policy.
        """
        statuses = {}
        for pid,name in self.processes_to_monitor.items():
            status = Status(pid, name)
            status.update()
            statuses[name] =  status
        self.policy.update(statuses)
    
    def start(self,):
        """
        Start the monitor
        """
        self.thread.start()

    def join(self,):
        """
        Wait for monitor to stop.
        """
        self.thread.join()
    
    def stop(self,):
        """
        Stop the monitor
        """
        self.stop_event.set()