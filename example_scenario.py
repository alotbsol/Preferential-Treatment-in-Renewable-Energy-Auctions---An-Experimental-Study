from auction import AuctionGenerator


def all_parameters():
    Auctions = AuctionGenerator(active_players=16)

    for rym_mbid in [[0, 90.3], [1, 70]]:
        Auctions.change_rym_parameter(rym=rym_mbid[0])
        Auctions.change_maximum_bid(maximum_bid=rym_mbid[1])

        for demand in [1, 3]:
            Auctions.change_demand_parameter(demand=demand)

            for itteration in range(100):
                print("round", itteration)
                Auctions.generate_parameters()
                Auctions.split_players()

                for i in Auctions.players_dic:
                   Auctions.players_dic[i].place_random_bid()

                Auctions.evaluate_round_per_group()
                Auctions.results_to_players()
                Auctions.store_round_results()

    Auctions.export_everything(name="example_scenario")


def example_figures():
    Auctions = AuctionGenerator(active_players=4, rym=0)
    Auctions.generate_parameters()

    for i in Auctions.players_dic:
        Auctions.players_dic[i].graph_project_input()


    Auctions2 = AuctionGenerator(active_players=2, rym=1)
    Auctions2.generate_parameters()

    for i in Auctions2.players_dic:
        Auctions2.players_dic[i].graph_project_input()


if __name__ == '__main__':
    """all_parameters()"""
    example_figures()


