"""
message module
-------------
It is the class which represents messages transmitted between agents in the multi-agent system.
@author Damien Boucard
"""

class Message(object):
    def __init__(self, sender, receiver, content):
        self.__sender = sender    
        self.__receiver = receiver
        self.__content = content
        
    def getSender(self):
        return self.__sender
    sender = property(getSender)
        
    def getReceiver(self):
        return self.__receiver
    receiver = property(getReceiver)
        
    def getContent(self):
        return self.__content
    content = property(getContent)
    
    def __str__(self):
        return "<pysma.message.Message sender=%s, receiver=%s, content=%s>" %(self.sender, self.receiver, self.content)