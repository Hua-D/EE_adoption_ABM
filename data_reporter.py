import attribute


def Dis0_AgentNum(model):
    return model.agentNumDis[0]


def Dis1_AgentNum(model):
    return model.agentNumDis[1]


def Dis2_AgentNum(model):
    return model.agentNumDis[2]


def Dis3_AgentNum(model):
    return model.agentNumDis[3]


def Dis4_AgentNum(model):
    return model.agentNumDis[4]


def Dis5_AgentNum(model):
    return model.agentNumDis[5]


def get_step(model):
    return model.stepCount


def getlabel_1_AdRate(model):
    totalhousehold = model.num_agents
    label1 = model.label_count[0]
    ad_rate = round(label1 / totalhousehold, 4)
    return ad_rate


def getlabel_2_AdRate(model):
    totalhousehold = model.num_agents
    label1 = model.label_count[1]
    ad_rate = round(label1 / totalhousehold, 4)
    return ad_rate


def getlabel_3_AdRate(model):
    totalhousehold = model.num_agents
    label1 = model.label_count[2]
    ad_rate = round(label1 / totalhousehold, 4)
    return ad_rate


def getlabel_1_AdRateDis(model):
    adRate_dis = []
    for i in range(6):
        household_disi = sum(model.agent_D_count[i])
        label1_disi = model.label_count_dis[i][0]
        rate_disi = round(label1_disi / household_disi, 4)
        adRate_dis.append(rate_disi)
    return adRate_dis


def getlabel_2_AdRateDis(model):
    adRate_dis = []
    for i in range(6):
        household_disi = sum(model.agent_D_count[i])
        label1_disi = model.label_count_dis[i][1]
        rate_disi = round(label1_disi / household_disi, 4)
        adRate_dis.append(rate_disi)
    return adRate_dis


def getlabel_3_AdRateDis(model):
    adRate_dis = []
    for i in range(6):
        household_disi = sum(model.agent_D_count[i])
        label1_disi = model.label_count_dis[i][2]
        rate_disi = round(label1_disi / household_disi, 4)
        adRate_dis.append(rate_disi)
    return adRate_dis


def getHouseperNeighbourhood(model):
    housePerNei = []
    for i in model.agent_list_DN:
        housePerNei.append(i)
    return housePerNei


def get_adoptionRate(model):
    ad_rate = 0
    if model.proType == 0:
        if model.totaladoption != 0:
            a = (
                model.adoptioncount[0]
                + model.adoptioncount[1]
                + model.adoptioncount[6]
                + model.adoptioncount[7]
                + model.adoptioncount[12]
                + model.adoptioncount[13]
            )
            b = model.totaladoption
            ad_rate = round(a / b, 4)
    elif model.proType == 1:
        if model.totaladoption != 0:
            a = (
                model.adoptioncount[0]
                + model.adoptioncount[3]
                + model.adoptioncount[6]
                + model.adoptioncount[9]
                + model.adoptioncount[12]
                + model.adoptioncount[15]
                + model.adoptioncount[18]
                + model.adoptioncount[21]
            )
            b = model.totaladoption
            ad_rate = round(a / b, 4)
    else:
        if model.totaladoption != 0:
            a = model.totaladoption
            b = len(model.buildingList)
            ad_rate = round(a / b, 4)
    return ad_rate


# district heating
def DisH_tatal(model):
    total_dis = model.disHeatingCount
    return total_dis


def DisH_Dis0(model):
    disH_dis0 = model.disHeatingCount_dis[0]
    return disH_dis0


def DisH_Dis1(model):
    disH_dis1 = model.disHeatingCount_dis[1]
    return disH_dis1


def DisH_Dis2(model):
    disH_dis2 = model.disHeatingCount_dis[2]
    return disH_dis2


def DisH_Dis3(model):
    disH_dis3 = model.disHeatingCount_dis[3]
    return disH_dis3


def DisH_Dis4(model):
    disH_dis4 = model.disHeatingCount_dis[4]
    return disH_dis4


def DisH_Dis5(model):
    disH_dis5 = model.disHeatingCount_dis[5]
    return disH_dis5


def countHeating_total_dis(model):
    total_dis = [[], []]
    if model.proType == 1:
        total_dis[0] = model.disHeatingCount
        for i in model.disHeatingCount_dis:
            total_dis[1].append(i)
    else:
        total_dis = [[0], [0]]
    return total_dis


