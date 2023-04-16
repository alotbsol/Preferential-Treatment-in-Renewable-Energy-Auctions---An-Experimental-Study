import random as random
import pandas as pd
from scipy.stats import percentileofscore

from distributions import DistributionGenerator
from all_parameters_generation import generate_all_parameters_combination


def generate_random_parameters(no_groups=4, plyers_per_group=4, no_rounds=100,
                               ws_min=5, ws_max=9,
                               oc_min=0.8, oc_max=1.2,
                               ws_decimals=1,
                               oc_decimals=2,
                               base_lcoe=50,
                               max_bid_no_rym=90.3,
                               max_bid_rym=70,
                               random_seed=16180339,
                               name="sample_x",
                               ):
    random.seed(random_seed)

    id_sample = str(name) + "_seed:" + str(random_seed) + \
                  "_ws_min_" + str(ws_min) + "_ws_max_" + str(ws_max) \
                  + "_base_lcoe_" + str(base_lcoe) + \
                  "_oc_min_" + str(oc_min) + "_oc_max_" + str(oc_max)

    ws_scale = 10 ** ws_decimals
    oc_scale = 10 ** oc_decimals

    InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=base_lcoe,
                                              oc_min=oc_min, oc_max=oc_max)

    parameters_dic = {"round": [],
                      "group": [],
                      "player_slot": [],
                      "cost": [],
                      "break_even_bid_no_rym": [],
                      "percentile_no_rym": [],
                      "correction_factor": [],
                      "break_even_bid_rym": [],
                      "percentile_rym": [],
                      "max_bid_no_rym": [],
                      "max_bid_rym": [],
                      "ws": [],
                      "other_costs": [],
                      "cost_A": [],
                      "cost_B": [],
                      "production": [],
                      "id_sample": [],
                      }

    all_parameters_distribution = generate_all_parameters_combination(
        ws_min=ws_min, ws_max=ws_max,
        oc_min=oc_min, oc_max=oc_max,
        ws_decimals=ws_decimals,
        oc_decimals=oc_decimals,
        base_lcoe=base_lcoe, )

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
                ws = random.randint(ws_min * ws_scale, ws_max * ws_scale) / ws_scale
                other_costs = random.randint(oc_min * oc_scale, oc_max * oc_scale) / oc_scale

                parameters_dic["round"].append(current_round)
                parameters_dic["group"].append(current_group)
                parameters_dic["player_slot"].append(current_player)
                parameters_dic["ws"].append(ws)
                parameters_dic["other_costs"].append(other_costs)

                """ Loaded from original distributions"""
                ws_index = InputDistribution.distribution["ws"].index(ws)
                production = InputDistribution.distribution["production"][ws_index]
                correction_factor = InputDistribution.distribution["correction_factor"][ws_index]
                production_cost = InputDistribution.distribution["cost"][ws_index]
                cost = production_cost * other_costs

                parameters_dic["cost_A"].append(production_cost)
                parameters_dic["cost_B"].append(cost - production_cost)
                parameters_dic["production"].append(production)
                parameters_dic["correction_factor"].append(correction_factor)

                parameters_dic["cost"].append(cost)
                parameters_dic["break_even_bid_no_rym"].append(cost)
                parameters_dic["break_even_bid_rym"].append(cost / correction_factor)

                parameters_dic["percentile_no_rym"].append(percentileofscore(
                    all_parameters_distribution["break_even_no_rym"], cost))
                parameters_dic["percentile_rym"].append(percentileofscore(
                    all_parameters_distribution["break_even_rym"], cost / correction_factor))

                parameters_dic["max_bid_no_rym"].append(max_bid_no_rym)
                parameters_dic["max_bid_rym"].append(max_bid_rym)

                parameters_dic["id_sample"].append(id_sample)

    df_out = pd.DataFrame.from_dict(parameters_dic)
    return df_out


def generate_random_parameters_to_csv(no_groups=4, plyers_per_group=4, no_rounds=100,
                                      ws_min=5, ws_max=9,
                                      oc_min=0.8, oc_max=1.2,
                                      ws_decimals=1,
                                      oc_decimals=2,
                                      base_lcoe=50,
                                      max_bid_no_rym=90.3,
                                      max_bid_rym=70,
                                      random_seed=16180339,
                                      name="sample_x",
                                      ):
    df_out = generate_random_parameters(no_groups=no_groups, plyers_per_group=plyers_per_group, no_rounds=no_rounds,
                                        ws_min=ws_min, ws_max=ws_max,
                                        oc_min=oc_min, oc_max=oc_max,
                                        ws_decimals=ws_decimals,
                                        oc_decimals=oc_decimals,
                                        base_lcoe=base_lcoe,
                                        max_bid_no_rym=max_bid_no_rym,
                                        max_bid_rym=max_bid_rym,
                                        random_seed=random_seed,
                                        name=name,
                                        )

    df_out.to_csv("distributions/{}.csv".format(name))


if __name__ == '__main__':
    generate_random_parameters_to_csv(random_seed=16180339, name="sample_1")
    generate_random_parameters_to_csv(random_seed=1618033, name="sample_2")
    generate_random_parameters_to_csv(random_seed=161803, name="sample_3")
    generate_random_parameters_to_csv(random_seed=16180, name="sample_4")
