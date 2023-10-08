"""
Common/Usefull actions to take, when monitoring processes.
"""
import signal
import os
from monitor.status import Status

def log(status: Status):
    """
    log status of process
    """
    print(status)

def kill(status: Status):
    """
    Kills the process with pid == <status.pid>
    """
    os.kill(status.pid, signal.SIGSTOP)
