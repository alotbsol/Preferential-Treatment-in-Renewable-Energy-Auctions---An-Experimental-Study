from random_parameters_generation import generate_random_parameters
from theory_calc import AuctionGeneratorTheory

import pandas as pd
from scipy.stats import ttest_ind


def play_scenario(parameters_df, demand=1, rym=0,):
    rounds = int(parameters_df["round"].max())

    """"Creating auction class"""
    Auctions = AuctionGeneratorTheory(parameters_df=parameters_df,
                                      active_players=4,
                                      rym=rym,
                                      demand=demand,
                                      supply=4,
                                      )

    Auctions.change_demand_parameter(demand=demand)

    for itteration in range(rounds):
        Auctions.split_players_random()
        Auctions.input_parameters_to_players()

        for i in Auctions.players_dic:
            Auctions.players_dic[i].place_random_bid()

        Auctions.evaluate_round_per_group()
        Auctions.results_to_players()
        Auctions.store_round_results()

    return Auctions.results_storage


def power_calc():
    writer = pd.ExcelWriter("distributions/{0}.xlsx".format("power_calc"), engine="xlsxwriter")

    for ii in [1, 3]:
        power_results_subsidy = {"t": [],
                                 "p": [],
                                 "average_subsidy_no_rym": [],
                                 "average_subsidy_rym": [],
                                 }

        for i in range(0, 100):
            scenario_parameters = generate_random_parameters(no_groups=1, plyers_per_group=4, no_rounds=50,
                                                         ws_min=5, ws_max=9,
                                                         oc_min=0.8, oc_max=1.2,
                                                         ws_decimals=1,
                                                         oc_decimals=2,
                                                         base_lcoe=50,
                                                         max_bid_no_rym=90.3,
                                                         max_bid_rym=70,
                                                         random_seed=i,
                                                         name="scenario_x",
                                                         )

            """playing scenario"""
            results = (play_scenario(parameters_df=scenario_parameters, demand=ii))

            results_subsidy_no_rym = results["1"]["NoRYM_model_subsidy"]
            results_subsidy_rym = results["1"]["RYM_model_subsidy"]

            t_stat, p_value = ttest_ind(results_subsidy_no_rym, results_subsidy_rym)

            power_results_subsidy["t"].append(t_stat)
            power_results_subsidy["p"].append(p_value)
            power_results_subsidy["average_subsidy_no_rym"].append(sum(results_subsidy_no_rym)/len(results_subsidy_no_rym))
            power_results_subsidy["average_subsidy_rym"].append(sum(results_subsidy_rym)/len(results_subsidy_rym))

        print("demand", ii,)
        print(power_results_subsidy["t"])
        print(power_results_subsidy["p"])
        print("max p value is", max(power_results_subsidy["p"]))

        df_out = pd.DataFrame.from_dict(power_results_subsidy)
        df_out.to_excel(writer, sheet_name=str(ii))

    writer.save()


if __name__ == '__main__':
    power_calc()
