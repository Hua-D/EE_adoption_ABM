import attribute
import model_initialization as mod_in
import agent_initialization as ag_in
import step_function as sf
import data_reporter as dr
from mesa import Model, Agent
import mesa
import pandas as pd
import networkx as nx
import random
from multiprocessing import freeze_support
import policy
import numpy as np
from mesa.datacollection import DataCollector


# ________________________________________________________________________________________________________________________________________________________________________________
# agent
class household(Agent):
    def __init__(
        self,
        unique_id,
        model,
        district_id,
        neighborhood_id,
        income,
        edu,
        age,
        att1,
        u1,
        att2,
        u2,
        esb,
        group,
        appy,
        appEX,
        hcy,
        hcEX,
        num_connections,
        building_ID,
        decision_strategy,
        app_ac_package,
        app_ac_energyLabel,
        PV_adoption,
        neg_info,
        recom_info,
        info_campaign,
        NeiAdoption,
        SnAdoption,
    ):
        super().__init__(unique_id, model)
        self.district_id = district_id
        self.neighborhood_id = neighborhood_id
        self.income = income
        self.edu = edu
        self.age = age
        self.att1 = att1  # 5
        self.u1 = u1
        self.att2 = att2
        self.u2 = u2
        self.esb = esb
        self.group = group
        self.appy = appy  # 10
        self.appEX = appEX
        self.hcy = hcy
        self.hcEX = hcEX
        self.num_connections = num_connections
        self.building_ID = building_ID  # 15
        self.decision_strategy = decision_strategy
        self.app_ac_package = app_ac_package
        self.app_ac_energyLabel = app_ac_energyLabel
        self.PV_adoption = PV_adoption
        self.neg_info = neg_info
        self.recom_info = recom_info
        self.info_campaign = info_campaign
        self.NeiAdoption = NeiAdoption
        self.SnAdoption = SnAdoption

    def resetAgent(self):
        del self.district_id
        del self.neighborhood_id
        del self.income
        del self.edu
        del self.age
        del self.att1
        del self.u1
        del self.att2
        del self.u2
        del self.esb
        del self.group
        del self.appy
        del self.appEX
        del self.hcy
        del self.hcEX
        del self.num_connections
        del self.building_ID
        del self.decision_strategy
        del self.app_ac_package
        del self.app_ac_energyLabel
        del self.PV_adoption
        del self.neg_info
        del self.recom_info
        del self.info_campaign
        del self.NeiAdoption
        del self.SnAdoption

    def step(self):
        self.age += 1
        self.appy += 1
        self.hcy += 1
        self.group = ag_in.GetGroup2(
            self.model.proType, self.att1, self.att2, self.income, self.esb
        )


