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
bank_up_threshold = 0.0
bank_down_threshold = 0.0
k = 0.0#life cost
p = 0.25#proportion shared for offsprings
sbStillGotMoney = True
agentList = []
converge = False

# methods
input_temp = input("plz input k:")
try:
    input_temp = float(input_temp)
    k = input_temp
except:
    print("A float expected")

def initAgents():
    for index in range(0, 150):
        agentList.append(Agent(index,1, random.random(), random.random()))
    return

def printAgentList():
    for agent in agentList:
        agent.printSelf()
    return

def convergeTest():
    i=0
    while i <len(agentList)-1:
        a = agentList[i]
        b = agentList[i+1]
        if abs(a.theta-b.theta) > 0.001:
            global converge
            converge = False
            ##print("theta converges to two or more values")
            return
        else:
            i+=1
    ##print("theta converges to single value")
    converge = True
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
            offeror.bank += (1 - offeror.theta)
            responder.bank += offeror.theta;

        """the cost of living"""
        offeror.bank -= k
        responder.bank -= k

        """log who's bankrupted"""
        if agentList[index].bank < 0:
            index_bankrupted.append(index)
        if agentList[index + 1].bank < 0:
            index_bankrupted.append(index + 1)

    """whether all agents are bankrupted"""
    if len(index_bankrupted) == len(agentList):
        global sbStillGotMoney
        sbStillGotMoney = False
        ##print("population collapse in round",round_count)
        for agent in agentList:
            agent.bank += 1.5#give each player some money to keep the game going
    else:
        """agents mimic"""
        new_agentList = []
        for index in range(len(agentList)):
            if not index_bankrupted.__contains__(index):
                new_agentList.append(mimic(index))

        reproduced_agents = []
        """Reproduce"""
        if len(index_bankrupted) > 0:
            """use algorithm to randomly pick an agent for each bankrupted agent"""
            sum_new_agentList = 0.0
            for a in new_agentList:
                sum_new_agentList += a.bank

            for index in range(len(index_bankrupted)):
                target_index = -1
                random_num = random.random()
                index_new_AgentList = 0.0
                for i in range(len(new_agentList)):
                    rate = new_agentList[i].bank / sum_new_agentList
                    index_new_AgentList += rate
                    if index_new_AgentList >= random_num:
                        # chosen
                        target_index = i
                        break;
                target_agent = new_agentList[target_index]
                id_bankrupted = agentList[index_bankrupted[index]].ID
                reproduced_agents.append(Agent(id_bankrupted, p * target_agent.bank, target_agent.theta, target_agent.Lambda))
                new_agentList[target_index].bank *= 1 - p

        new_agentList.extend(reproduced_agents)
        agentList.clear()
        agentList.extend(new_agentList)

    # print("Result of Round", round_count)
    # print("Bankrupted:", len(index_bankrupted))
    # printAgentList()
    # print("---------------------------------------")
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
        newTheta += 0.01*numerator_theta / denominator
        numerator_lambda = (agent.bank - agent_mimic.bank) * (agent.Lambda - agent_mimic.Lambda);
        newLambda += 0.01*numerator_lambda / denominator;
    return Agent(agent_mimic.ID, agent_mimic.bank, newTheta, newLambda)


file_theta = open("theta", "w", encoding='utf-8')
file_lambda = open("lambda", "w", encoding='utf-8')
# Start of the program
rep_count=1
while rep_count<=30:
    initAgents()
    round_count = 1
    converge = False
    print(rep_count)
    while converge != True and round_count<=900:
        play()
        #print(round_count,"the round")
        round_count += 1
        convergeTest()        
    for agent in agentList:
        file_theta.write(str(agent.theta))
        file_theta.write("\n")
        file_lambda.write(str(agent.Lambda))
        file_lambda.write("\n")
    rep_count +=1
    agentList = []
file_theta.close()
file_lambda.close()
print("Program ended")
