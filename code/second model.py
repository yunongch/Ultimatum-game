# coding=UTF-8
import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import os

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
path = "results"
agentAmount_left = 25
agentAmount_right = 25
bank = 1
k = 0.0
k_times = 3
p = 0.25

file_log = None
file_theta = None
file_lambda = None
file_bank = None
agentList = []
index_left = []
index_right = []
vertices = []
temp_vertices = []
sbStillGotMoney = True
extraBridges = 30
extraBridges_list = []
count_round = 1
stop = True
# methods
def restoreParams():
    global agentList
    global index_left
    global index_right
    global vertices
    global temp_vertices
    global sbStillGotMoney
    global count_round
    global extraBridges_list

    agentList = []
    index_left = []
    index_right = []
    vertices = []
    temp_vertices = []
    sbStillGotMoney = True
    count_round = 1
    extraBridges_list = []
def makeDir():
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

def inputParams():
    global k
    global extraBridges
    while True:
        input_temp = input("plz input k:")
        try:
            input_temp = float(input_temp)
            k = input_temp
            break
        except:
            print("A float expected")
    return

def getNeighbourIndicesList(targetIndex):
    neighbourIndicesList = []
    for tup in extraBridges_list:
        if tup[0] == targetIndex:
            neighbourIndicesList.append(tup[1])
        elif tup[1] == targetIndex:
            neighbourIndicesList.append(tup[0])
    return neighbourIndicesList

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
            vertices.append((index_left[i], index_left[j]))
    for i in range(0, len(index_right)):
        for j in range(i + 1, len(index_right)):
            vertices.append((index_right[i], index_right[j]))
    vertices.append((index_left[0], index_right[0]))

    # add extra bridges
    if extraBridges != 0:
        temp_left_index_list = index_left[1:]
        temp_right_index_list = index_right[1:]
        for i in range(0, extraBridges):
            not_done = True
            while not_done:
                target_left_index = math.floor(random.random() * len(temp_left_index_list))
                target_right_index = math.floor(random.random() * len(temp_right_index_list))
                target_bridge = (temp_left_index_list[target_left_index], temp_right_index_list[target_right_index])
                target_bridge_reverse = (temp_right_index_list[target_right_index], temp_left_index_list[target_left_index])
                if not vertices.__contains__(target_bridge) or not vertices.__contains__(target_bridge_reverse):
                    vertices.append(target_bridge)
                    extraBridges_list.append(target_bridge)
                    not_done = False

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

    # choose which community it's in
    if index_left.__contains__(index):
        temp_list = index_left[:]
    else:
        temp_list = index_right[:]

    # delete itself
    temp_list.remove(index)

    # add extra bridges
    if extraBridges != 0:
        neighbourIndicesList = getNeighbourIndicesList(index)
        for n in neighbourIndicesList:
            if not temp_list.__contains__(n):
                temp_list.append(n)

    # prepare data for the algorithm
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
        newTheta += 0.01*numerator_theta / denominator
        numerator_lambda = (agent.bank - agent_mimic.bank) * (agent.Lambda - agent_mimic.Lambda)
        newLambda += 0.01*numerator_lambda / denominator
    return Agent(agent_mimic.ID, agent_mimic.bank, newTheta, newLambda)


def playInVertices():
    index_bankrupted = []

    global temp_vertices
    temp_vertices = vertices[:]

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

        # accepted
        if offeror.theta >= responder.Lambda:
            offeror.bank += 1 - offeror.theta
            responder.bank += offeror.theta

        """the cost of living"""
        offeror.bank -= k 
        responder.bank -= k

        """log who's bankrupted"""
        if offeror.bank <= 0:
            index_bankrupted.append(index_offeror)
        if responder.bank <= 0:
            index_bankrupted.append(index_responder)

        """delete the chosen players"""
        removeAgentFromVertices(index_offeror)
        removeAgentFromVertices(index_responder)

        log_play = "%d play with %d\n" % (index_offeror, index_responder)
        log_remaining = "Remaining edge:" + temp_vertices.__str__() + "\n"
        file_log.write(log_play)
        file_log.write(log_remaining)
        file_log.flush()

    index_bankrupted.sort()
    return index_bankrupted

