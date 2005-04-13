"""
Scheduler module
-------------
It is the class of an agent which schedules other agents.
@author Damien Boucard
"""
from agent import Agent
import thread

class Scheduler(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.__alive = False
        self.activators = []
        
    def born(self):
        self.__alive = True
        thread.start_new_thread(self.schedule)
        
    def die(self):
        self.__alive = False
        
    def schedule(self):
        while self.__alive:
            self.live()
            
    def live(self):
        pass
        
class Activator:
    """
    It is the class used by a scheduler to activate other agents.
    @author Damien Boucard
    """
    def __init__(self, group=None, role=None):
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
        if kernel!=None:
            return self.kernel.getAgentsWith(self.__group, self.__role)
        return []
    agents = property(getAgents)
    
    def activate(self):
        for id in agents:
            agent = self.kernel.getAgent(id)
            if agent != None:
                agent.live()
                
class DummyScheduler(Scheduler):
    def __init__(self):
        Scheduler.__init__(self)
        self.activators.append(Activator())
        
    def live():
        self.activators[0].activate()