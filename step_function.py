from itertools import count
import random
import networkx as nx
import math
import attribute
import numpy as np
import policy
import copy


def Hcadoption(model):
    # 40% of the neighborhoods in Qingshan district (index 5) will adopt district heating in step 5 (according to official documents)
    # and households in district 4 and 5 can choose adopt district heating or not.
    nei_selected = random.sample([i for i in range(10)], 4)
    for i in nei_selected:
        select_nei = model.agent_list_DN[5][i]
        for j in select_nei:
            agent_j = model.agent_list[j]
            agent_j.app_ac_package = 3
            model.disHeatingCount += 1
            model.disHeatingCount_dis[5] += 1


def negInfoExchange(agent, model, productIndex):
    ph_SN = model.ph_SN
    ol_SN = model.ol_SN
    agentID = agent.unique_id
    agent_Phy_neighbour = list(ph_SN.adj[agentID])
    if len(agent_Phy_neighbour) >= 1:
        listPhyInfoChange = random.sample(agent_Phy_neighbour, 1)
        for agent_i_ID in listPhyInfoChange:
            agent_i = model.agent_list[agent_i_ID]
            if agent_i.neg_info[0] == -1:
                agent_i.neg_info[0] = productIndex
                agent_i.neg_info[1] = 1
    Online_neighbour = list(ol_SN.adj[agentID])
    agent_num = round(0.05 * len(Online_neighbour))
    if agent_num >= 1:
        listOnlineInfoChange = random.sample(Online_neighbour, agent_num)
        for agent_j_id in listOnlineInfoChange:
            agent_j = model.agent_list[agent_j_id]
            if agent_j.neg_info[0] == -1:
                agent_j.neg_info[0] = productIndex
                agent_j.neg_info[1] = 2


def phsicalNetwork_RA(model):
    # self attitude: xi1, xi2, ui1, ui2 ( opinion xi and unceratinty ui if for the agent)
    # interation agent: xj1, xj2, uj1, uj2
    ph_SN = model.ph_SN
    for i in model.agent_list:
        agentID_i = i.unique_id
        xi1 = (i.att1 - 3) / 2
        xi2 = (i.att2 - 3) / 2
        i_neighbour = list(ph_SN.adj[agentID_i])
        # for more than one interaction
        agentID_j_list = None
        # if len(i_neighbour) > 1:
        #     agentID_j_list = random.sample(i_neighbour, 2)
        if len(i_neighbour) > 0:
            agentID_j_list = random.sample(i_neighbour, 1)
        if agentID_j_list != None:
            for agentID_j in agentID_j_list:
                j = model.agent_list[agentID_j]
                xj1 = (j.att1 - 3) / 2
                xj2 = (j.att2 - 3) / 2
                # att 1
                if xi1 != xj1:
                    ui1 = i.u1
                    uj1 = j.u1
                    h1 = min(xi1 + ui1, xj1 + uj1) - max(xi1 - ui1, xj1 - uj1)
                    # agent i
                    if h1 > uj1:
                        tep_xi1 = xi1 + 0.5 * (h1 / uj1 - 1) * (xj1 - xi1)
                        tep_ui1 = ui1 + 0.5 * (h1 / uj1 - 1) * (uj1 - ui1)
                        i.att1 = round(tep_xi1 * 2 + 3, 1)
                        i.u1 = tep_ui1
                    # agent j
                    if h1 > ui1:
                        tep_xj1 = xj1 + 0.5 * (h1 / ui1 - 1) * (xi1 - xj1)
                        tep_uj1 = uj1 + 0.5 * (h1 / ui1 - 1) * (ui1 - uj1)
                        j.att1 = round(tep_xj1 * 2 + 3, 1)
                        j.u1 = tep_uj1
                # att 2
                if xi2 != xj2:
                    ui2 = i.u2
                    uj2 = j.u2
                    h2 = min(xi2 + ui2, xj2 + uj2) - max(xi2 - ui2, xj2 - uj2)
                    # agent i
                    if h2 > uj2:
                        # att2
                        tep_xi2 = xi2 + 0.5 * (h2 / uj2 - 1) * (xj2 - xi2)
                        tep_ui2 = ui2 + 0.5 * (h2 / uj2 - 1) * (uj2 - ui2)
                        i.att2 = round(tep_xi2 * 2 + 3, 1)
                        i.u2 = tep_ui2
                    # agent j
                    if h2 > ui2:
                        # att2
                        tep_xj2 = xj2 + 0.5 * (h2 / ui2 - 1) * (xi2 - xj2)
                        tep_uj2 = uj2 + 0.5 * (h2 / ui2 - 1) * (ui2 - uj2)
                        j.att2 = round(tep_xj2 * 2 + 3, 1)
                        j.u2 = tep_uj2


