"""
A class the contains a sample of the status of the process.
"""
import psutil

def size_human_format(num):
    if num is None:
        return 
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:.2f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

class Status:
    """
    The process status
        pid - the processes pid 
        name - the proceses logical name
        alive - is the process alive
        memory - memory usage
        cpu - cpu usage (%)
    """
    def __init__(self, pid, name) -> None:
        self.pid = pid
        self.name = name
        self.alive = None
        self.status_code = None
        self.memory = None
        self.cpu = None
    
    def update(self,):
        """
        Get current status
        """
        try:
            process = psutil.Process(self.pid)
            self.alive = process.status() in [psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING]
            self.status_code = process.status()
        except psutil.NoSuchProcess:
            self.alive = False
        if not self.alive:
            return
        self.memory = process.memory_info().rss
        self.cpu = process.cpu_percent(1)
    
    def is_alive(self,):
        """
        Return if process is alive
        """
        return self.alive
    
    def __str__(self) -> str:
        return f"PID: {self.pid} | Name: {self.name} | Alive: {self.alive} | MEM: {size_human_format(self.memory)} | CPU: {str(self.cpu) + '%' if self.cpu is not None else None} | STATUS: {self.status_code}"