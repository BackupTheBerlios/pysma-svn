"""
whitePages module
-------------
It is a system which references all agent ids.
@author Damien Boucard
"""

class WhitePages(object):    
    def __init__(self):
        self.__directory = {}
        self.__reverse = {}
        
    def register(self, id, agent, name, parent):
        if id not in self.__directory:
            dico = {"agent": agent}
            if name!=None:
                dico["name"] = name
            if parent!=None:
                dico["parent"] = parent
            self.__directory[id] = dico
            self.__reverse[agent] = id
            
    def unregister(self, agentId):
        if agentId in self.__directory:
            agent = self.__directory.pop(agentId)["agent"]
            del self.__reverse[agent]
                
    def getAgent(self, id):
        return self.__directory.get(id, {"agent":None})["agent"]
        
    def getId(self, agent):
        return self.__reverse.get(agent, None)
