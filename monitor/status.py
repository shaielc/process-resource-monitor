import psutil

class Status:
    def __init__(self, pid, name) -> None:
        self.pid = pid
        self.name = name
        self.alive = None
        self.memory = None
        self.cpu = None
    
    def update(self,):
        try:
            process = psutil.Process(self.pid)
            self.alive = True
        except psutil.NoSuchProcess:
            print("?")
            self.alive = False
            return
        self.memory = process.memory_info().rss
        self.cpu = process.cpu_percent()
    
    def is_alive(self,):
        return self.alive
    
    def __str__(self) -> str:
        return f"PID: {self.pid} | Name: {self.name} | Alive: {self.alive} | MEM: {self.memory} | CPU: {self.cpu}%"