"""
Kernel module
-------------
It is the core of the multi-agent system.
@author Damien Boucard
"""
from whitePages import WhitePages
from message import Message

class Kernel(object):
    instance = None
    __agentCounter = 0
    
    def __init__(self):
        Kernel.instance = self
        Kernel.__agentCounter = 0
        self.__wPages = WhitePages()
        self.__agents = []
        self.__groups = {}
        self.__roles = {}
        
    def stopKernel(self):
        Kernel.instance = None
        for agt in self.__agents:
            self.removeAgent(self.getAgentId(agt))
        
    # AGENT MANAGEMENT
    def addAgent(self, agent, name="unamed", parent=None):
        id = Kernel.__agentCounter
        Kernel.__agentCounter = id + 1
        self.__wPages.register(id, agent, name, parent)
        self.__agents.append(agent)
        self.__roles[id] = []
        self.requestRole(id)
        agent.kernel = self
        agent.born()
        
    def removeAgent(self, agentId):
        agent = self.__wPages.getAgent(agentId)
        if agent != None:
            agent.die()
            agent.kernel = None
            self.__agents.remove(agent)
        self.__wPages.unregister(agentId)
        self.leaveAllRoles(agentId)
        del self.__roles[agentId]
        
    def getAgentId(self, agent):
        return self.__wPages.getId(agent)
    
    def getAgent(self, agentId):
        return self.__wPages.getAgent(agentId)
    
    def getAgentNb(self):
        return len(self.__agents)
        
    # MESSAGE MANAGEMENT
    def sendMessage(self, message):
        agent = self.__wPages.getAgent(message.receiver)
        if agent != None:
            agent.receiveMessage(message)
            
    def sendBroadcastMessage(self, message):
        group, role = message.receiver
        if group in self.__groups and role in self.__groups[group]:
            for id in self.__groups[group][role]:
                agent = self.__wPages.getAgent(id)
                msg = Message(message.sender, id, message.content)
                agent.receiveMessage(msg)
        
    # ORGANIZATION MANAGEMENT
    def requestRole(self, agentId, role=None, group=None):
        if group in self.__groups:
            if role in self.__groups[group]:
                self.__groups[group][role].append(agentId)
            else:
                self.__groups[group][role] = [agentId,]
        else:
            self.__groups[group] = {role: [agentId,]}
        self.__roles[agentId].append((group, role))
    
    def leaveRole(self, agentId, role=None, group=None):
        if group in self.__groups:
            if role in self.__groups[group]:
                self.__groups[group][role].remove(agentId)
        self.__roles[agentId].remove((group, role))

    def leaveAllRoles(self, agentId):
        for group, role in self.__roles[agentId]:
            self.__groups[group][role].remove(agentId)
        self.__roles[agentId] = []
        
    def getGroupsOf(self, agentId):
        groups = []
        for group, role in self.__roles[agentId]:
            groups.append(group)
        return groups
        
    def getGroups(self):
        return self.__groups.keys()
        
    def getRoles(self, group=None):
        return self.__groups.get(group, {}).keys()
        
    def getRolesOf(self, agentId, group=None):
        roles = []
        for grp, rol in self.__roles.get(agentId, ()):
            if grp == group:
                roles.append(rol)
        return roles
        
    def getAgentsIn(self, group=None):
        agents = []
        roles = self.__groups.get(group, {})
        for role in roles:
            agents.extend(roles[role])
        return agents
        
    def getAgentsWith(self, role=None, group=None):
        return self.__groups.get(group, {}).get(role, ())[:]