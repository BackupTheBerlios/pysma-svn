"""
@author: Damien Boucard
@version: 0.3
"""
from whitePages import WhitePages
from message import Message

class Kernel(object):
    """ The core of the multi-agent system.
    @cvar instance: The last created instance, for a global access (by all agents).
    @type instance: C{L{Kernel}}
    @cvar __agentCounter: Used for affect a new agent IDs. In each agent creation, it increments.
    @type __agentCounter: C{int}
    @ivar __wPages: Agent white pages for this kernel.
    @type __wPages: C{L{WhitePages}}
    @ivar __agents: Collection of agents in this kernel.
    @type __agents: C{list<L{Agent}>}
    @ivar __groups: Collection of groups and roles to access to agent IDs in this kernel. Dictionnary of groups (type C{str}) which point to a dictionnary of roles (type C{str}) which point to a list of agent ids (type C{int}).
    @type __groups: C{dict<str, dict<str, list<int>>>}
    @ivar __roles: Collection of agent IDs to access to groups and roles in this kernel. Dictionnary of agent IDs (type C{int}) which point to a list of couples (type C{tuple}) which contain a group (type C{str}) and a role (type C{str}).
    @type __roles: C{dict<int, list<(str, str)>>}
    @group Agent Management: addAgent, removeAgent, getAgent, getAgentId, getAgentNb
    @group Message Management: sendMessage, sendBroadcastMessage
    @group Organization Management: requestRole, leaveRole, leaveAllRoles, getGroupsOf, getGroups, getRoles, getRolesOf, getAgentsIn, getAgentsWith
    """
    instance = None
    __agentCounter = 0
    
    def __init__(self):
        """ Kernel constructor. """
        Kernel.instance = self
        Kernel.__agentCounter = 0
        self.__wPages = WhitePages()
        self.__agents = []
        self.__groups = {}
        self.__roles = {}
        
    def stopKernel(self):
        """ Shutdowns the kernel. Stops all agents living in this kernel. """
        Kernel.instance = None
        for agt in self.__agents:
            self.removeAgent(self.getAgentId(agt))
        
    # AGENT MANAGEMENT
    def addAgent(self, agent, name="unamed", parent=None):
        """ Launchs an agent in this kernel.
        @param agent: Agent to launch.
        @type agent: C{L{Agent}}
        @param name: Name of the agent in the white pages (Optional).
        @type name: C{str}
        @param parent: Parent agent of the launched agent (Optional).
        @type parent: C{L{Agent}}
        """
        id = Kernel.__agentCounter
        Kernel.__agentCounter = id + 1
        self.__wPages.register(id, agent, name, parent)
        self.__agents.append(agent)
        self.__roles[id] = []
        self.requestRole(id)
        agent.kernel = self
        agent.born()
        
    def removeAgent(self, agentId):
        """ Kills an agent from this kernel.
        @param agentId: ID of the killed agent.
        @type agentId: C{int}
        """
        agent = self.__wPages.getAgent(agentId)
        if agent != None:
            agent.die()
            agent.kernel = None
            self.__agents.remove(agent)
        self.__wPages.unregister(agentId)
        self.leaveAllRoles(agentId)
        del self.__roles[agentId]
        
    def getAgentId(self, agent):
        """ Gets the ID of a given agent.
        @param agent: Agent which ID is wanted.
        @type agent: C{L{Agent}}
        @return: The corresponding ID or C{None} if the given agent is not launched in this kernel.
        @rtype: C{int}
        """
        return self.__wPages.getId(agent)
    
    def getAgent(self, agentId):
        """ Gets the agent corresponding to the given ID.
        @param agentId: ID of the wanted agent.
        @type agentId: C{int}
        @return: The corresponding agent or C{None} if the ID does not exist in the kernel, or if corresponding agent has been killed.
        @rtype: C{L{Agent}}
        """
        return self.__wPages.getAgent(agentId)
    
    def getAgentNb(self):
        """ Gets the number of agents presently living in the kernel.
        @return: The number of agents.
        @rtype: C{int}
        """
        return len(self.__agents)
        
    # MESSAGE MANAGEMENT
    def sendMessage(self, message):
        """ Sends a message from an agent to another agent.
        @param message: Message to send.
        @type message: C{L{Message}}
        """
        agent = self.__wPages.getAgent(message.receiver)
        if agent != None:
            agent.receiveMessage(message)
            
    def sendBroadcastMessage(self, message):
        """ Sends a message from an agent to all the agents of a role.
        @param message: Message to send.
        @type message: C{L{Message}}
        """
        group, role = message.receiver
        if group in self.__groups and role in self.__groups[group]:
            for id in self.__groups[group][role]:
                agent = self.__wPages.getAgent(id)
                msg = message.__copy__()
                msg.receiver = id
                agent.receiveMessage(msg)
        
    # ORGANIZATION MANAGEMENT
    def requestRole(self, agentId, role=None, group=None):
        """ Adds an agent into a role. Creates the role and/or the group if not already existing.
        @note: All agents are automatically added into the common role at launching.
        @param agentId: ID of the agent to add.
        @type agentId: C{int}
        @param role: Role in which agent is added (if C{role} and C{group} equal C{None}, agent is added in the common role).
        @type role: C{str}
        @param group: Group in which the role belongs to (if C{None}, the common group is used.
        @type group: C{str}
        """
        if group in self.__groups:
            if role in self.__groups[group]:
                self.__groups[group][role].append(agentId)
            else:
                self.__groups[group][role] = [agentId,]
        else:
            self.__groups[group] = {role: [agentId,]}
        self.__roles[agentId].append((group, role))
    
    def leaveRole(self, agentId, role=None, group=None):
        """ Removes an agent from a role.
        @note: All agents are automatically added into the common role at launching.
        @param agentId: ID of the agent to remove.
        @type agentId: C{int}
        @param role: Role from which agent is removed (if C{role} and C{group} equal C{None}, agent is removed from the common role).
        @type role: C{str}
        @param group: Group in which the role belongs to (if C{None}, the common group is used.
        @type group: C{str}
        """
        if group in self.__groups:
            if role in self.__groups[group]:
                self.__groups[group][role].remove(agentId)
        self.__roles[agentId].remove((group, role))

    def leaveAllRoles(self, agentId):
        """ Removes an agent from all roles of all groups. It includes the common role.
        @param agentId: ID of the agent to remove.
        @type agentId: C{int}
        """
        for group, role in self.__roles[agentId]:
            self.__groups[group][role].remove(agentId)
        self.__roles[agentId] = []
        
    def getGroupsOf(self, agentId):
        """ Gets all the groups in which the given agent has a role.
        @param agentId: ID of the concerned agent.
        @type agentId: C{int}
        @return: A collection of groups.
        @rtype: C{list<str>}
        """
        groups = []
        for group, role in self.__roles[agentId]:
            groups.append(group)
        return groups
        
    def getGroups(self):
        """ Gets the existing groups created in the kernel.
        @return: A collection of groups.
        @rtype: C{list<str>}
        """
        return self.__groups.keys()
        
    def getRoles(self, group=None):
        """ Gets the existing roles created in the kernel of the given group.
        @param group: Group in which the roles are wanted (if C{None}, the common group is used).
        @type group: C{str}
        @return: A collection of roles.
        @rtype: C{list<str>}
        """
        return self.__groups.get(group, {}).keys()
        
    def getRolesOf(self, agentId, group=None):
        """ Gets all the roles in which an agent is, in a given group.
        @param agentId: ID of the concerned agent.
        @type agentId: C{int}
        @param group: Group in which the roles are wanted (if C{None}, the common group is used).
        @type group: C{str}
        @return: A collection of roles.
        @rtype: C{list<str>}
        """
        roles = []
        for grp, rol in self.__roles.get(agentId, ()):
            if grp == group:
                roles.append(rol)
        return roles
        
    def getAgentsIn(self, group=None):
        """ Gets all the agent having one or more roles in the given group.
        @param group: Group in which the agents are wanted (if C{None}, the common group is used).
        @type group: C{str}
        @return: A collection of agent IDs.
        @rtype: C{list<int>}
        """
        agents = []
        roles = self.__groups.get(group, {})
        for role in roles:
            agents.extend(roles[role])
        return agents
        
    def getAgentsWith(self, role=None, group=None):
        """ Gets all the agent having the given role.
        @param role: Role in which the agents are wanted (if C{group} and C{role} equal C{None}, the common role is used).
        @type role: C{str}
        @param group: Group of the concerned role (if C{None}, the common group is used).
        @type group: C{str}
        @return: A collection of agent IDs.
        @rtype: C{list<int>}
        """
        return self.__groups.get(group, {}).get(role, ())[:]