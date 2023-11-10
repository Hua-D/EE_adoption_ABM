import random
import attribute
import numpy as np
import copy


def AdAccessAndAge(age):
    p_age = 1.10 * np.exp(-np.exp(-(age + 1 - 25) / 4)) - np.exp(
        -np.exp(-(age - 25) / 4)
    )
    yes_np = [1, 0]
    yesNoDis = [p_age, 1 - p_age]
    accessAd = random.choices(yes_np, yesNoDis)[0]
    return accessAd


def chooseNei():
    choosenDisNei = []
    choosenNei = random.sample(range(76), 10)
    for i in choosenNei:
        if i < 17:
            choosenDisNei.append([0, i])
        elif i < 29:
            choosenDisNei.append([1, i - 17])
        elif i < 40:
            choosenDisNei.append([2, i - 29])
        elif i < 51:
            choosenDisNei.append([3, i - 40])
        elif i < 66:
            choosenDisNei.append([4, i - 51])
        else:
            choosenDisNei.append([5, i - 66])
    return choosenDisNei


def info_cam(model):
    impactLevel = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    impactDisNei = attribute.impactNeiDistribution
    impactDisAd = attribute.impactAdDistribution
    count = 0
    if model.proType <= 1:
        if model.policyList[-1] == 0:
            pass
        elif model.policyList[-1] == 1:  # Ad continuous
            if model.stepCount <= 9:
                count = 0
                for agent_i in model.agent_list:
                    AdAccess = AdAccessAndAge(agent_i.age)
                    if AdAccess == 1:
                        count += 1
                        if agent_i.att1 < 5:
                            attitudeChange1 = random.choices(impactLevel, impactDisAd)[
                                0
                            ]
                            agent_i.att1 = agent_i.att1 + attitudeChange1
                            if agent_i.att1 > 5:
                                agent_i.att1 = 5
                        if agent_i.att2 < 5:
                            attitudeChange2 = random.choices(impactLevel, impactDisAd)[
                                0
                            ]
                            agent_i.att2 = agent_i.att2 + attitudeChange2
                            if agent_i.att2 > 5:
                                agent_i.att2 = 5
                print("AD", count)
        elif model.policyList[-1] == 2:  # campaign in neighbourhoods continuous
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount <= 9:
                count = 0
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    for agentId_j in agentList_i:
                        access_v = [1, 0]
                        access_dis = [0.5, 0.5]
                        access = random.choices(access_v, access_dis)[0]
                        if access == 1:
                            count += 1
                            agent_j = model.agent_list[agentId_j]
                            if agent_j.att1 < 5:
                                attitudeChange1 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att1 = agent_j.att1 + attitudeChange1
                                if agent_j.att1 > 5:
                                    agent_j.att1 = 5
                            if agent_j.att2 < 5:
                                attitudeChange2 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att2 = agent_j.att2 + attitudeChange2
                                if agent_j.att2 > 5:
                                    agent_j.att2 = 5
                print("nei", count)
        elif model.policyList[-1] == 3:  # Ad every other step
            if model.stepCount % 2 == 0:
                for agent_i in model.agent_list:
                    AdAccess = AdAccessAndAge(agent_i.age)
                    if AdAccess == 1:
                        count += 1
                        if agent_i.att1 < 5:
                            attitudeChange1 = random.choices(impactLevel, impactDisAd)[
                                0
                            ]
                            agent_i.att1 = agent_i.att1 + attitudeChange1
                            if agent_i.att1 > 5:
                                agent_i.att1 = 5
                        if agent_i.att2 < 5:
                            attitudeChange2 = random.choices(impactLevel, impactDisAd)[
                                0
                            ]
                            agent_i.att2 = agent_i.att2 + attitudeChange2
                            if agent_i.att2 > 5:
                                agent_i.att2 = 5
        elif model.policyList[-1] == 4:  # campaign in neighbourhoods every other step
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount % 2 == 0:
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    for agentId_j in agentList_i:
                        access_v = [1, 0]
                        access_dis = [0.5, 0.5]
                        access = random.choices(access_v, access_dis)[0]
                        if access == 1:
                            count += 1
                            agent_j = model.agent_list[agentId_j]
                            if agent_j.att1 < 5:
                                attitudeChange1 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att1 = agent_j.att1 + attitudeChange1
                                if agent_j.att1 > 5:
                                    agent_j.att1 = 5
                            if agent_j.att2 < 5:
                                attitudeChange2 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att2 = agent_j.att2 + attitudeChange2
                                if agent_j.att2 > 5:
                                    agent_j.att2 = 5
        # stop neg info (label 1: 100%, label 2: 50%, label 3: 0)
        elif model.policyList[-1] == 5:
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount <= 9:
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    if model.proType == 0:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                count += 1
                                agent_j = model.agent_list[agentId_j]
                                if agent_j.neg_info[0] == (
                                    0 or 1 or 6 or 7 or 12 or 13
                                ):
                                    agent_j.neg_info[0] = -1
                                    agent_j.neg_info[1] = 0
                                elif agent_j.neg_info[0] == (
                                    2 or 3 or 8 or 9 or 14 or 15
                                ):
                                    agent_j.neg_info[0] = -1
                                    agent_j.neg_info[1] = 0
                    if model.proType == 1:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                agent_j = model.agent_list[agentId_j]
                                agent_j.recom_info = 1
                    if model.proType == 2:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.2, 0.8]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                agent_j = model.agent_list[agentId_j]
                                if agent_j.decision_strategy == 0:
                                    agent_j.decision_strategy = random.choice([1, 2, 3])
        elif model.policyList[-1] == 6:  # stop neg info and change attitude
            NeiList = chooseNei()  # 5 choosen neighbourhoods
            if model.stepCount <= 9:
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    if model.proType == 0:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                count += 1
                                agent_j = model.agent_list[agentId_j]
                                if agent_j.neg_info[0] == (
                                    0 or 1 or 6 or 7 or 12 or 13
                                ):
                                    agent_j.neg_info[0] = -1
                                    agent_j.neg_info[1] = 0
                                elif agent_j.neg_info[0] == (
                                    2 or 3 or 8 or 9 or 14 or 15
                                ):
                                    agent_j.neg_info[0] = -1
                                    agent_j.neg_info[1] = 0
                    if model.proType == 1:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                agent_j = model.agent_list[agentId_j]
                                agent_j.recom_info = 1
                    if model.proType == 2:
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.2, 0.8]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                agent_j = model.agent_list[agentId_j]
                                if agent_j.decision_strategy == 0:
                                    agent_j.decision_strategy = random.choice([1, 2, 3])
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    for agentId_j in agentList_i:
                        access_v = [1, 0]
                        access_dis = [0.5, 0.5]
                        access = random.choices(access_v, access_dis)[0]
                        if access == 1:
                            count += 1
                            agent_j = model.agent_list[agentId_j]
                            if agent_j.att1 < 5:
                                attitudeChange1 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att1 = agent_j.att1 + attitudeChange1
                                if agent_j.att1 > 5:
                                    agent_j.att1 = 5
                            if agent_j.att2 < 5:
                                attitudeChange2 = random.choices(
                                    impactLevel, impactDisNei
                                )[0]
                                agent_j.att2 = agent_j.att2 + attitudeChange2
                                if agent_j.att2 > 5:
                                    agent_j.att2 = 5
    else:
        if model.policyList[-1] == 0:
            pass
        elif model.policyList[-1] == 1:
            if model.stepCount <= 9:
                count = 0
                for agent_i in model.agent_list:
                    AdAccess = AdAccessAndAge(agent_i.age)
                    if AdAccess == 1:
                        count += 1
                        agent_i.info_campaign = 1

        elif model.policyList[-1] == 2:  # campaign in neighbourhoods continuous
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount <= 9:
                count = 0
                for neighbourhood in NeiList:
                    dis = neighbourhood[0]
                    nei = neighbourhood[1]
                    agentList_i = model.agent_list_DN[dis][nei]
                    for agentId_j in agentList_i:
                        access_v = [1, 0]
                        access_dis = [0.5, 0.5]
                        access = random.choices(access_v, access_dis)[0]
                        if access == 1:
                            count += 1
                            agent_j = model.agent_list[agentId_j]
                            agent_j.info_campaign = 2

        elif model.policyList[-1] == 3:  # Ad every other step
            if model.stepCount <= 18:
                if model.stepCount % 2 == 0:
                    for agent_i in model.agent_list:
                        AdAccess = AdAccessAndAge(agent_i.age)
                        if AdAccess == 1:
                            count += 1
                            agent_i.info_campaign = 1

        elif model.policyList[-1] == 4:  # campaign in neighbourhoods every other step
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount <= 18:
                if model.stepCount % 2 == 0:
                    for neighbourhood in NeiList:
                        dis = neighbourhood[0]
                        nei = neighbourhood[1]
                        agentList_i = model.agent_list_DN[dis][nei]
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                count += 1
                                agent_j = model.agent_list[agentId_j]
                                agent_j.info_campaign = 2

        elif model.policyList[-1] == 5:  # campaign in neighbourhoods every other step
            NeiList = chooseNei()  # 10 choosen neighbourhoods
            if model.stepCount <= 18:
                if model.stepCount % 2 == 0:
                    for neighbourhood in NeiList:
                        dis = neighbourhood[0]
                        nei = neighbourhood[1]
                        agentList_i = model.agent_list_DN[dis][nei]
                        for agentId_j in agentList_i:
                            access_v = [1, 0]
                            access_dis = [0.5, 0.5]
                            access = random.choices(access_v, access_dis)[0]
                            if access == 1:
                                count += 1
                                agent_j = model.agent_list[agentId_j]
                                agent_j.info_campaign = 3


