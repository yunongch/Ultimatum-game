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
agentAmount = 0
bank = 0.0
k = 0.0
p = 0.25
agentList = []
sbStillGotMoney = True


# methods
def inputParams():
    global agentAmount
    global bank
    global k

    while True:
        input_temp = input("plz input amount of agents:")
        try:
            input_temp = int(input_temp)
            if input_temp % 2 != 0:
                print("An even integer expected")
                continue
            agentAmount = input_temp
            break
        except:
            print("An integer expected")
    while True:
        input_temp = input("plz input bank:")
        try:
            input_temp = float(input_temp)
            if input_temp <= 0:
                print("Invalid Bank")
                continue
            bank = input_temp
            break
        except:
            print("A float expected")
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
    for index in range(0, agentAmount):
        agentList.append(Agent(index, bank, random.random(), random.random()))
    return

def printAgentList():
    for agent in agentList:
        agent.printSelf()
    return

def play():
    random.shuffle(agentList)
    index_bankrupted = []
    for index in range(len(agentList)):
        if index % 2 != 0:
            continue
        if random.random() < random.random():
            offeror = agentList[index]
            responder = agentList[index+1]
        else:
            responder = agentList[index]
            offeror = agentList[index + 1]

        if offeror.theta >= responder.Lambda:
            offeror.bank += (1 - offeror.theta) * 10
            responder.bank += offeror.theta * 10;

        """the cost of living"""
        offeror.bank -= k * 10
        responder.bank -= k * 10

        """log who's bankrupted"""
        if agentList[index].bank < 0:
            index_bankrupted.append(index)
        if agentList[index + 1].bank < 0:
            index_bankrupted.append(index + 1)

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

        reproduced_agents = []
        """Reproduce"""
        if len(index_bankrupted) > 0:
            """TODO randomly pick an agent for each bankrupted agent"""
            for index in range(len(index_bankrupted)):
                target_index = math.floor(random.random() * len(new_agentList))
                target_agent = new_agentList[target_index]
                id_bankrupted = agentList[index_bankrupted[index]].ID
                reproduced_agents.append(Agent(id_bankrupted, p * target_agent.bank, target_agent.theta, target_agent.Lambda))
                new_agentList[target_index].bank *= 1 - p

        new_agentList.extend(reproduced_agents)
        agentList.clear()
        agentList.extend(new_agentList)

    print("Result of Round", round_count)
    print("Bankrupted:", len(index_bankrupted))
    printAgentList()
    print("---------------------------------------")
    return

def mimic(index):
    """the agent needs to mimic"""
    agent_mimic = agentList[index]

    agents_wealthier = []
    sum_bank = 0.0
    for agent in agentList:
        if agent.bank > agent_mimic.bank:
            agents_wealthier.append(agent)
            sum_bank += agent.bank

    """Algorithm"""
    newTheta = agent_mimic.theta
    newLambda = agent_mimic.Lambda
    denominator = sum_bank - agent_mimic.bank * len(agents_wealthier)
    for agent in agents_wealthier:
        numerator_theta = (agent.bank - agent_mimic.bank) * (agent.theta - agent_mimic.theta)
        newTheta += numerator_theta / denominator
        numerator_lambda = (agent.bank - agent_mimic.bank) * (agent.Lambda - agent_mimic.Lambda);
        newLambda += numerator_lambda / denominator;
    return Agent(agent_mimic.ID, agent_mimic.bank, newTheta, newLambda)



# Start of the program
print("Program started")

inputParams()
initAgents()
print("------------Original Data-----------")
printAgentList()
print("------------------------------------")

round_count = 1
while sbStillGotMoney and round_count <= 300:
    play()
    round_count += 1

print("Program ended")
