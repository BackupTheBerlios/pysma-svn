"""
Scheduler module
-------------
It is the class of an agent which schedules other agents.
@author Damien Boucard
"""
from agent import Agent
import thread, time

class Scheduler(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.__alive = False
        self.activators = []
        
    def born(self):
        self.__alive = True
        for act in self.activators:
            act.kernel = self.kernel
        thread.start_new_thread(self.schedule, ())
        
    def die(self):
        self.__alive = False
        
    def schedule(self):
        while self.__alive:
            self.live()
            
    def live(self):
        pass
        
class Activator(object):
    """
    It is the class used by a scheduler to activate other agents.
    @author Damien Boucard
    """
    def __init__(self, role=None, group=None):
        self.__group = group
        self.__role = role
        self.kernel = None
        
    def getGroup(self):
        return self.__group
    group = property(getGroup)
    
    def getRole(self):
        return self.__role
    role = property(getRole)
    
    def getAgents(self):
        if self.kernel!=None:
            return self.kernel.getAgentsWith(self.__role, self.__group)
        return []
    agents = property(getAgents)
    
    def activate(self):
        for id in self.agents:
            #print id
            agent = self.kernel.getAgent(id)
            #print agent
            if agent != None:
                agent.live()
                
class DummyScheduler(Scheduler):
    def __init__(self, sleep=1):
        Scheduler.__init__(self)
        self.activators.append(Activator())
        self.sleep_duration = sleep
        
    def born(self):
        self.leaveRole(None)
        Scheduler.born(self)
        
    def live(self):
        self.activators[0].activate()
        time.sleep(self.sleep_duration)