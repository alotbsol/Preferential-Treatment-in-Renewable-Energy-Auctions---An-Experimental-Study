import random as random
import pandas as pd

from distributions import DistributionGenerator


def generate_random_parameters_to_csv(no_groups=4, plyers_per_group=4, no_rounds=100,
                                      ws_min=5, ws_max=9,
                                      oc_min=0.8, oc_max=1.2,
                                      base_lcoe=50,
                                      random_seed=16180339,
                                      name="scenario_x",
                                      ):
    random.seed(random_seed)

    id_scenario = str(name) + "_seed:" + str(random_seed) + \
                  "_ws_min_" + str(ws_min) +"_ws_max_" + str(ws_max) \
                  +"_base_lcoe_"+ str(base_lcoe) + \
                  "_oc_min_" + str(oc_min) + "_oc_max_"+ str(oc_max)

    InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=base_lcoe,
                                              oc_min=oc_min, oc_max=oc_max)

    parameters_dic = {"round": [],
                      "group": [],
                      "player_slot": [],
                      "ws": [],
                      "other_costs": [],
                      "cost_A": [],
                      "cost_B": [],
                      "production": [],
                      "lcoe": [],
                      "correction_factor": [],
                      "minimum_bid_rym": [],
                      "id_scenario": [],
                      }

    current_round = 0

    for iii in range(no_rounds):
        current_round += 1
        current_group = 0
        for ii in range(no_groups):
            current_group += 1
            current_player = 0
            for i in range(plyers_per_group):
                current_player += 1
                """random generation of parameters"""
                ws = random.randint(ws_min * 10, ws_max * 10) / 10
                other_costs = random.randint(oc_min * 100, oc_max * 100) / 100

                parameters_dic["round"].append(current_round)
                parameters_dic["group"].append(current_group)
                parameters_dic["player_slot"].append(current_player)
                parameters_dic["ws"].append(ws)
                parameters_dic["other_costs"].append(other_costs)

                """ Loaded from original distributions"""
                ws_index = InputDistribution.distribution["ws"].index(ws)
                production = InputDistribution.distribution["production"][ws_index]
                correction_factor = InputDistribution.distribution["correction_factor"][ws_index]
                production_lcoe = InputDistribution.distribution["lcoe"][ws_index]
                lcoe = production_lcoe * other_costs

                parameters_dic["cost_A"].append(production_lcoe)
                parameters_dic["cost_B"].append(lcoe - production_lcoe)
                parameters_dic["production"].append(production)
                parameters_dic["lcoe"].append(lcoe)
                parameters_dic["correction_factor"].append(correction_factor)
                parameters_dic["minimum_bid_rym"].append(lcoe/correction_factor)

                parameters_dic["id_scenario"].append(id_scenario)

    df_out = pd.DataFrame.from_dict(parameters_dic)
    df_out.to_csv("{}.csv".format(name))

    pd.DataFrame.from_dict(InputDistribution.distribution).to_csv("{}_distribution.csv".format(name))


if __name__ == '__main__':
    generate_random_parameters_to_csv(random_seed=16180339, name="scenario_1")
    generate_random_parameters_to_csv(random_seed=1618033, name="scenario_2")
    generate_random_parameters_to_csv(random_seed=161803, name="scenario_3")
    generate_random_parameters_to_csv(random_seed=16180, name="scenario_4")