# App policies
def getAppSubsidy(a, policyScenario):
    # subsidy arguement is different subsidy policy that need to be designed
    k = {1: [1, 0, 0], 2: [0, 1, 0], 3: [0, 0, 1]}  # 1: no subsudy; 3: highest subsidy
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            y[i] = a[i] + k[1]
    if policyScenario == 1:
        for i in range(len(a)):
            if a[i][10] == 1:
                y[i] = a[i] + k[2]
            else:
                y[i] = a[i] + k[1]
    if policyScenario == 2:
        for i in range(len(a)):
            if a[i][10] == 1:
                y[i] = a[i] + k[3]
            else:
                y[i] = a[i] + k[1]
    return y


def getAppNeg2(a, neg_info):
    # neg_info: the first parameter is infomation status,
    # the second parameter is the source of the information (1: physical connetions; 2: online connections)
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    y = [[]] * len(a)
    if neg_info[0] == -1:
        for i in range(len(a)):
            y[i] = a[i] + k[0]
            if len(y[i]) == 3:
                print("problem")
    else:
        for i in range(len(a)):
            if i == neg_info[0]:
                if neg_info[1] == 1:
                    y[i] = a[i] + k[1]
                if neg_info[1] == 2:
                    y[i] = a[i] + k[2]
            else:
                y[i] = a[i] + k[0]
            if len(y[i]) == 3:
                print("problem")
    return y


