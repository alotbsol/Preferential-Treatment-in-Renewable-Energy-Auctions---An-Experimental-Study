from auction import AuctionGenerator
import pandas as pd


def all_parameters():
    Auctions = AuctionGenerator(active_players=16)

    for rym_mbid in [[0, 90.3], [1, 70]]:
        Auctions.change_rym_parameter(rym=rym_mbid[0])
        Auctions.change_maximum_bid(maximum_bid=rym_mbid[1])

        for demand in [1, 3]:
            Auctions.change_demand_parameter(demand=demand)

            for itteration in range(100):
                print("round", itteration)
                Auctions.generate_random_parameters()
                Auctions.split_players_random()

                for i in Auctions.players_dic:
                   Auctions.players_dic[i].place_random_bid()

                Auctions.evaluate_round_per_group()
                Auctions.results_to_players()
                Auctions.store_round_results()

    Auctions.export_everything(name="example_scenario")


def example_figures():
    parameters_df = pd.read_csv("scenario_1.csv")
    distributions_df = pd.read_csv("scenario_1_distribution.csv")

    Auctions = AuctionGenerator(parameters_df=parameters_df,
                                distributions_df=distributions_df,
                                active_players=4,
                                rym=0,)

    Auctions.split_players_random()
    Auctions.input_parameters_to_players()

    for i in Auctions.players_dic:
        Auctions.players_dic[i].graph_project_input()

    Auctions = AuctionGenerator(parameters_df=parameters_df,
                                distributions_df=distributions_df,
                                active_players=2,
                                rym=1)

    for i in Auctions.players_dic:
        Auctions.players_dic[i].graph_project_input()


if __name__ == '__main__':
    example_figures()


