"""
@author: Damien Boucard
@version: 0.3
"""
class Message(object):
    """ It is the class which represents messages transmitted between agents in the multi-agent system.
    @ivar sender: ID of the agent who sent the message (Automatically set).
    @type sender: C{int}
    @ivar receiver: ID of the agent who received (or will receive) the message (Automatically set).
    @type receiver: C{int}
    @type content: any
    @ivar __content: Data content of the message.
    @type __content: any
    """
    def __init__(self, content):
        """ Message constructor.
        @param content: Data content of the message.
        @type content: any
        """
        self.sender = None    
        self.receiver = None
        self.__content = content
           
    def __getContent(self):
        """ C{L{content}} property getter.
        @return: Data content of the message.
        @rtype: any
        """
        return self.__content
    content = property(__getContent, doc="Data content of the message (Read only).")
            
    def __str__(self):
        """ Converts the message to string.
        @return: The converted string.
        @rtype: C{str}
        """
        return "<pysma.message.Message sender=%s receiver=%s content=%s>" %(self.sender, self.receiver, self.content)
        
    def __copy__(self):
        """ Makes a shallow copy of the message.
        @return: The copy.
        @rtype: C{L{Message}}
        """
        msg = Message(self.__content)
        msg.sender = self.sender
        msg.receiver = self.receiver
        return msg