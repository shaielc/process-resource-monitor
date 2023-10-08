from monitor.status import Status

class Policy:
    def update(self, status):
        pass

class AlwaysPolicy(Policy):
    def __init__(self, reaction) -> None:
        self.reaction = reaction
    
    def update(self, status: Status):
        self.reaction(status)

class SimplePolicy(Policy):
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
        self.reaction(status)

class CompositePolicy(Policy):
    def __init__(self, policies: list[Policy]) -> None:
        self.policies = policies
    
    def update(self, status: Status):
        for policy in self.policies:
            policy.update(status)

class MultiProcessPolicy:
    def __init__(self, policies: dict[str, Policy]):
        self.policies = policies
    
    def update(self, statuses: dict[str, Status]):
        for name, status in statuses.items():
            self.policies[name].update(status)
        
    def set(self, name, policy):
        self.policies[name] = policy