def play():
    file_log.flush()
    index_bankrupted = playInVertices()
    """whether all agents are bankrupted"""
    temp_index_left = index_left[:]
    temp_index_right = index_right[:]
    temp_index_left.reverse()
    temp_index_right.reverse()
    for index in index_bankrupted:
        if temp_index_left.__contains__(index):
            temp_index_left.remove(index)
        else:
            temp_index_right.remove(index)

    if len(temp_index_left) == 0 or len(temp_index_right) == 0:
        global sbStillGotMoney
        sbStillGotMoney = False
    else:
        """agents mimic"""
        new_agentList = []
        for index in range(0, len(agentList)):
            # if not index_bankrupted.__contains__(index):
            if agentList[index].bank >= 0:
                new_agentList.append(mimic(index))

        """update agentList"""
        # index_new_agentList = 0
        # for index in range(len(agentList)):
        #     if index_new_agentList >= len(new_agentList):
        #         break
        #     if not index_bankrupted.__contains__(index):
        #         agentList[index] = new_agentList[index_new_agentList]
        #         index_new_agentList += 1


        """Reproduce"""
        reproduced_agents = []
        if len(index_bankrupted) > 0:
            """split new agents into 2 groups"""
            sum_bank_left = 0.0
            sum_bank_right = 0.0
            target_left_group = []
            target_right_group = []

            """prepare params"""
            for newAgent in new_agentList:
                if index_left.__contains__(newAgent.ID):
                    sum_bank_left += newAgent.bank
                    target_left_group.append(newAgent)
                else:
                    sum_bank_right += newAgent.bank
                    target_right_group.append(newAgent)

            """use algorithm to randomly pick an agent for each bankrupted agent"""
            for index in index_bankrupted:
                if index_left.__contains__(index):
                    sum_target_group = sum_bank_left
                    group_target = target_left_group[:]
                else:
                    sum_target_group = sum_bank_right
                    group_target = target_right_group[:]

                # add extra bridges
                neighbourIndicesList = getNeighbourIndicesList(index)
                for neighbourIndex in neighbourIndicesList:
                    if (not group_target.__contains__(neighbourIndex)) and (agentList[neighbourIndex].bank > 0):
                        sum_target_group += agentList[neighbourIndex].bank
                        group_target.append(agentList[neighbourIndex])

                target_index = -1
                random_num = random.random()
                index_new_AgentList = 0.0
                for i in range(0, len(group_target)):
                    rate = group_target[i].bank / sum_target_group
                    index_new_AgentList += rate
                    if index_new_AgentList >= random_num:
                        # chosen
                        target_index = i
                        break

                target_agent = group_target[target_index]
                reproduced_agent = Agent(index, p * target_agent.bank, target_agent.theta, target_agent.Lambda)
                reproduced_agents.append(reproduced_agent)
                agentList[group_target[target_index].ID].bank *= (1 - p)


        """insert new agents"""
        index_new_agents = 0
        index_reproduced_agents = 0
        for i in range(0, len(agentList)):
            if agentList[i].bank < 0:
                agentList[i] = reproduced_agents[index_reproduced_agents]
                index_reproduced_agents += 1
            else:
                agentList[i] = new_agentList[index_new_agents]
                index_new_agents += 1

    # print("Result of Round", count_round)
    # print("Bankrupted:", len(index_bankrupted))
    # printAgentList()
    # print("---------------------------------------")
    return
def openlog():
    global file_log
    filename_log = "log.txt"
    file_log = open(filename_log, "w", encoding='utf-8')    
def openFiles():
    global file_theta
    global file_lambda
    global file_bank
    global file_group
    # Result output to txts
    filename_theta = "theta.txt"
    filename_lambda = "lambda.txt"
    filename_bank = "bank.txt"
    filename_group = "group.txt"
    file_theta = open(filename_theta, "w", encoding='utf-8')
    file_lambda = open(filename_lambda, "w", encoding='utf-8')
    file_bank = open(filename_bank, "w", encoding='utf-8')
    file_group = open(filename_group, "w", encoding='utf-8') 
def closeFiles():
    file_log.close()
    file_theta.close()
    file_lambda.close()
    file_bank.close()
    file_group.close()
def convergeTest():
    i=0
    while i <len(agentList)-1:
        a = agentList[i]
        b = agentList[i+1]
        if abs(a.theta-b.theta) > 0.01:
            global stop
            stop = True
            ##print("theta converges to two or more values")
            return
        else:
            i+=1
    ##print("theta converges to single value")
    stop = False
    return

# Start of the program
print("Program started")

inputParams()
makeDir()
openFiles()
repCount=1
while repCount<=1:
    restoreParams()
    openlog()
    initAgents()
    getVertices()
    file_log.flush()
    while sbStillGotMoney and count_round <= 2400:
        play()
        count_round += 1
        if count_round%20 == 0:
            print(count_round)
            for agent in agentList:
                file_bank.write(str(agent.bank))
                file_bank.write("\n")
                file_bank.flush()
                file_theta.write(str(agent.theta))
                file_theta.write("\n")
                file_theta.flush()
                file_lambda.write(str(agent.Lambda))
                file_lambda.write("\n")
                file_lambda.flush()
            ii=0
            while ii<25:
                file_group.write("1")
                file_group.write("\n")
                file_group.flush
                ii +=1
            ij=0
            while ij<25:
                file_group.write("2")
                file_group.write("\n")
                file_group.flush
                ij +=1
    repCount +=1
closeFiles()
print("Program ended")
