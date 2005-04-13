"""
Agent module
-------------
It is the class of an agent of the multi-agent system.
@author Damien Boucard
"""
from message import Message

class Agent(object):
    def __init__(self):
        self.kernel = None
        self.__msgbox = []
        
    def getId(self):
        return self.kernel.getAgentId(self)
    id = property(getId)
        
    # ABSTRACT METHODS
    def born(self):
        pass
        
    def live(self):
        pass
        
    def die(self):
        pass
        
    # MESSAGE MANAGEMENT
    def sendMessage(self, receiver, content):
        if self.kernel != None:
            msg = Message(self.id, receiver, content)
            return self.kernel.sendMessage(msg)
        return False
    
    def sendBroadcastMessage(self, content, group=None, role=None):
        msg = Message(self.id, (group,role), content)
        self.kernel.sendBroadcastMessage(msg)
    
    def receiveMessage(self, message):
        self.__msgbox.append(message)
    
    def getNextMessage(self):
        if self.kernel != None:
            return self.__msgBox.pop[0]
        return None
        
    def hasMessage(self):
        if self.kernel != None:
            return len(self.__msgbox) > 0
        return False

    # ORGANISATION MANAGEMENT
    def requestRole(self, group=None, role=None):
        self.kernel.requestRole(self.id, group, role)
        
    def leaveRole(self, group=None, role=None):
        self.kernel.leaveRole(self.id, group, role)