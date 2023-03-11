import random as random
import pandas as pd

from distributions import DistributionGenerator


def generate_probabiltiy_distribution_to_csv(iterations=10,
                                             ws_min=5, ws_max=9,
                                             oc_min=0.8, oc_max=1.2,
                                             base_lcoe=50,
                                             random_seed=16180339,
                                             name="probability_dist",
                                              ):
    random.seed(random_seed)

    id_scenario = str(name) + "_seed:" + str(random_seed) + \
                  "_ws_min_" + str(ws_min) +"_ws_max_" + str(ws_max) \
                  +"_base_lcoe_"+ str(base_lcoe) + \
                  "_oc_min_" + str(oc_min) + "_oc_max_"+ str(oc_max)

    InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=base_lcoe,
                                              oc_min=oc_min, oc_max=oc_max)

    parameters_dic = {"iteration": [],
                      "ws": [],
                      "other_costs": [],
                      "cost_A": [],
                      "cost_B": [],
                      "production": [],
                      "break_even_no_rym": [],
                      "correction_factor": [],
                      "break_even_rym": [],
                      "id_scenario": [],
                      }

    current_round = 0

    """generation of parameters"""
    for ii in range(ws_min * 10, ws_max * 10 + 1):
        ws = ii / 10
        for i in range(int(oc_min * 100), int(oc_max * 100) + 1):
            current_round += 1

            other_costs = i / 100

            parameters_dic["iteration"].append(current_round)
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
            parameters_dic["break_even_no_rym"].append(lcoe)
            parameters_dic["correction_factor"].append(correction_factor)
            parameters_dic["break_even_rym"].append(lcoe/correction_factor)

            parameters_dic["id_scenario"].append(id_scenario)

    writer = pd.ExcelWriter("{0}.xlsx".format(name), engine="xlsxwriter")

    df_out = pd.DataFrame.from_dict(parameters_dic)


    df_out.to_excel(writer, sheet_name="all_data")

    df_no_rym = df_out["break_even_no_rym"].sort_values()
    df_rym = df_out["break_even_rym"].sort_values()

    df_out.to_excel(writer, sheet_name="all_data")
    df_no_rym.to_excel(writer, sheet_name="no_rym")
    df_rym.to_excel(writer, sheet_name="rym")

    writer.save()


if __name__ == '__main__':
    generate_probabiltiy_distribution_to_csv(random_seed=16180339, name="probability_dist", iterations=10000)