def onlineNetwork_RA(model):
    # self attitude: xi1, xi2, ui1, ui2 ( opinion xi and unceratinty ui if for the agent)
    # interation agent: xj1, xj2, uj1, uj2
    ol_SN = model.ol_SN
    for i in model.agent_list:
        agentID_i = i.unique_id
        i_neighbour = list(ol_SN.adj[agentID_i])
        agent_num = int(
            0.05 * len(i_neighbour)
        )  # only influence 5% of the agents in online social netwrok
        if agent_num >= 1:
            xi1 = (i.att1 - 3) / 2
            xi2 = (i.att2 - 3) / 2
            listOfInteractAgent = random.choices(
                i_neighbour, k=agent_num
            )  # get the list of agent influenced by the rich agent
            for j in listOfInteractAgent:
                agentID_j = random.choice(i_neighbour)
                j = model.agent_list[agentID_j]
                xj1 = (j.att1 - 3) / 2
                xj2 = (j.att2 - 3) / 2
                # the inluence is oneway, so only agentj will be influenced
                # att1
                ui1 = i.u1
                uj1 = j.u1
                h1 = min(xi1 + ui1, xj1 + uj1) - max(xi1 - ui1, xj1 - uj1)
                if h1 > ui1:
                    tep_xj1 = xj1 + 0.5 * (h1 / ui1 - 1) * (xi1 - xj1)
                    tep_uj1 = uj1 + 0.5 * (h1 / ui1 - 1) * (ui1 - uj1)
                    j.att1 = round(tep_xj1 * 2 + 3, 1)
                    j.u1 = tep_uj1
                # att2
                ui2 = i.u2
                uj2 = j.u2
                h2 = min(xi2 + ui2, xj2 + uj2) - max(xi2 - ui2, xj2 - uj2)
                if h2 > ui2:
                    tep_xj2 = xj2 + 0.5 * (h2 / ui2 - 1) * (xi2 - xj2)
                    tep_uj2 = uj2 + 0.5 * (h2 / ui2 - 1) * (ui2 - uj2)
                    j.att2 = round(tep_xj2 * 2 + 3, 1)
                    j.u2 = tep_uj2


def RA2_model(model):
    if model.proType == 0:
        if model.policyList[3] == 0:
            phsicalNetwork_RA(model)
            onlineNetwork_RA(model)
        elif model.policyList[3] == 1:
            onlineNetwork_RA(model)
        elif model.policyList[3] == 2:
            phsicalNetwork_RA(model)
    else:
        phsicalNetwork_RA(model)
        onlineNetwork_RA(model)


def GetGroupPara(product, group):
    if product == 0:
        a = attribute.coefficients[product + group - 1]
    if product == 1:
        a = attribute.coefficients[product + group + 1]
    if product == 2:
        a = attribute.coefficients[product + group + 3]
    return a


def getFullCode(model, agent):
    product = model.proType
    policy_list = model.policyList
    # policy array: 0__energy lable, 1__subsidy, 2__popularity
    if product == 0:
        n = attribute.app_code2
        # n1 = attribute.getEnergyLabel(n, policy_list[0], P_poolLenth)
        n2 = policy.getAppSubsidy(n, policy_list[1])
        n3 = policy.getAppNeg2(n2, agent.neg_info)
        n4 = policy.getAppPopularity(n3, policy_list[2], model.stepCount)
        full_code = n4
    if product == 1:
        n = attribute.hc_code_full
        # full_code = policy.getHcSubsidy(n, policy_list[1])
        n_recom = policy.getHCrecom(n, agent.recom_info)
        n_pop = policy.getHCpop(n_recom, policy_list[2], model.stepCount)
        full_code = n_pop
    return full_code


