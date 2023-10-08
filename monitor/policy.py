"""
Common/Base Policies for the monitor
"""
from monitor.status import Status

class Policy:
    """
    Base class for policies
    """
    def update(self, status):
        """
        virtual update function - override
        """

class IsDeadPolicy:
    """
    Trigger a reaction when the process dies
    """
    def __init__(self, reaction):
        self.reaction = reaction
  
    def update(self, status: Status):
        if not status.is_alive():
            self.reaction(status)

class AlwaysPolicy(Policy):
    """
    Trigger a reaction whenever there is a status update
    """
    def __init__(self, reaction) -> None:
        self.reaction = reaction
    
    def update(self, status: Status):
        self.reaction(status)

class SimplePolicy(Policy):
    """
    Trigger a reaction when CPU or MEM are above threshold
    """
    def __init__(self, reaction, mem_threshold=-1, cpu_threshold=-1) -> None:
        self.mem_threshold = mem_threshold
        self.cpu_threshold = cpu_threshold
        self.reaction = reaction

    def update(self, status: Status):
        if not status.alive:
            return
        if self.mem_threshold != -1 and status.memory > self.mem_threshold:
            self.react(status)
        elif self.cpu_threshold != -1 and status.cpu > self.cpu_threshold:
            self.react(status)
    
    def react(self, status: Status):
        """
        Calls the reaction - expected to be overriden.
        """
        self.reaction(status)

class CompositePolicy(Policy):
    """
    Apply multiple policies in a row
    """
    def __init__(self, policies: list[Policy]) -> None:
        self.policies = policies
    
    def update(self, status: Status):
        for policy in self.policies:
            policy.update(status)

class MultiProcessPolicy:
    """
    Holds the configuration of policies.
    relates a logical process to the underlying policy
    """
    def __init__(self, policies: dict[str, Policy]):
        self.policies = policies

    def update(self, statuses: dict[str, Status]):
        """
        Update policies of the status
        """
        for name, status in statuses.items():
            self.policies[name].update(status)

    def set(self, name, policy):
        """
        Set a policy.
        """
        self.policies[name] = policy
