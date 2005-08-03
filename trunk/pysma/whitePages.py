"""
@author: Damien Boucard
@version: 0.3
"""
class WhitePages(object):
    """ It is a system which references all agent ids.
    @ivar __directory: Dictionnary which references agents and their ID.
    @type __directory: C{dict<int, dict<str, any>>}
    @ivar __reverse: A reverse directory in order to retrieve an ID with an agent object.
    @type __reverse: C{dict<L{Agent}, int>}
    """
    def __init__(self):
        """ White page constructor """
        self.__directory = {}
        self.__reverse = {}
        
    def register(self, id, agent, name, parent):
        """ Registers a new agent in the directory.
        @param id: ID of the agent, affected by the kernel.
        @type id: C{int}
        @param agent: Agent instance.
        @type agent: C{L{Agent}}
        @param name: Name of the agent.
        @type name: C{str}
        @param parent: Agent which launched the agent.
        @type parent: C{L{Agent}}
        """
        if id not in self.__directory:
            dico = {"agent": agent}
            if name!=None:
                dico["name"] = name
            if parent!=None:
                dico["parent"] = parent
            self.__directory[id] = dico
            self.__reverse[agent] = id
            
    def unregister(self, agentId):
        """ Unregisters an agent from the directory.
        @param agentId: ID of the agent.
        @type agentId: C{int}
        """
        if agentId in self.__directory:
            agent = self.__directory[agentId]["agent"]
            del self.__directory[agentId]
            del self.__reverse[agent]
                
    def getAgent(self, id):
        """ Gets the agent corresponding to the given ID.
        @param id: ID of the wanted agent.
        @type id: C{int}
        @return: The corresponding agent or C{None} if the ID does not exist in the kernel, or if corresponding agent has been killed.
        @rtype: C{L{Agent}}
        """
        return self.__directory.get(id, {"agent":None})["agent"]
        
    def getId(self, agent):
        """ Gets the ID of a given agent.
        @param agent: Agent which ID is wanted.
        @type agent: C{L{Agent}}
        @return: The corresponding ID or C{None} if the given agent is not launched in this kernel.
        @rtype: C{int}
        """
        return self.__reverse.get(agent, None)
