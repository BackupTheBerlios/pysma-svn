"""
@author: Damien Boucard
@version: 0.3
"""
from agent import Agent
from message import Message

class ActionAgent(Agent):
    """ It is the subclass of an agent which processes messages by calling methods.
    
    An event-specific handler is an instance method which handle one and only one action type. It has a conventionnal name made by the concatenation of the C{prefix} L{constructor<__init__>} parameter + the action name + the C{suffix} L{constructor<__init__>} parameter.
    
    The default handler is an instace method which handle each action message which cannot be handled by its repective action-specific handler. It has a conventionnal name defined by the C{default} L{constructor<__init__>} parameter.
    
    If the event cannot be handled (because the default handler is not implemented), an C{L{UnhandledActionError}} is raised, except if C{L{silent}} flag is C{True}.
    
    If a message which is not an C{L{ActionMessage}} instance is processed, it will be handled by the default handler. If the default handler is not implemented, the message will be ignored.
    @ivar pattern: Action-specific handler pattern.
    @type pattern: C{str}
    @ivar silent: Silent flag. If C{False}, C{L{UnhandledActionError}} is raised if an action cannot be handled. If C{True}, do nothing, listener does not handle the event.
    @type silent: C{str}
    @ivar currentMessage: The last message processed. C{None} when no action-specific handler is executing.
    @type currentMessage: C{L{Message}}
    """
    def __init__(self, prefix="msg", suffix="", default="messageReceived", silent=False):
        """ Action agent constructor.
        @param prefix: Prefix for all action-specific handler function name.
        @type prefix: C{str}
        @param suffix: Suffix for all action-specific handler function name.
        @type suffix: C{str}
        @param default: Default handler function name.
        @type default: C{str}
        @param silent: Silent flag.
        @type silent: C{bool}
        """
        Agent.__init__(self)
        self.pattern = prefix + "%s" + suffix
        if hasattr(self, default):
            self.__defaultHandler = getattr(self, default)
        self.silent = silent
        self.currentMessage = None
    
    # Launch message processing for the next message
    def processActionMessage(self, msg):
        """ Processes a message to be handled.
        @param msg: The message processed.
        @type msg: C{L{ActionMessage} or L{Message}}
        @raise UnhandledActionError: if C{L{silent}} is C{False} and there is no default handler to handle the message.
        """
        if msg == None:
            return
        if isinstance(msg, ActionMessage):
            action = self.pattern %(msg.action.replace(' ', '_'))
            if hasattr(self, action):
                fct = getattr(self, action)
                if callable(fct):
                    self.currentMessage = msg
                    try:
                        fct(*msg.arg, **msg.kw)
                        self.currentMessage = None
                    except:
                        self.currentMessage = None
                        raise
                    return
        self.__default_handler(msg)        
        
    # Lanch message processing for all waiting messages
    def processAllMessages(self):
        """ Processes all the messages of the box to be handled.
        @raise UnhandledActionError: if C{L{silent}} is C{False} and there is no default handler to handle a message.
        """
        while self.hasMessage():
            self.processActionMessage(self.getNextMessage())
       
    def __default_handler(message):
        """ The default function for the default handler. If the C{default} L{constructor<__init__>} parameter is not implememented, this function will be used.
        @param message: The message which cannot be handled.
        @type message: C{L{ActionMessage} or L{Message}}
        @raise UnhandledActionError: if C{L{silent}} is C{False} and the message is an C{L{ActionMessage}} instance.
        """
        if not silent and isinstance(message, ActionMessage):
            raise UnhandledActionError(message)

    def live(self):
        """ Method which is called by a L{scheduler<Scheduler>}. It only processes all incoming messages, but it can be overrided. """
        self.processAllMessages()

    
class ActionMessage(Message):
    """ Represents a message to an C{L{ActionAgent}} which will call the corresponding method.
    @type action: C{str}
    @type arg: C{tuple or list}
    @type kw: C{dict}
    """
    def __init__(self, action, arg, kw={}):
        """ Action message constructor.
        @param action: Type of the action to perform. The name of the handler will depend on the action name.
        @type action: C{str}
        @param arg: Arguments attached to the action (Empty tuple (C{()}) for none).
        @type arg: C{tuple or list}
        @param kw: Keywords (optional arguments) attached to the action (Empty dictionnary (C{E{lb}E{rb}}) for none).
        @type kw: C{dict}
        """
        Message.__init__(self, (action, arg, kw))
        
    def __getAction(self):
        """ C{L{action}} property getter.
        @return: The name of the action.
        @rtype: C{str}
        """
        return self.content[0]
    
    action = property(__getAction, doc="Type of the action to perform. The name of the handler will depend on the action name.")
    

    def __getArguments(self):
        """ C{L{arg}} property getter.
        @return: The action arguments.
        @rtype: C{tuple or list}
        """
        return self.content[1]
    arg = property(__getArguments, doc="Arguments attached to the action (Empty tuple (C{()}) for none).")
        
    def __getKeywords(self):
        """ C{L{kw}} property getter.
        @return: The action keywords.
        @rtype: C{dict}
        """
        return self.content[2]
    kw = property(__getKeywords, doc="Keywords (optional arguments) attached to the action (Empty dictionnary (C{E{lb}E{rb}}) for none).")
    
    def __str__(self):
        return "<pysma.actionAgent.ActionMessage sender=%s receiver=%s content=%s(*%s, **%s)>" %(self.sender, self.receiver, self.action, self.arg, self.kw)
                
    
class UnhandledActionError(AttributeError):
    """ Error raised when an action message cannot be handled, except if C{L{silent<ActionAgent.silent>}} flag is C{True}. """
    pass