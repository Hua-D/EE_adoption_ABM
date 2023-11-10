import random
import attribute
import numpy as np


def getAtgw(income, edu):
    at_v = [1, 4, 5]
    at_d = at_d = attribute.dict_att1[(income, edu)]
    midValue = random.choices(at_v, at_d)[0]
    if midValue == 1:
        at_v2 = [1, 2, 3]
        at_d2 = [6, 17, 63]
        atgw = random.choices(at_v2, at_d2)[0]
    else:
        atgw = midValue
    return atgw


def getAtnr(income, edu):
    at_v = [1, 4, 5]
    at_d = attribute.dict_att2[(income, edu)]
    midValue = random.choices(at_v, at_d)[0]
    if midValue == 1:
        at_v2 = [1, 2, 3]
        at_d2 = [10, 14, 90]
        atnr = random.choices(at_v2, at_d2)[0]
    else:
        atnr = midValue
    return atnr


def NumPhysicalConnections():
    nc_v = [0, 2, 3, 5, 7, 8, 10]
    nc_d = [0.37, 0.02, 0.08, 0.18, 0.04, 0.23, 0.07]
    return random.choices(nc_v, nc_d)[0]


def GetDistrict():
    district_v = [0, 1, 2, 3, 4, 5]
    district_d = attribute.disPop
    return random.choices(district_v, district_d)[0]


def GetNeigh(Dis):
    m = []
    for i in range(6):
        if Dis == i:
            num = len(attribute.neiPop[i])
            nei_d = attribute.neiPop[i]
            break
    for i in range(num):
        m.append(i)
    return random.choices(m, nei_d)[0]


def GetAge(dis):
    age_v = [i for i in range(12)]
    age_d = attribute.age_dis[dis]
    a = random.choices(age_v, age_d)[0]
    age = random.randint(a * 5 + 20, a * 5 + 24)
    return age


def Getesb(income, edu):  # ESB4
    esb_v = [1, 2, 3]
    esb_d = attribute.dict_esb4[(income, edu)]
    esb = random.choices(esb_v, esb_d)[0]
    return esb


def GetGroup2(proType, att1, att2, income, esb):
    appDic = attribute.agentClassProbAPP
    hcDic = attribute.agentClassProbHC
    pvDic = attribute.agentClassProbPV
    cla_value = [1, 2, 3]
    att1_r = round(att1)
    att2_r = round(att2)
    keyIndex = (att1_r, att2_r, income, esb)
    dis = []
    if proType == 0:
        if keyIndex in appDic:
            dis = appDic[keyIndex]
        else:
            dis = [0.459, 0.32, 0.221]
    if proType == 1:
        if keyIndex == hcDic:
            dis = hcDic[keyIndex]
        else:
            dis = [0.456, 0.371, 0.173]
    if proType == 2:
        if keyIndex in pvDic:
            dis = pvDic[keyIndex]
        else:
            dis = [0.22, 0.353, 0.427]
    cla = random.choices(cla_value, dis)[0]
    return cla


def GetIncome():
    in_v = [1, 2, 3, 4]
    in_d = [
        558 / (558 + 1098 + 630 + 1089),
        1098 / (558 + 1098 + 630 + 1089),
        630 / (558 + 1098 + 630 + 1089),
        1089 / (558 + 1098 + 630 + 1089),
    ]
    return random.choices(in_v, in_d)[0]


def getEdu(district_id):
    in_v = [1, 2, 3, 4]
    in_d = attribute.edu_dis[district_id]
    return random.choices(in_v, in_d)[0]


def getappLifeEX():
    a = np.random.gumbel(20, 1, 1)
    return round(a[0])


def gethcLifeEX():
    a = np.random.gumbel(24, 2, 1)
    return round(a[0])


def getInitialApp():
    a = random.randint(0, 20)
    return a


def getInitialHc():
    a = random.randint(0, 24)
    return a


def getApp_ac(proType):
    if proType == 0:
        pass


def getAppAcEnergyLabel(proType):
    energyLabel = 0
    enerLabelList = [1, 2, 3]
    appEnergyLabelDis = [0.18799, 0.50762, 0.18033]
    hcEnergyLabelDis = [0.3645, 0.1612, 0.4232]
    if proType == 0:
        energyLabel = random.choices(enerLabelList, appEnergyLabelDis)[0]
    if proType == 1:
        energyLabel = random.choices(enerLabelList, hcEnergyLabelDis)[0]
    return energyLabel


def getAppAcEnergyPackage(proType, dis):
    package = 0
    packageList = [1, 2, 3]
    packageDis = [25, 11, 16]
    if proType == 0:
        package = random.choices(packageList, packageDis)[0]
    if proType == 1:
        if dis == 4:
            Heating_dis = [0.7436, 0.1175, 20 / 144]
            package = random.choices(packageList, Heating_dis)[0]
        else:
            Heating_dis = [0.86352, 0.13648]
            Heating_value = [1, 2]
            package = random.choices(Heating_value, Heating_dis)[0]
    return package
