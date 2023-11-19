from theory_calc import AuctionGeneratorTheory

import pandas as pd


def play_scenario(parameters_df, name="", rym=0,):
    export_name = str(name)

    # specific demand scenario setup with 16 rounds per demand scenario
    demand_scenarios = [1, 3, 1, 3, 1, 3]
    runs_per_demand_scenario = 16

    # can be used for arbitrarily long csv
    # runs_per_demand_scenario = int(parameters_df["round"].max() / len(demand_scenarios))


    """"Creating auction class"""
    Auctions = AuctionGeneratorTheory(parameters_df=parameters_df,
                                active_players=16,
                                rym=rym,
                                demand=3,
                                supply=4,
                                )

    for demand in demand_scenarios:
        Auctions.change_demand_parameter(demand=demand)

        for itteration in range(runs_per_demand_scenario):
            print("demand", demand, "round", itteration)
            Auctions.split_players_random()
            Auctions.input_parameters_to_players()

            for i in Auctions.players_dic:
               Auctions.players_dic[i].place_random_bid()

            Auctions.evaluate_round_per_group()
            Auctions.results_to_players()
            Auctions.store_round_results()

    Auctions.export_everything(name=str(export_name))


if __name__ == '__main__':
    """playing scenarios"""
    play_scenario(name="theory_sample_1", parameters_df=pd.read_csv("distributions/sample_1.csv"))
    play_scenario(name="theory_sample_2", parameters_df=pd.read_csv("distributions/sample_2.csv"))
    play_scenario(name="theory_sample_3", parameters_df=pd.read_csv("distributions/sample_3.csv"))
    play_scenario(name="theory_sample_4", parameters_df=pd.read_csv("distributions/sample_4.csv"))
