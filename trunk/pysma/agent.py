"""
@author: Damien Boucard
@version: 0.3
"""
class Agent(object):
    """ It is the class of an agent of the multi-agent system.
    @ivar kernel: The kernel where the agents lives. C{None} until born or since died.
    @type kernel: C{L{Kernel}}
    @type id: C{int}
    @ivar __msgbox: Incomming message box.
    @type __msgbox: C{list<L{Message}>}
    @group Abstract methods: born, live, die
    @group Message methods: sendMessage, sendBroadcastMessage, receiveMessage, getNextMessage, hasMessage
    @group Organization methods: requestRole, leaveRole
    """
    def __init__(self):
        """ Agent constructor. """
        self.kernel = None
        self.__msgbox = []
        
    def __getId(self):
        """ C{L{id}} property getter.
        @return: The ID.
        @rtype: C{int}
        """
        return self.kernel.getAgentId(self)
    id = property(__getId, "The ID of the agent (Read only).")
    
    def addAgent(self, agent, name="unamed"):
        """ Launches a child agent.
        @param agent: Agent to launch.
        @type agent: C{L{Agent}}
        @param name: Name of the new agent.
        @type name: C{str}
        """
        if self.kernel != None:
            self.kernel.addAgent(agent, name, self)
        
    # ABSTRACT METHODS
    def born(self):
        """ Abstract method which is called when the agent is launched. """
        pass
        
    def live(self):
        """ Abstract method which is called by a L{scheduler<Scheduler>}. """
        pass
        
    def die(self):
        """ Abstract method which is called when the agent is killed. """
        pass
        
    # MESSAGE MANAGEMENT
    def sendMessage(self, message, receiver):
        """ Sends a message to another agent.
        @param receiver: ID of the agent who will receive the message.
        @type receiver: C{int}
        @param message: Message to send.
        @type message: C{L{Message}}
        """
        if self.kernel != None:
            message.sender = self.id
            message.receiver = receiver
            self.kernel.sendMessage(message)
    
    def sendBroadcastMessage(self, message, role=None, group=None):
        """ Sends a message to all the agent of a given role.
        @param message: Message to send.
        @type message: C{L{Message}}
        @param role: Role of the agents who will receive the message (if C{group} and C{role} equal C{None}, the common role is used).
        @type role: C{str}
        @param group: Group of the concerned role (if C{None}, the common group is used).
        @type group: C{str}
        """
        message.sender = self.id
        message.receiver = (group,role)
        self.kernel.sendBroadcastMessage(message)
    
    def receiveMessage(self, message):
        """ Receives an incoming message and puts it, in the message box. Called by the kernel.
        @param message: The incoming message.
        @type message: C{L{Message}}
        """
        self.__msgbox.append(message)
    
    def getNextMessage(self):
        """ Gets the oldest message of the message box.
        @precondition: self.hasMessage()
        @return: The message.
        @rtype: C{L{Message}}
        """
        if self.kernel != None:
            return self.__msgbox.pop(0)
        return None
        
    def hasMessage(self):
        """ Verify if the message box is empty or not.
        @return: C{False}, if the message box is empty. C{True}, if there are one or more messages in the box (C{L{self.getNextMessage()<getNextMessage>}} can be called).
        @rtype: C{bool}
        """
        if self.kernel != None:
            return len(self.__msgbox) > 0
        return False

    # ORGANISATION MANAGEMENT
    def requestRole(self, role, group=None):
        """ Adds the agent into a given role.
        @note: The agent is automatically added into the common role at launching.
        @param role: Role in which agent is added (if C{role} and C{group} equal C{None}, agent is added in the common role).
        @type role: C{str}
        @param group: Group in which the role belongs to (if C{None}, the common group is used.
        @type group: C{str}
        """
        self.kernel.requestRole(self.id, role, group)
        
    def leaveRole(self, role, group=None):
        """ Removes the agent from a given role.
        @note: The agent is automatically added into the common role at launching.
        @param role: Role from which agent is removed (if C{role} and C{group} equal C{None}, agent is removed from the common role).
        @type role: C{str}
        @param group: Group in which the role belongs to (if C{None}, the common group is used.
        @type group: C{str}
        """
        self.kernel.leaveRole(self.id, role, group)