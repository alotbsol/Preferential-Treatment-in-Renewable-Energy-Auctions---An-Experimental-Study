from auction import AuctionGenerator
from random_parameters_generation import generate_random_parameters_to_csv

import pandas as pd


def play_scenario(parameters_df, distributions_df, name="", rym=0, maximum_bid=90.3):
    export_name = str(name) + "rym" + str(rym)

    demand_scenarios = [1, 3, 1, 3]
    runs_per_demand_scenario = int(parameters_df["round"].max() / len(demand_scenarios))

    """"Creating auction class"""
    Auctions = AuctionGenerator(parameters_df=parameters_df,
                                distributions_df=distributions_df,
                                active_players=16,
                                rym=rym,
                                demand=3,
                                supply=4,
                                maximum_bid=maximum_bid)

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
    """creating input csv"""
    generate_random_parameters_to_csv(random_seed=16180339, name="scenario_1")

    """playing scenario"""
    for i in [0, 1]:
        play_scenario(name="scenario_1",
                      parameters_df=pd.read_csv("distributions/scenario_1.csv"),
                      distributions_df=pd.read_csv("distributions/scenario_1_distribution.csv"),
                      rym=i,
                      maximum_bid=90.3)









