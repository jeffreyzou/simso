# original FRP: discard executed work at preempted if is not finished
from simso.core.etm.AbstractExecutionTimeModel \
    import AbstractExecutionTimeModel


class MEMA(AbstractExecutionTimeModel):
    def __init__(self, sim, _):
        self.sim = sim
        self.executed = {}
        self.on_execute_date = {}		
	self.num_preempted = {}
	self.on_preempted_date = {}
	self.current_wcet = {}

    def init(self):
        pass

    def update_executed(self, job):
        if job in self.on_execute_date:
            self.executed[job] += (self.sim.now() - self.on_execute_date[job]
                                   ) * job.cpu.speed

            del self.on_execute_date[job]

    def on_activate(self, job):
        self.executed[job] = 0
	self.num_preempted[job] = 0
	self.on_preempted_date[job] = 0
	self.current_wcet[job] = job.wcet
		
    def on_execute(self, job):
	if self.on_preempted_date[job] < self.sim.now():
		self.num_preempted[job] += 1
		
		# new computation time based on number of preemptions (and self.executed[job])
		# c = func(job.get_num_premptions)
		# self.current_wcet[job] = c

		self.executed[job] = 0
		
        self.on_execute_date[job] = self.sim.now()

    def on_preempted(self, job):
        self.update_executed(job)
	self.on_preempted_date[job] = self.sim.now()

    def on_terminated(self, job):
        self.update_executed(job)
	del self.current_wcet[job]
	del self.on_preempted_date[job]

    def on_abort(self, job):
        self.update_executed(job)
	del self.current_wcet[job]
	del self.on_preempted_date[job]

    def get_executed(self, job):
        if job in self.on_execute_date:
            c = (self.sim.now() - self.on_execute_date[job]) * job.cpu.speed
        else:
            c = 0
        return self.executed[job] + c

    def get_ret(self, job):
#        wcet_cycles = int(job.wcet * self.sim.cycles_per_ms)
        wcet_cycles = int(self.current_wcet[job] * self.sim.cycles_per_ms)
        return int(wcet_cycles - self.get_executed(job))

    def update(self):
        for job in list(self.on_execute_date.keys()):
            self.update_executed(job)
