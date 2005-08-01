"""
@author: Damien Boucard
@version: 0.3
"""
from agent import Agent
import thread, time

class Scheduler(Agent):
    """ It is the class of an agent which schedules other agents.
    @ivar activators: Collection of activators used by the scheduler.
    @type activators: C{L{Activator}}
    @ivar __alive: Alive flag. C{True} if the scheduler is running.
    @type __alive: C{bool}
    """
    def __init__(self):
        """ Scheduler constructor. """
        Agent.__init__(self)
        self.__alive = False
        self.activators = []
        
    def born(self):
        """ Runs the scheduler on another thread. """
        self.__alive = True
        for act in self.activators:
            act.kernel = self.kernel
        thread.start_new_thread(self.schedule, ())
        
    def die(self):
        """ Stops the scheduler. """
        self.__alive = False
        
    def schedule(self):
        """ Manages the scheduling. """
        while self.__alive:
            self.live()
            
    def live(self):
        """ Abstract method which activates a step of scheduling. """
        pass
        
class Activator(object):
    """ It is the class used by a scheduler to activate other agents of a certain role.
    @ivar kernel: The kernel where the activator works. C{None} when the affected scheduler is not running.
    @type kernel: C{L{Kernel}}
    @type role: C{str}
    @type group: C{str}
    @type agents: C{list<int>}
    @ivar __role: Role of the agents to activate (if C{group} and C{role} equal C{None}, the common role is used).
    @type __role: C{str}
    @ivar __group: Group of the concerned role (if C{None}, the common group is used).
    @type __group: C{str}
    """
    def __init__(self, role=None, group=None):
        """ Activator constructor.
        @param role: Role of the agents to activate (if C{group} and C{role} equal C{None}, the common role is used).
        @type role: C{str}
        @param group: Group of the concerned role (if C{None}, the common group is used).
        @type group: C{str}
        """
        self.__group = group
        self.__role = role
        self.kernel = None
        
    def getGroup(self):
        """ C{L{group}} property getter.
        @return: The group of the concerned role.
        @rtype: C{str}
        """
        return self.__group
    group = property(getGroup, doc="Group of the concerned role (if C{None}, the common group is used) (Read only).")
    
    def getRole(self):
        """ C{L{role}} property getter.
        @return: The role affected to the activator.
        @rtype: C{str}
        """
        return self.__role
    role = property(getRole, doc="Role of the agents to activate (if C{group} and C{role} equal C{None}, the common role is used) (Read only).")
    
    def getAgents(self):
        """ C{L{agents}} property getter.
        @return: The agents activated by this activator.
        @rtype: C{list<int>}
        """
        if self.kernel!=None:
            return self.kernel.getAgentsWith(self.__role, self.__group)
        return []
    agents = property(getAgents, doc="Collection of agents activated by this activator.")
    
    def activate(self):
        """ Activates all agents of the concerned role. """
        for id in self.agents:
            agent = self.kernel.getAgent(id)
            if agent != None:
                agent.live()
                
class DummyScheduler(Scheduler):
    """ Subclass which implements the abstract method of C{L{Scheduler}} with a very simple way. It activates all agents (on the common role), except itself of course.
    @ivar sleep_duration: Duration of the sleep (in seconds) of the thread between each step of scheduling.
    @type sleep_duration: C{float}
    """
    def __init__(self, sleep=1):
        """ Dummy scheduler constructor.
        @param sleep: Duration of the sleep (in seconds) of the thread between each step of scheduling.
        @type sleep: C{float}
        """
        Scheduler.__init__(self)
        self.activators.append(Activator())
        self.sleep_duration = sleep
        
    def born(self):
        self.leaveRole(None)
        Scheduler.born(self)
        
    def live(self):
        """ Activates a new step of scheduling. """
        self.activators[0].activate()
        time.sleep(self.sleep_duration)