def get_adoptionCount(model):
    a = []
    for i in model.adoptioncount:
        a.append(i)
    return a


def get_adoptionNumber(model):
    a = model.totaladoption
    return a


def Dis0_adoptionNum(model):
    return model.total_adoption_dis[0]


def Dis1_adoptionNum(model):
    return model.total_adoption_dis[1]


def Dis2_adoptionNum(model):
    return model.total_adoption_dis[2]


def Dis3_adoptionNum(model):
    return model.total_adoption_dis[3]


def Dis4_adoptionNum(model):
    return model.total_adoption_dis[4]


def Dis5_adoptionNum(model):
    return model.total_adoption_dis[5]


def get_dis_adoption(model):
    a = []
    for i in model.total_adoption_dis:
        a.append(i)
    return a


def get_dis_adoptionRate(model):
    adotpionRate = [0] * 6
    if model.proType == 0:
        for i in range(6):
            b = model.total_adoption_dis[i]
            if b == 0:
                adotpionRate[i] = 0
            else:
                a = (
                    model.adoption_dis_count[i][0]
                    + model.adoption_dis_count[i][1]
                    + model.adoption_dis_count[i][6]
                    + model.adoption_dis_count[i][7]
                    + model.adoption_dis_count[i][12]
                    + model.adoption_dis_count[i][13]
                )
                adotpionRate[i] = round(a / b, 4)
    elif model.proType == 1:
        for i in range(6):
            b = model.total_adoption_dis[i]
            if b == 0:
                adotpionRate[i] = 0
            else:
                a = (
                    model.adoption_dis_count[i][0]
                    + model.adoption_dis_count[i][3]
                    + model.adoption_dis_count[i][6]
                    + model.adoption_dis_count[i][9]
                    + model.adoption_dis_count[i][12]
                    + model.adoption_dis_count[i][15]
                    + model.adoption_dis_count[i][18]
                    + model.adoption_dis_count[i][21]
                )
                adotpionRate[i] = round(a / b, 4)
    else:
        for i in range(6):
            b = model.total_adoption_dis[i]
            if b == 0:
                adotpionRate[i] = 0
            else:
                lenNei = [len(j) for j in model.blByNei[i]]
                a = sum(lenNei)
                adotpionRate[i] = round(b / a, 4)
    return adotpionRate


def get_disAdCount(model):
    a = []
    for i in model.adoption_dis_count:
        m = []
        for j in i:
            m.append(j)
        a.append(m)
    return a


def get_att1_dis(model):  # get the count of att1
    att1_dis = [0] * 5
    for i in model.agent_list:
        a = i.att1
        if a < 1.5:
            att1_dis[0] += 1
        elif a < 2.5:
            att1_dis[1] += 1
        elif a < 3.5:
            att1_dis[2] += 1
        elif a < 4.5:
            att1_dis[3] += 1
        else:
            att1_dis[4] += 1
    return att1_dis


def get_att2_dis(model):  # get the count of att2
    att2_dis = [0] * 5
    for i in model.agent_list:
        a = i.att2
        if a < 1.5:
            att2_dis[0] += 1
        elif a < 2.5:
            att2_dis[1] += 1
        elif a < 3.5:
            att2_dis[2] += 1
        elif a < 4.5:
            att2_dis[3] += 1
        else:
            att2_dis[4] += 1
    return att2_dis


def get_class_dis(model):
    class_dis = [0] * 3
    for i in model.agent_list:
        a = i.group
        class_dis[(a - 1)] += 1
    return class_dis


def getEleEnergy(model):
    totalEnergy = 0
    if model.proType == 0:
        for i in model.agent_list:
            package = i.app_ac_package
            energyLabel = i.app_ac_energyLabel
            agentEC = attribute.appAnnualEnergy[package - 1][energyLabel - 1] / 2
            totalEnergy += agentEC
    if model.proType == 2:
        for i in model.agent_list:
            productIndex = i.PV_adoption
            elecProduction = 0
            if attribute.PV_code[productIndex][0] != 1:
                if attribute.PV_code[productIndex][1] == 1:
                    elecProduction = 5600 / 2
                elif attribute.PV_code[productIndex][2] == 1:
                    elecProduction = 13000 / 2
                else:
                    elecProduction = 19000 / 2
            totalEnergy += elecProduction
    return totalEnergy
