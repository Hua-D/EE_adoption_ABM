import attribute
import random
import networkx as nx
import copy
import numpy as np


def getBuildingNum(agentlist, agent_list_DN, communitySize, model):
    combinedList = [[], [], []]
    m = copy.deepcopy(
        agent_list_DN
    )  # copy agent list in district and neighbourhood format
    building_list = []
    BL_by_nei = []
    BL_by_dis = []
    BL_index = 0  # building list index
    for i in range(len(agent_list_DN)):
        BL_by_nei.append([])
        BL_by_dis.append([])
        for j in range(len(agent_list_DN[i])):
            BL_by_nei[i].append([])
            m_ij = m[i][j]
            len_mij = len(m_ij)
            while len_mij > 0:
                if communitySize == 0:
                    z = random.choice([4, 5, 5, 6])
                elif communitySize == 1:
                    z = 3
                elif communitySize == 2:
                    z = 7
                elif communitySize == 3:
                    z = 10
                if len(m_ij) > z:
                    y = random.sample(m_ij, z)
                else:
                    y = copy.deepcopy(m_ij)
                for a in y:
                    agentlist[a].building_ID = BL_index
                    m_ij.remove(a)
                    len_mij -= 1
                building_list.append(y)
                BL_by_nei[i][j].append(y)
                BL_by_dis[i].append(y)
                BL_index += 1
            for id in agent_list_DN[i][j]:
                agent_agent_id = model.agent_list[id]
                agent_agent_id.NeiAdoption = np.zeros(len(BL_by_nei[i][j]) - 1)
    combinedList[0] = building_list
    combinedList[1] = BL_by_nei
    combinedList[2] = BL_by_dis
    return combinedList


def getHouseNum(agent_list_DN):  # get the number of household per neigbourhood
    agent_D_count = []
    for i in range(len(agent_list_DN)):
        agent_D_count.append([])
        for j in range(len(agent_list_DN[i])):
            agent_D_count[i].append(len(agent_list_DN[i][j]))
    return agent_D_count


def DN_agentList():
    DN_list = []
    for i in range(len(attribute.disPop)):
        DN_list.append([])
        for j in range(len(attribute.neiPop[i])):
            DN_list[i].append([])
    return DN_list


def ol_SN(agentlist):
    num_list = [i for i in range(len(agentlist))]
    SN = nx.Graph()
    first_node = random.choice(num_list)
    num_list.remove(first_node)
    SN.add_node(first_node)
    i = len(SN)
    repeat_nodes = [first_node]
    while i < len(agentlist):
        m = random.choice(num_list)
        num_list.remove(m)
        target = random.choice(repeat_nodes)
        SN.add_edge(m, target)
        repeat_nodes.extend([m, target])
        i += 1
    return SN


def ph_SN(agentList, DN_list):
    So_Ne = nx.Graph()
    num_agents = len(agentList)
    for i in range(num_agents):
        So_Ne.add_node(i)
    for i in range(len(DN_list)):
        for j in range(len(DN_list[i])):
            m = DN_list[i][j]
            for x in m:
                n = []
                index_x = m.index(x)
                if agentList[x].num_connections > len(list(So_Ne.adj[x])):
                    for index_y in range(index_x + 1, len(m)):
                        y = m[index_y]
                        if len(list(So_Ne.adj[y])) < agentList[y].num_connections:
                            if agentList[x].income == agentList[y].income:
                                if agentList[x].edu == agentList[y].edu:
                                    n.append(y)
                min_loop = min(agentList[x].num_connections, len(n))
                # print(min_loop)
                para = 0
                if min_loop > 0:
                    while para < min_loop:
                        k = random.choice(n)
                        So_Ne.add_edge(
                            x,
                            k,
                            feature="similar socio-backgroud and close geographic distance",
                        )
                        para += 1
                    n.clear()
    # rewire
    edge_list = list(So_Ne.edges)
    rewire_num = int(0.1 * len(edge_list))
    rewire_list = random.sample(edge_list, rewire_num)
    for i in rewire_list:
        a = random.sample(list(i), 1)[0]
        So_Ne.remove_edge(i[0], i[1])
        b = random.randint(0, (len(agentList) - 1))
        while b == a:
            b = random.randint(0, len(agentList))
        So_Ne.add_edge(a, b, feature="rewireing")
    return So_Ne


def getInitialPV2(model):
    initialAdoptionNum = 358
    building_WithPv = random.sample(model.buildingList, initialAdoptionNum)
    print("initialAdoptionNum", initialAdoptionNum)
    building_WithoutPV = copy.deepcopy(model.buildingList)
    m = [i for i in range(1, 11)]
    for i in building_WithPv:
        building_WithoutPV.remove(i)
        adptedPV = random.choice(m)
        for j in i:
            agentj = model.agent_list[j]
            agentj.PV_adoption = adptedPV
            if agentj.num_connections > 0:
                SN = model.ph_SN
                friends = list(SN.adj[j])
                for fri in friends:
                    agent_fri = model.agent_list[fri]
                    for k in range(len(agent_fri.SnAdoption)):
                        if agent_fri.SnAdoption[k] != 0:
                            pass
                        elif agent_fri.SnAdoption[k] == 0:
                            agent_fri.SnAdoption[k] = adptedPV
                            break
        model.totaladoption += 1
        model.adoptioncount[adptedPV] += 1
        dis = model.agent_list[i[0]].district_id
        nei = model.agent_list[i[0]].neighborhood_id
        model.adoption_dis_count[dis][adptedPV] += 1
        model.total_adoption_dis[dis] += 1
        buildingListDisNei = model.blByNei[dis][nei]
        BuiListDisNeiWithout_i = [
            building for building in buildingListDisNei if building != i
        ]
        for building in BuiListDisNeiWithout_i:
            for agent_id in building:
                agent = model.agent_list[agent_id]
                for k in range(len(agent.NeiAdoption)):
                    if agent.NeiAdoption[k] != 0:
                        pass
                    elif agent.NeiAdoption[k] == 0:
                        agent.NeiAdoption[k] = adptedPV
                        break
    return building_WithoutPV