def chooseProduct(agent, product, policyList, model):  #
    groupPara = GetGroupPara(product, agent.group)
    para = np.array(groupPara)
    fullcode = getFullCode(model, agent)
    b = []
    # produt pool limitation for heating & cooling simulation
    if product == 1:
        # 40% of the neighborhoods in Qingshan district (index 5) will adopt district heating in step 5 (according to official documents)
        # and households in district 4 and 5 can choose adopt district heating or not.
        if policyList[-2] == 0:
            dis = agent.district_id
            if (dis == 4) or (dis == 5):
                if model.stepCount < 5:
                    b = copy.deepcopy(fullcode[:17])
                else:
                    b = copy.deepcopy(fullcode)
            else:
                b = copy.deepcopy(fullcode[:17])
        elif policyList[-2] == 1:
            dis = agent.district_id
            if model.stepCount < 5:
                b = copy.deepcopy(fullcode[:17])
            else:
                b = copy.deepcopy(fullcode)
        elif policyList[-2] == 2:  # dis_heat0
            b = copy.deepcopy(fullcode)
        elif policyList[-2] == 3:  # dis_heat10
            if model.stepCount < 10:
                b = copy.deepcopy(fullcode[:17])
            else:
                b = copy.deepcopy(fullcode)
        if agent.app_ac_package == 3:
            b = copy.deepcopy(fullcode[18:])
    else:
        b = copy.deepcopy(fullcode)
    # product utility and choose probability calculation
    c = []
    k = [*range(0, len(b), 1)]
    for i in b:
        d = np.dot(para, i)
        c.append(d)
    sumExp_i = 0
    for i in c:
        sumExp_i += math.exp(i)
    p = []
    for i in c:
        p.append(math.exp(i) / sumExp_i)
    prodChoice = random.choices(k, p)[0]

    # after choosing, change the statists for simulaiton results
    # appliances
    if product == 0:
        prob = random.choice([True, False])
        if prob == True:
            negInfoExchange(agent, model, prodChoice)
        if attribute.app_code2[prodChoice][0] == 1:
            agent.app_ac_package = 1
        elif attribute.app_code2[prodChoice][1] == 1:
            agent.app_ac_package = 2
        else:
            agent.app_ac_package = 3
        # replacing through minus and add
        model.label_count[agent.app_ac_energyLabel - 1] -= 1
        model.label_count_dis[agent.district_id][agent.app_ac_energyLabel - 1] -= 1
        if attribute.app_code2[prodChoice][10] == 1:
            agent.app_ac_energyLabel = 1
            model.label_count[0] += 1
            model.label_count_dis[agent.district_id][0] += 1
        elif attribute.app_code2[prodChoice][11] == 1:
            agent.app_ac_energyLabel = 2
            model.label_count[1] += 1
            model.label_count_dis[agent.district_id][1] += 1
        else:
            agent.app_ac_energyLabel = 3
            model.label_count[2] += 1
            model.label_count_dis[agent.district_id][2] += 1

    # heating & cooling
    if product == 1:
        if agent.app_ac_package != 3:
            if attribute.hc_code_full[prodChoice][1] == 1:
                agent.app_ac_package = 1
            elif attribute.hc_code_full[prodChoice][2] == 1:
                agent.app_ac_package = 2
            else:
                agent.app_ac_package = 3
                model.disHeatingCount += 1
                model.disHeatingCount_dis[agent.district_id] += 1
        model.label_count[agent.app_ac_energyLabel - 1] -= 1
        model.label_count_dis[agent.district_id][agent.app_ac_energyLabel - 1] -= 1
        if attribute.hc_code_full[prodChoice][10] == 1:
            agent.app_ac_energyLabel = 1
            model.label_count[0] += 1
            model.label_count_dis[agent.district_id][0] += 1
        elif attribute.hc_code_full[prodChoice][11] == 1:
            agent.app_ac_energyLabel = 2
            model.label_count[1] += 1
            model.label_count_dis[agent.district_id][1] += 1
        else:
            agent.app_ac_energyLabel = 3
            model.label_count[2] += 1
            model.label_count_dis[agent.district_id][2] += 1
    return prodChoice


def NeiAdoptionRateChange(agent, fullCode):
    adoptionNei = agent.NeiAdoption
    dis = agent.district_id
    nei = agent.neighborhood_id
    totalBuldingNei = len(agent.model.blByNei[dis][nei]) - 1
    adoptionRateNei = len(adoptionNei) / totalBuldingNei
    fullCodeIndividual = copy.deepcopy(fullCode)
    if adoptionRateNei < 0.35:
        for i in fullCodeIndividual:
            i[32] = 1
            i[33] = 0
            i[34] = 0
    elif adoptionRateNei >= 0.35 and adoptionRateNei < 0.75:
        for i in fullCodeIndividual:
            i[32] = 0
            i[33] = 1
            i[34] = 0
    else:
        for i in fullCodeIndividual:
            i[32] = 0
            i[33] = 0
            i[34] = 1
    return fullCodeIndividual


