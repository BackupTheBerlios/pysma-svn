"""
ActionAgent module
-------------
It is the subclass of an agent which processes messages by calling methods
@author Damien Boucard
"""
from agent import Agent

class ActionAgent(Agent):
    def __init__(self, prefix="evt", silent=False):
        Agent.__init__(self)
        self.prefix = prefix
        if silent:
            self.liveFct = self.silentlyProcessAllMessages
        else:
            self.liveFct = self.processAllMessages
    
    # Process one ActionMessage
    def processMessage(self, msg):
        action = self.prefix + msg.action.replace(' ', '_')
        if hasattr(self, action):
            fct = getattr(self, action)
            if callable(fct):
                fct(*msg.arg, **msg.kw)
                return
        raise NotHandledError(msg)
        
    # Launch message processing for the next message
    # (verify if hasNextMessage before)
    def processNextMessage(self):
        msg = self.getNextMessage()
        if msg != None:
            self.processMessage(msg.content)
        
    # Lanch message processing for all waiting messages
    # (until a NotHandledError is raised)
    def processAllMessages(self):
        while self.hasMessage():
            self.processNextMessage(self)
       
   # Lanch message processing for all waiting messages
   # (even if raised, don't manage NotHandledError)     
    def silentlyProcessAllMessages(self):
        try:
            self.processAllMessages()
        except NotHandledError:
            self.silentlyProcessAllMessages()

    def live(self):
        self.liveFct()
    
class ActionMessage:
    def __init__(action, arg, kw):
        self.action = action
        self.arg = arg
        self.kw = kw
                
    
class NotHandledError(AttributeError):
    pass