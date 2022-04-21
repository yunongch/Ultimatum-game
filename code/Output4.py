# coding=UTF-8
import random
import math


class Agent:
    ID = -1
    bank = -1.0
    theta = -1.0
    Lambda = -1.0

    def printSelf(self):
        print("[Agent]id:", self.ID, "bank:", self.bank, "theta:", self.theta, "lambda:", self.Lambda)

    def __init__(self, ID, bank, theta, Lambda):
        self.ID = ID
        self.bank = bank
        self.theta = theta
        self.Lambda = Lambda


# constants for the whole program
agentAmount_left = 25
agentAmount_right = 25
bank = 1
k = 0.0
k_times = 3
p = 0.25

agentList = []
index_left = []
index_right = []
vertices = []
temp_vertices = []
sbStillGotMoney = True


# methods
def inputParams():
    global k
    while True:
        input_temp = input("plz input k:")
        try:
            input_temp = float(input_temp)
            k = input_temp
            break
        except:
            print("A float expected")
    return

def initAgents():
    for i in range(0, (agentAmount_left + agentAmount_right)):
        agentList.append(Agent(i, bank, random.random(), random.random()))
        if i < agentAmount_left:
            index_left.append(i)
        else:
            index_right.append(i)

def printAgentList():
    print("-----------------------------")
    for agent in agentList:
        agent.printSelf()
    print("-----------------------------")

def getVertices():
    for i in range(0, len(index_left)):
        for j in range(i + 1, len(index_left)):
            vertices.append(( index_left[i], index_left[j] ))
    for i in range(0, len(index_right)):
        for j in range(i + 1, len(index_right)):
            vertices.append(( index_right[i], index_right[j] ))
    vertices.append(( index_left[0], index_right[0] ))

def removeAgentFromVertices(index):
    # indices of agents whom need to delete
    index_del = []
    for i in range(0, len(temp_vertices)):
        if temp_vertices[i][0] == index or temp_vertices[i][1] == index:
            index_del.append(i)
    index_del.reverse()
    for i in index_del:
        temp_vertices.pop(i)

def mimic(index):
    """the agent needs to mimic"""
    agent_mimic = agentList[index]

    agents_wealthier = []
    sum_bank = 0.0
    if index_left.__contains__(index):
        temp_list = index_left
    else:
        temp_list = index_right

    for i in temp_list:
        if agentList[i].bank > agent_mimic.bank:
            agents_wealthier.append(agentList[i])
            sum_bank += agentList[i].bank

    """Algorithm"""
    newTheta = agent_mimic.theta
    newLambda = agent_mimic.Lambda
    denominator = sum_bank - agent_mimic.bank * len(agents_wealthier)
    for agent in agents_wealthier:
        numerator_theta = (agent.bank - agent_mimic.bank) * (agent.theta - agent_mimic.theta)
        newTheta += numerator_theta / denominator
        numerator_lambda = (agent.bank - agent_mimic.bank) * (agent.Lambda - agent_mimic.Lambda)
        newLambda += numerator_lambda / denominator
    return Agent(agent_mimic.ID, agent_mimic.bank, newTheta, newLambda)



def playInVertices():
    index_bankrupted = []

    while len(temp_vertices) > 0:
        target_index = math.floor(random.random() * len(temp_vertices))
        if random.random() < random.random():
            index_offeror = temp_vertices[target_index][0]
            index_responder = temp_vertices[target_index][1]
        else:
            index_responder = temp_vertices[target_index][0]
            index_offeror = temp_vertices[target_index][1]

        offeror = agentList[index_offeror]
        responder = agentList[index_responder]

        if offeror.theta >= responder.Lambda:
            offeror.bank += (1 - offeror.theta) * 10
            responder.bank += offeror.theta * 10;

        """the cost of living"""
        offeror.bank -= k * k_times
        responder.bank -= k * k_times

        """log who's bankrupted"""
        if offeror.bank < 0:
            index_bankrupted.append(index_offeror)
        if responder.bank < 0:
            index_bankrupted.append(index_responder)

        """delete the chosen players"""
        removeAgentFromVertices(index_offeror)
        removeAgentFromVertices(index_responder)

    index_bankrupted.sort()
    return index_bankrupted

def play():
    index_bankrupted = playInVertices()

    """whether all agents are bankrupted"""
    if len(index_bankrupted) == len(agentList):
        global sbStillGotMoney
        sbStillGotMoney = False
    else:
        """agents mimic"""
        new_agentList = []
        for index in range(len(agentList)):
            if not index_bankrupted.__contains__(index):
                new_agentList.append(mimic(index))

        """update agentList"""
        index_new_agentList = 0
        for index in range(len(agentList)):
            if index_new_agentList >= len(new_agentList):
                break
            if not index_bankrupted.__contains__(index):
                agentList[index] = new_agentList[index_new_agentList]
                index_new_agentList += 1


        """Reproduce"""
        reproduced_agents = []
        if len(index_bankrupted) > 0:
            """split new agents into 2 groups"""
            left_new_agent = []
            right_new_agent = []
            sum_left_new_agent = 0.0
            sum_right_new_agent = 0.0

            for agent in new_agentList:
                if index_left.__contains__(agent.ID):
                    left_new_agent.append(agent)
                    sum_left_new_agent += agent.bank
                else:
                    right_new_agent.append(agent)
                    sum_right_new_agent += agent.bank

            """use algorithm to randomly pick an agent for each bankrupted agent"""
            for index in index_bankrupted:
                if index_left.__contains__(agent.ID):
                    agent_target_group = left_new_agent
                    sum_target_group = sum_left_new_agent
                else:
                    agent_target_group = right_new_agent
                    sum_target_group = sum_right_new_agent

                target_index = -1
                random_num = random.random()
                index_new_AgentList = 0.0
                for i in range(len(agent_target_group)):
                    rate = agent_target_group[i].bank / sum_target_group
                    index_new_AgentList += rate
                    if index_new_AgentList >= random_num:
                        # chosen
                        target_index = i
                        break
                target_agent = agent_target_group[target_index]
                reproduced_agent = Agent(index, p * target_agent.bank, target_agent.theta, target_agent.Lambda)
                reproduced_agents.append(reproduced_agent)
                reproduced_agent.printSelf()
                print("is reproduced to replace")
                agentList[agent_target_group[target_index].ID].bank *= 1 - p

        """update agentList"""
        if len(reproduced_agents) > 0:
            index_reproduced_agents = 0
            for i in range(0, len(agentList)):
                if agentList[i].bank < 0:
                    agentList[i] = reproduced_agents[index_reproduced_agents]
                    index_reproduced_agents += 1

    print("Result of Round", round_count)
    print("Bankrupted:", len(index_bankrupted))
    printAgentList()
    print("---------------------------------------")
    return




# Start of the program
print("Program started")

inputParams()
initAgents()
getVertices()
print("------------Original Data-----------")
printAgentList()
print("------------------------------------")

round_count = 1
while sbStillGotMoney and round_count <= 300:
    temp_vertices = vertices[:]
    play()
    round_count += 1

# Result output to txts
file_theta = open("theta.txt", "w", encoding='utf-8')
file_lambda = open("lambda.txt", "w", encoding='utf-8')

for agent in agentList:
    file_theta.write(str(agent.theta))
    file_theta.write("\n")
    file_lambda.write(str(agent.Lambda))
    file_lambda.write("\n")

file_theta.close()
file_lambda.close()
print("Program ended")
