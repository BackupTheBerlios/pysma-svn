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
        self.currentMessage = None
        self.trashbox = []
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
            if not isinstance(msg.content, ActionMessage):
                # Keep non-ActionMessages
                self.trashbox.append(msg)
                return
            self.currentMessage = msg
            try:
                self.processMessage(msg.content)
                self.currentMessage = None
            except:
                self.currentMessage = None
                raise
        
    # Lanch message processing for all waiting messages
    # (until a NotHandledError is raised)
    def processAllMessages(self):
        while self.hasMessage():
            self.processNextMessage()
       
   # Lanch message processing for all waiting messages
   # (even if raised, don't manage NotHandledError)     
    def silentlyProcessAllMessages(self):
        try:
            self.processAllMessages()
        except NotHandledError:
            self.silentlyProcessAllMessages()

    def live(self):
        self.trashbox = []
        self.liveFct()
    
class ActionMessage:
    def __init__(self, action, arg, kw={}):
        self.action = action
        self.arg = arg
        self.kw = kw
    
    def __str__(self):
        return "<pysma.actionAgent.ActionMessage %s(*%s, **%s)>" %(self.action, self.arg, self.kw)
                
    
class NotHandledError(AttributeError):
    pass