def getAppPopularity(a, policyScenario, stepcount):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            y[i] = a[i] + k[0]
    elif policyScenario == 1:
        for i in range(len(a)):
            if stepcount <= 9:
                if a[i][10] == 1:
                    popularList = [True, False]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    elif policyScenario == 2:
        for i in range(len(a)):
            if stepcount <= 4:
                if a[i][10] == 1:
                    popularList = [True, False]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    elif policyScenario == 3:
        for i in range(len(a)):
            if stepcount <= 9:
                if a[i][10] == 1:
                    popularList = [True, False, False, False, False]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    elif policyScenario == 4:
        for i in range(len(a)):
            if stepcount <= 30:
                if a[i][10] == 1:
                    popularList = [
                        True,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                    ]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    return y


# H&C policy
def getHcSubsidy(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            y[i] = a[i] + k[0]
    if policyScenario == 1:
        for i in range(len(a)):
            if a[i][10] == 1:
                y[i] = a[i] + k[2]
            else:
                y[i] = a[i] + k[1]
    if policyScenario == 2:
        for i in range(len(a)):
            if a[i][10] == 1:
                y[i] = a[i] + k[3]
            else:
                y[i] = a[i] + k[1]
    return y


def getHCrecom(a, recom_info):
    k = {1: [1, 0, 0, 0], 2: [0, 1, 0, 0], 3: [0, 0, 1, 0], 4: [0, 0, 0, 1]}
    y = [[]] * len(a)
    if recom_info == 0:
        for i in range(len(a)):
            y[i] = a[i] + k[1]
    if recom_info == 0:
        for i in range(len(a)):
            if y[i][3] == 1:
                y[i] = a[i] + k[2]
            else:
                y[i] = a[i] + k[1]
    return y


def getHCpop(a, policyScenario, stepcount):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            y[i] = a[i] + k[0]
    if policyScenario == 1:
        for i in range(len(a)):
            if stepcount <= 4:
                if a[i][10] == 1:
                    popularList = [True, False]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    elif policyScenario == 4:
        for i in range(len(a)):
            if stepcount <= 30:
                if a[i][10] == 1:
                    popularList = [
                        True,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                    ]
                    pop = random.choice(popularList)
                    if pop == True:
                        y[i] = a[i] + k[2]
                    else:
                        y[i] = a[i] + k[0]
                else:
                    y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k[0]
    return y


def HcDistrcit(model):
    dis_Nei = []
    if model.policyList[-2] == 0:
        choosenNei = random.sample(range(76), 10)
        for i in choosenNei:
            if i < 17:
                dis_Nei.append([0, i])
            elif i < 29:
                dis_Nei.append([1, i - 17])
            elif i < 40:
                dis_Nei.append([2, i - 29])
            elif i < 51:
                dis_Nei.append([3, i - 40])
            elif i < 66:
                dis_Nei.append([4, i - 51])
            else:
                dis_Nei.append([5, i - 66])
    return dis_Nei


# PV policy (7)
def getPvBattery(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            # the do not adopt choice
            else:
                y[i] = a[i] + [0, 0, 0]
    return y


def getPvSub(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    if policyScenario == 1:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[1]
            else:
                y[i] = a[i] + k0
    if policyScenario == 2:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[2]
            else:
                y[i] = a[i] + k0
    return y


def getPvEnerService(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    if policyScenario == 1:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                serviceCost = random.choice([0, 20, 40])
                if serviceCost == 20:
                    y[i] = a[i] + k[1]
                else:
                    y[i] = a[i] + k[2]
    return y


def getPvAgreeRate(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    return y


def getPvReconmantation(a, policyScenario):
    k = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    k0 = [0, 0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range((len(a))):
            if a[i][0] == 1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    return y


def getPvNeg(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    return y


def getPvInstallRate(a, policyScenario):
    k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k0 = [0, 0, 0]
    y = [[]] * len(a)
    if policyScenario == 0:
        for i in range(len(a)):
            if a[i][0] == -1:
                y[i] = a[i] + k[0]
            else:
                y[i] = a[i] + k0
    return y


def DemoProjectPV(policyScenario, model, buildingWithoutPVList):
    productpool = [i for i in range(1, 11)]
    buildingChoosen = []
    if policyScenario == 1:  # 100 Pilot project in random area
        buildingChoosen = random.sample(buildingWithoutPVList, 358)
    if policyScenario == 2:
        buildingChoosen = random.sample(buildingWithoutPVList, 716)
    if policyScenario == 3:
        district_pop = []
        for i in model.agent_list_DN:
            m = [len(j) for j in i]
            k = sum(m)
            district_pop.append(k)
        maxPop = max(district_pop)
        maxPopDis = district_pop.index(maxPop)
        choosenDis_full = copy.deepcopy(
            model.blbydis[maxPopDis]
        )  # including buildings with or without PV
        choosenDis = []
        for i in choosenDis_full:  # removing buildings with PV from the list
            houseNumber_i0 = i[0]
            agent_i0 = model.agent_list[houseNumber_i0]
            if agent_i0.PV_adoption == 0:
                choosenDis.append(i)
        buildingChoosen = random.sample(choosenDis, 716)
    # print("buildingChoosen lenth", len(buildingChoosen))
    for i in buildingChoosen:
        agenti0 = model.agent_list[i[0]]
        product = random.choice(productpool)
        for j in i:
            agentj = model.agent_list[j]
            agentj.PV_adoption = product
            if agentj.num_connections > 0:
                SN = model.ph_SN
                friends = list(SN.adj[j])
                for fri in friends:
                    agent_fri = model.agent_list[fri]
                    if agent_fri.PV_adoption == 0:
                        for k in range(len(agent_fri.SnAdoption)):
                            if agent_fri.SnAdoption[k] != 0:
                                pass
                            elif agent_fri.SnAdoption[k] == 0:
                                agent_fri.SnAdoption[k] = product
                                break
        model.totaladoption += 1
        model.adoptioncount[product] += 1
        dis = agenti0.district_id
        model.adoption_dis_count[dis][product] += 1
        model.total_adoption_dis[dis] += 1
        BuiListDisNeiWithout_i = [
            building for building in buildingChoosen if building != i
        ]
        for building in BuiListDisNeiWithout_i:
            # print('building',building)
            for agent_id in building:
                # print(agent_id)
                agent = model.agent_list[agent_id]
                if agent.PV_adoption == 0:
                    for k in range(len(agent.NeiAdoption)):
                        if agent.NeiAdoption[k] != 0:
                            pass
                        elif agent.NeiAdoption[k] == 0:
                            agent.NeiAdoption[k] = product
                            break
