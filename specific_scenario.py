from auction import AuctionGenerator
from random_parameters_generation import generate_random_parameters_to_csv

import pandas as pd


def scenario_1_no_rym():
    """"loading scenario parameters"""
    parameters_df = pd.read_csv("scenario_1.csv")
    demand_scenarios = [1, 3, 1, 3]
    runs_per_demand_scenario = int(parameters_df["round"].max() / len(demand_scenarios))

    """"Creating auction class"""
    Auctions = AuctionGenerator(active_players=16)

    """"putting pre created scenario in """
    Auctions.store_input_parameters_csv(input_df=parameters_df)
    Auctions.change_rym_parameter(rym=0)
    Auctions.change_maximum_bid(maximum_bid=90.3)

    for demand in demand_scenarios:
        Auctions.change_demand_parameter(demand=demand)

        for itteration in range(runs_per_demand_scenario):
            print("round", itteration)
            Auctions.split_players_random()
            Auctions.input_parameters()

            for i in Auctions.players_dic:
               Auctions.players_dic[i].place_random_bid()

            Auctions.evaluate_round_per_group()
            Auctions.results_to_players()
            Auctions.store_round_results()

    Auctions.export_everything(name="scenario_1_no_rym")


def scenario_1_rym():
    """"loading scenario parameters"""
    parameters_df = pd.read_csv("scenario_1.csv")
    demand_scenarios = [1, 3, 1, 3]
    runs_per_demand_scenario = int(parameters_df["round"].max() / len(demand_scenarios))

    """"Creating auction class"""
    Auctions = AuctionGenerator(active_players=16)

    """"putting pre created scenario in """
    Auctions.store_input_parameters_csv(input_df=parameters_df)
    Auctions.change_rym_parameter(rym=1)
    Auctions.change_maximum_bid(maximum_bid=70)

    for demand in demand_scenarios:
        Auctions.change_demand_parameter(demand=demand)

        for itteration in range(runs_per_demand_scenario):
            print("round", itteration)
            Auctions.split_players_random()
            Auctions.input_parameters()

            for i in Auctions.players_dic:
                Auctions.players_dic[i].place_random_bid()

            Auctions.evaluate_round_per_group()
            Auctions.results_to_players()
            Auctions.store_round_results()

    Auctions.export_everything(name="scenario_1_rym")


if __name__ == '__main__':
    """creating input csv"""
    generate_random_parameters_to_csv(random_seed=16180339, name="scenario_1")

    """playing scenario"""
    scenario_1_no_rym()
    scenario_1_rym()