def recommendationChange(agent, fullCode):
    if agent.model.proType == 2:
        adoptionSetNei = agent.NeiAdoption
        adoptionSetSn = agent.SnAdoption
        fullCodeIndividual = copy.deepcopy(fullCode)
        for i in range(len(attribute.PV_code)):
            # change code for community comment
            if i in adoptionSetSn:
                if random.choice([True, False]):
                    fullCodeIndividual[i][25] = 0
                    fullCodeIndividual[i][26] = 1
            if i in adoptionSetNei:
                if random.choice([True, False]):
                    fullCodeIndividual[i][25] = 0
                    fullCodeIndividual[i][27] = 1
    return fullCodeIndividual


def getPvFullCode2(policy_list):  # for new decision functions
    n = attribute.PV_code
    n1 = policy.getPvBattery(n, policy_list[0])
    n2 = policy.getPvSub(n1)
    n3 = policy.getPvEnerService(n2, policy_list[0])
    n4 = policy.getPvAgreeRate(n3, 0)
    n5 = policy.getPvReconmantation(n4, 0)
    n6 = policy.getPvNeg(n5, 0)
    fullCode = policy.getPvInstallRate(n6, 0)
    return fullCode


# ________________________________________________________________________________________________________________________________________________________________________________
# PV


def getPvFullCode(agent, policy_list):
    if agent.decision_strategy == 1:
        n = attribute.PV_code
        n1 = policy.getPvBattery(n, policy_list[0])
        n2 = policy.getPvSub(n1, policy_list[0])
        n3 = policy.getPvEnerService(n2, policy_list[0])
        n4 = policy.getPvAgreeRate(n3, 0)
        n5 = policy.getPvReconmantation(n4, 0)
        n6 = policy.getPvNeg(n5, 0)
        n7 = policy.getPvInstallRate(n6, 0)
        fullCode = recommendationChange(agent, n7)
    if agent.decision_strategy == 3:
        adoptionList = np.concatenate((agent.NeiAdoption, agent.SnAdoption), axis=None)
        proPool = copy.deepcopy(attribute.PV_code)
        len_code = len(proPool[0])
        for i in range(11):
            if i not in adoptionList:
                proPool[i] = [0] * len_code
        proPool[0][0] = 1
        n1 = policy.getPvBattery(proPool, policy_list[0])
        n2 = policy.getPvSub(n1, policy_list[0])
        n3 = policy.getPvEnerService(n2, policy_list[0])
        n4 = policy.getPvAgreeRate(n3, 0)
        n5 = policy.getPvReconmantation(n4, 0)
        n6 = policy.getPvNeg(n5, 0)
        n7 = policy.getPvInstallRate(n6, 0)
        fullCode = recommendationChange(agent, n7)
    return fullCode


def getDeliAdoption(agent):
    indivialDecision = [0, []]
    groupPara = GetGroupPara(agent.model.proType, agent.group)
    para = np.array(groupPara)
    fullcode = getPvFullCode(agent, agent.model.policyList)
    exp = []
    sum = 0
    for pr_code in fullcode:
        d = np.dot(para, pr_code)
        exp_m = math.exp(d)
        exp.append(exp_m)
        sum += exp_m
    prob = [round(i / sum, 4) for i in exp]
    indivialDecision[1] = prob
    return indivialDecision


def getSoComAdoption(agent):
    indivialDecision = [0, []]
    indivialDecision[1] = [0] * 11
    proList = [i for i in range(11)]
    fullcode = getPvFullCode(agent, agent.model.policyList)
    groupPara = GetGroupPara(agent.model.proType, agent.group)
    para = np.array(groupPara)
    exp = []
    sum = 0
    adoptionList = np.concatenate((agent.NeiAdoption, agent.SnAdoption), axis=None)
    choice_v = list(set(adoptionList))
    for pr_code in fullcode:
        if fullcode.index(pr_code) in choice_v:
            d = np.dot(para, pr_code)
            exp_m = math.exp(d)
        else:
            exp_m = 0
        exp.append(exp_m)
        sum += exp_m
    prob = [round(i / sum, 4) for i in exp]
    indivialDecision[1] = prob
    return indivialDecision


def getImiAdoption(agent):
    indivialDecision = [0, []]
    adoptionList = np.concatenate((agent.NeiAdoption, agent.SnAdoption), axis=None)
    choice_v = list(set(adoptionList))
    choice_d = []
    for i in choice_v:
        choice_d.append(np.count_nonzero(adoptionList == i))
    sum_count = sum(choice_d)
    indivialDecision[1] = [0] * 11
    for i in range(len(choice_v)):
        product = int(choice_v[i])
        indivialDecision[1][product] = choice_d[i] / sum_count
    return indivialDecision


