from monitor.status import Status
import os

def log(status: Status):
    print(status)

def kill(status: Status):
    os.kill(status.pid, 1)