# ________________________________________________________________________________________________________________________________________________________________________________
# Model
class adoptionmodel(Model):
    social_N = nx.Graph()
    stepCount = 0

    def __init__(
        self,
        num_agents,
        proType=0,
        policyList=[0, 0, 0, 0, 0],
        decision_heuristic=[0.049, 0.67, 0.22, 0.259],
    ):
        self.num_agents = num_agents
        self.proType = proType
        self.policyList = policyList
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.running = True
        self.productPoolLen = attribute.get_productpool_len(self.proType)
        self.totaladoption = 0
        self.total_adoption_dis = [0] * 6
        self.adoption_dis_count = []
        for i in range(6):
            self.adoption_dis_count.append([0] * self.productPoolLen)
        self.adoptioncount = [0] * self.productPoolLen
        self.buildingList = []
        self.blByNei = []
        self.blbydis = []
        self.ph_SN = 0
        self.ol_SN = 0
        self.agent_list = []
        self.agent_list_DN = mod_in.DN_agentList()
        self.agent_D_count = []
        self.label_count = [0, 0, 0]
        self.label_count_dis = [[0, 0, 0] for i in range(6)]
        self.disHeatingCount = 0
        self.disHeatingCount_dis = [0, 0, 0, 0, 0, 0]
        self.agentNumDis = [0, 0, 0, 0, 0, 0]
        self.buildingwithoutPV = []
        self.decision_heuristic = decision_heuristic

        for i in range(self.num_agents):
            dis = ag_in.GetDistrict()
            nei = ag_in.GetNeigh(dis)
            income = ag_in.GetIncome()
            edu = ag_in.getEdu(dis)
            age = ag_in.GetAge(dis)
            att1 = ag_in.getAtgw(income, edu)
            u1 = random.uniform(0.1, 2)
            u2 = random.uniform(0.1, 2)
            att2 = ag_in.getAtnr(income, edu)
            esb = ag_in.Getesb(income, edu)
            group = ag_in.GetGroup2(self.proType, att1, att2, income, esb)
            appy = ag_in.getInitialApp()
            appex = ag_in.getappLifeEX()
            hcy = ag_in.getInitialHc()
            hcex = ag_in.gethcLifeEX()
            decision_strategy = random.choices([0, 1, 2, 3], decision_heuristic)[0]
            building_ID = 0
            PV_adoption = 0
            # the first parameter is the index of the product (-1 means no negtive information),
            # the second parameter is the source of the information (1: physical connetions; 2: online connections)
            neg_info = [
                -1,
                0,
            ]
            recom_info = 0
            app_ac_package = ag_in.getAppAcEnergyPackage(self.proType, dis)
            if self.proType == 1:
                if app_ac_package == 3:
                    self.disHeatingCount += 1
                    self.disHeatingCount_dis[dis] += 1
            app_ac_energyLabel = ag_in.getAppAcEnergyLabel(self.proType)
            self.label_count[(app_ac_energyLabel - 1)] += 1
            self.label_count_dis[dis][(app_ac_energyLabel - 1)] += 1

            info_campaign = 0

            m = household(
                i,
                self,
                dis,
                nei,
                income,  # 5
                edu,
                age,
                att1,
                u1,
                att2,
                u2,  # 10
                esb,
                group,
                appy,
                appex,
                hcy,
                hcex,  # 15
                ag_in.NumPhysicalConnections(),
                building_ID,
                decision_strategy,
                # PV adoption status variable, 0 is no adoption
                app_ac_package,
                app_ac_energyLabel,
                PV_adoption,
                neg_info,
                recom_info,
                info_campaign,
                np.array([]),  # NeiAdption
                np.zeros(ag_in.NumPhysicalConnections()),  # SnAdoption
            )
            self.agent_list.append(m)
            self.agent_list_DN[dis][nei].append(m.unique_id)
            self.schedule.add(m)
            self.agentNumDis[dis] += 1

        if self.proType == 1:
            self.datacollector = mesa.DataCollector(
                model_reporters={
                    "step": dr.get_step,
                    # number of agent per district
                    "Dis0 agentNum": dr.Dis0_AgentNum,
                    "Dis1 agentNum": dr.Dis1_AgentNum,
                    "Dis2 agentNum": dr.Dis2_AgentNum,
                    "Dis3 agentNum": dr.Dis3_AgentNum,
                    "Dis4 agentNum": dr.Dis4_AgentNum,
                    "Dis5 agentNum": dr.Dis5_AgentNum,
                    # others
                    "adoption count": dr.get_adoptionCount,
                    "adoption rate": dr.get_adoptionRate,
                    "total adoption": dr.get_adoptionNumber,
                    "adoption rate by district": dr.get_dis_adoptionRate,
                    "total adoption by district": dr.get_dis_adoption,
                    "adotpion count by district": dr.get_disAdCount,
                    "atttude 'global warming' distribution": dr.get_att1_dis,
                    "attitude 'resource depletion' distribution": dr.get_att2_dis,
                    "class distribution": dr.get_class_dis,
                    "label1 rate": dr.getlabel_1_AdRate,
                    "label2 rate": dr.getlabel_2_AdRate,
                    "label3 rate": dr.getlabel_3_AdRate,
                    "label1 rate by district": dr.getlabel_1_AdRateDis,
                    "label2 rate by district": dr.getlabel_2_AdRateDis,
                    "label3 rate by district": dr.getlabel_3_AdRateDis,
                    # district heating adoption number
                    "district heating total": dr.DisH_tatal,
                    "district 0 disAdoption": dr.DisH_Dis0,
                    "district 1 disAdoption": dr.DisH_Dis1,
                    "district 2 disAdoption": dr.DisH_Dis2,
                    "district 3 disAdoption": dr.DisH_Dis3,
                    "district 4 disAdoption": dr.DisH_Dis4,
                    "district 5 disAdoption": dr.DisH_Dis5,
                },
            )
        elif self.proType == 0:
            self.datacollector = mesa.DataCollector(
                model_reporters={
                    "step": dr.get_step,
                    "adoption count": dr.get_adoptionCount,
                    "adoption rate": dr.get_adoptionRate,
                    "total adoption": dr.get_adoptionNumber,
                    "adoption rate by district": dr.get_dis_adoptionRate,
                    "total adoption by district": dr.get_dis_adoption,
                    "adotpion count by district": dr.get_disAdCount,
                    "atttude 'global warming' distribution": dr.get_att1_dis,
                    "attitude 'resource depletion' distribution": dr.get_att2_dis,
                    "class distribution": dr.get_class_dis,
                    "energy (kwh)": dr.getEleEnergy,
                    "label1 rate": dr.getlabel_1_AdRate,
                    "label2 rate": dr.getlabel_2_AdRate,
                    "label3 rate": dr.getlabel_3_AdRate,
                    "label1 rate by district": dr.getlabel_1_AdRateDis,
                    "label2 rate by district": dr.getlabel_2_AdRateDis,
                    "label3 rate by district": dr.getlabel_3_AdRateDis,
                },
            )
        else:
            self.datacollector = mesa.DataCollector(
                model_reporters={
                    "step": dr.get_step,
                    # number of agent per district
                    "Dis0 agentNum": dr.Dis0_AgentNum,
                    "Dis1 agentNum": dr.Dis1_AgentNum,
                    "Dis2 agentNum": dr.Dis2_AgentNum,
                    "Dis3 agentNum": dr.Dis3_AgentNum,
                    "Dis4 agentNum": dr.Dis4_AgentNum,
                    "Dis5 agentNum": dr.Dis5_AgentNum,
                    # others
                    "adoption count": dr.get_adoptionCount,
                    "adoption rate": dr.get_adoptionRate,
                    "total adoption": dr.get_adoptionNumber,
                    "adoption rate by district": dr.get_dis_adoptionRate,
                    "total adoption by district": dr.get_dis_adoption,
                    "adotpion count by district": dr.get_disAdCount,
                    "atttude 'global warming' distribution": dr.get_att1_dis,
                    "attitude 'resource depletion' distribution": dr.get_att2_dis,
                    "class distribution": dr.get_class_dis,
                    "label1 rate": dr.getlabel_1_AdRate,
                    "label2 rate": dr.getlabel_2_AdRate,
                    "label3 rate": dr.getlabel_3_AdRate,
                    "label1 rate by district": dr.getlabel_1_AdRateDis,
                    "label2 rate by district": dr.getlabel_2_AdRateDis,
                    "label3 rate by district": dr.getlabel_3_AdRateDis,
                    # PV adoption number per district
                    "Dis0 adoption Num": dr.Dis0_adoptionNum,
                    "Dis1 adoption Num": dr.Dis1_adoptionNum,
                    "Dis2 adoption Num": dr.Dis2_adoptionNum,
                    "Dis3 adoption Num": dr.Dis3_adoptionNum,
                    "Dis4 adoption Num": dr.Dis4_adoptionNum,
                    "Dis5 adoption Num": dr.Dis5_adoptionNum,
                },
            )

        # get the number of household per neigbourhood
        self.agent_D_count = mod_in.getHouseNum(self.agent_list_DN)
        # get a list of buildings include which household
        self.ph_SN = mod_in.ph_SN(self.agent_list, self.agent_list_DN)

        self.ol_SN = mod_in.ol_SN(self.agent_list)
        if self.proType == 2:
            self.buildingList = mod_in.getBuildingNum(
                self.agent_list, self.agent_list_DN, policyList[1], self
            )[0]
            self.blByNei = mod_in.getBuildingNum(
                self.agent_list, self.agent_list_DN, policyList[1], self
            )[1]
            self.blbydis = mod_in.getBuildingNum(
                self.agent_list, self.agent_list_DN, policyList[1], self
            )[2]
            self.buildingwithoutPV = mod_in.getInitialPV2(self)

    def proType(self):
        return self.proType

    def getProduct(self):
        sf.modelGetProduct(self)

    def reset(self):
        for i in self.agent_list:
            i.resetAgent()
        del self.adoption_dis_count
        del self.adoptioncount
        del self.agent_D_count
        del self.agent_list
        del self.agent_list_DN
        del self.blByNei
        del self.num_agents
        del self.ol_SN
        del self.ph_SN
        del self.datacollector
        del self.schedule
        del self

    def step(self):
        policy.info_cam(self)
        self.datacollector.collect(self)
        sf.RA2_model(self)
        # 40% of the neighborhoods in Qingshan district (index 5) will adopt district heating in step 5 (according to official documents)
        # and households in district 4 and 5 can choose adopt district heating or not.
        if self.proType == 1:
            if self.stepCount == 5:
                sf.Hcadoption(self)
        if self.proType == 2:
            if self.stepCount == 1:
                policy.DemoProjectPV(self.policyList[3], self, self.buildingwithoutPV)
        self.getProduct()
        self.schedule.step()
        self.stepCount += 1

    def get_numAgent(self):
        return self.N