def pvDecisionIndividual(agent):
    indivialDecision = [0, []]
    nei = agent.NeiAdoption
    SN = agent.SnAdoption
    neiAdp = np.count_nonzero(nei != 0)
    snAdp = np.count_nonzero(SN != 0)
    ratio = 0
    if snAdp > 0:
        ratio = 1
    else:
        ratio_original = neiAdp / len(nei)
        if agent.info_campaign == 0:
            ratio = ratio_original
        elif agent.info_campaign == 1:
            ratio = ratio_original + 0.05
        elif agent.info_campaign == 2:
            ratio = ratio_original + 0.10
        elif agent.info_campaign == 3:
            ratio = ratio_original + 0.05
        if ratio > 1:
            ratio = 1
    value = [True, False]
    dis = [ratio, 1 - ratio]
    a = random.choices(value, dis)[0]
    if a == False:
        indivialDecision[0] = 0
        indivialDecision[1] = [1] + [0] * 10
    elif a == True:
        if agent.decision_strategy == 0:  # repetition
            indivialDecision[0] = 0
            indivialDecision[1] = [1] + [0] * 10
        elif agent.decision_strategy == 1:  # Deliberation
            indivialDecision = getDeliAdoption(agent)
        elif agent.decision_strategy == 2:  # Imitation
            indivialDecision = getImiAdoption(agent)
        else:  # social comparison
            indivialDecision = getSoComAdoption(agent)
    return indivialDecision


def PvGroupAdoption(model):
    buildingList = model.buildingList
    for i in buildingList:
        agent0 = model.agent_list[i[0]]
        if agent0.PV_adoption == 0:
            buildingProb = [0] * 11
            for j in i:
                agentj = model.agent_list[j]
                indivialDecision = pvDecisionIndividual(agentj)
                j_prob = indivialDecision[1]
                for m in range(len(buildingProb)):
                    buildingProb[m] = buildingProb[m] + j_prob[m]

            ##### group agreement factor
            if model.policyList[2] == 0:
                agreeRate = 0.25  # agreement rate 75%
            elif model.policyList[2] == 1:
                agreeRate = 0.35  # agreement Rate 65%
            elif model.policyList[2] == 2:
                agreeRate = 0.45  # agreement rate 55%
            elif model.policyList[2] == 3:
                agreeRate = 0.4  # agreement rate 60%
            elif model.policyList[2] == 4:
                agreeRate = 0.5  # agreement rate  50%
            if buildingProb[0] / len(i) <= agreeRate:
                buildingProb[0] = 0
                pvmax = max(buildingProb) / sum(buildingProb)
                if pvmax > 0:
                    pro_list = [pro_index for pro_index in range(11)]
                    pro_choice = random.choices(pro_list, buildingProb)[0]
                    pro_choice = buildingProb.index(max(buildingProb))
                    for j in i:
                        agentj = model.agent_list[j]
                        agentj.PV_adoption = pro_choice
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
                                            agent_fri.SnAdoption[k] = pro_choice
                                            break
                    model.totaladoption += 1
                    model.adoptioncount[pro_choice] += 1
                    dis = agent0.district_id
                    nei = agent0.neighborhood_id
                    model.adoption_dis_count[dis][pro_choice] += 1
                    model.total_adoption_dis[dis] += 1
                    buildingListDisNei = model.blByNei[dis][nei]
                    BuiListDisNeiWithout_i = [
                        building for building in buildingListDisNei if building != i
                    ]
                    for building in BuiListDisNeiWithout_i:
                        for agent_id in building:
                            agent = model.agent_list[agent_id]
                            if agent.PV_adoption == 0:
                                for k in range(len(agent.NeiAdoption)):
                                    if agent.NeiAdoption[k] != 0:
                                        pass
                                    elif agent.NeiAdoption[k] == 0:
                                        agent.NeiAdoption[k] = pro_choice
                                        break


# ________________________________________________________________________________________________________________________________________________________________________________
def modelGetProduct(model):
    if model.proType == 0:
        for i in model.agent_list:
            if i.appy == i.appEX:
                m = chooseProduct(i, model.proType, model.policyList, model)
                model.adoptioncount[m] += 1
                model.totaladoption += 1
                dis_num = i.district_id
                model.adoption_dis_count[dis_num][m] += 1
                model.total_adoption_dis[dis_num] += 1
                i.appy = 0
    elif model.proType == 1:
        for i in model.agent_list:
            if i.hcy == i.hcEX:
                m = chooseProduct(i, model.proType, model.policyList, model)
                model.adoptioncount[m] += 1
                model.totaladoption += 1
                dis_num = i.district_id
                model.adoption_dis_count[dis_num][m] += 1
                model.total_adoption_dis[dis_num] += 1
                i.hcy = 0
    else:
        PvGroupAdoption(model)
