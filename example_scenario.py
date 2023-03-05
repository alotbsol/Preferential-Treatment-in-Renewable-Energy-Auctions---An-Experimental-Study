from auction import AuctionGenerator
import pandas as pd


def example_figures():
    parameters_df = pd.read_csv("scenario_1.csv")
    distributions_df = pd.read_csv("scenario_1_distribution.csv")

    Auctions = AuctionGenerator(parameters_df=parameters_df,
                                distributions_df=distributions_df,
                                active_players=8,
                                rym=0,)

    Auctions.split_players_random()
    Auctions.input_parameters_to_players()

    for i in Auctions.players_dic:
        Auctions.players_dic[i].graph_project_input()

    Auctions2 = AuctionGenerator(parameters_df=parameters_df,
                                distributions_df=distributions_df,
                                active_players=4,
                                rym=1)

    Auctions2.split_players_random()
    Auctions2.input_parameters_to_players()

    for i in Auctions2.players_dic:
        print(i)
        Auctions2.players_dic[i].graph_project_input()


if __name__ == '__main__':
    example_figures()


