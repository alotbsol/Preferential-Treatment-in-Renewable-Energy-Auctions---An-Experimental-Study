from random_parameters_generation import generate_random_parameters
from theory_calc import AuctionGeneratorTheory

import pandas as pd
from scipy.stats import ttest_ind


def play_scenario(parameters_df, demand=1, name="", rym=0,):
    export_name = str(name)

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
        print("demand", demand, "round", itteration)
        Auctions.split_players_random()
        Auctions.input_parameters_to_players()

        for i in Auctions.players_dic:
            Auctions.players_dic[i].place_random_bid()

        Auctions.evaluate_round_per_group()
        Auctions.results_to_players()
        Auctions.store_round_results()

    return Auctions.results_storage


def power_calc():
    scenario_parameters = generate_random_parameters(no_groups=1, plyers_per_group=4, no_rounds=25,
                                                     ws_min=5, ws_max=9,
                                                     oc_min=0.8, oc_max=1.2,
                                                     ws_decimals=1,
                                                     oc_decimals=2,
                                                     base_lcoe=50,
                                                     max_bid_no_rym=90.3,
                                                     max_bid_rym=70,
                                                     random_seed=16180339,
                                                     name="scenario_x",
                                                     )

    """playing scenario"""
    results = (play_scenario(name="theory_scenario_1", parameters_df=scenario_parameters))
    results_subsidy_no_rym = results["1"]["NoRYM_model_subsidy"]
    results_subsidy_rym = results["1"]["RYM_model_subsidy"]

    print(results_subsidy_no_rym)
    print(results_subsidy_rym)
    t_stat, p_value = ttest_ind(results_subsidy_no_rym, results_subsidy_rym)

    print(t_stat, p_value)

if __name__ == '__main__':
    power_calc()
