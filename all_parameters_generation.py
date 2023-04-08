import pandas as pd

from distributions import DistributionGenerator


def generate_all_parameters_combination(ws_min=5, ws_max=9,
                                               oc_min=0.8, oc_max=1.2,
                                               ws_decimals=1,
                                               oc_decimals=2,
                                               base_lcoe=50,
                                               name="probability_dist",
                                               ):

    id_scenario = str(name) + \
                  "_ws_min_" + str(ws_min) +"_ws_max_" + str(ws_max) \
                  +"_base_lcoe_"+ str(base_lcoe) + \
                  "_oc_min_" + str(oc_min) + "_oc_max_" + str(oc_max)

    ws_scale = 10 ** ws_decimals
    oc_scale = 10 ** oc_decimals

    InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=base_lcoe,
                                              oc_min=oc_min, oc_max=oc_max,
                                              ws_decimals=ws_decimals,
                                              )

    parameters_dic = {"iteration": [],
                      "ws": [],
                      "other_costs": [],
                      "cost_A": [],
                      "cost_B": [],
                      "production": [],
                      "cost": [],
                      "break_even_no_rym": [],
                      "correction_factor": [],
                      "break_even_rym": [],
                      "id_scenario": [],
                      }

    current_round = 0

    """generation of parameters"""
    for ii in range(ws_min * ws_scale, ws_max * ws_scale + 1):
        ws = ii / ws_scale
        for i in range(int(oc_min * oc_scale), int(oc_max * oc_scale) + 1):
            current_round += 1

            other_costs = i / oc_scale

            parameters_dic["iteration"].append(current_round)
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
            parameters_dic["cost"].append(cost)
            parameters_dic["break_even_no_rym"].append(cost)
            parameters_dic["correction_factor"].append(correction_factor)
            parameters_dic["break_even_rym"].append(cost/correction_factor)

            parameters_dic["id_scenario"].append(id_scenario)

    df_out = pd.DataFrame.from_dict(parameters_dic)

    return df_out


def export_to_csv(name="probability_dist"):
    df = generate_all_parameters_combination(name="probability_dist", ws_decimals=1, oc_decimals=2, )

    writer = pd.ExcelWriter("distributions/{0}.xlsx".format(name), engine="xlsxwriter")

    df.to_excel(writer, sheet_name="all_data")

    df_no_rym = df["break_even_no_rym"].sort_values()
    df_rym = df["break_even_rym"].sort_values()

    df.to_excel(writer, sheet_name="all_data")
    df_no_rym.to_excel(writer, sheet_name="no_rym")
    df_rym.to_excel(writer, sheet_name="rym")

    writer.save()


if __name__ == '__main__':
    export_to_csv(name="probability_dist")

