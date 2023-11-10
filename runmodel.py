from model import adoptionmodel
import time
import mesa
import pandas as pd
from multiprocessing import freeze_support
import random


for runTime in range(10):  # interation of model
    print("runtime", runTime)
    initial_time = time.time()
    model = adoptionmodel(
        num_agents=150000,  # the number of simulated agents
        proType=0,  # the simualted product (0: appliance, 1: h&c, 2: community PV)
        # policy list:
        # app: 0__energy lable, 1__subsidy, 2__popularity (4), 3__only online or only phsical (normal: 0, only online: 1, only phsical),
        #      -1: information campaign
        # heating: 2__pop, -2__district heating promotion, -1__information campaign
        # PV: 3__demo project, 1__community size (1: 3, 2: 7, 3: 5), 2__agreerate, -1__information campaign
        policyList=[0, 0, 0, 0, 2],
        decision_heuristic=[0.049, 0.67, 0.22, 0.259],  # for community PV
    )
    # report model initialization time
    print("initialization time", "--- %s seconds ---" % (time.time() - initial_time))
    step_time = time.time()
    for i in range(31):  # model steps
        model.step()
    fileName = "runTime_" + str(runTime) + ".csv"
    # get data
    adoption_df = model.datacollector.get_model_vars_dataframe()
    # write simulation results
    adoption_df.to_csv(
        "file_path" + fileName,
        index=False,
    )

    # get time
    print("step time", "--- %s seconds ---" % (time.time() - step_time))
    print("model time", "--- %s seconds ---" % (time.time() - initial_time))
    model.reset()
