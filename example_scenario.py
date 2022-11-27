from auction import AuctionGenerator


if __name__ == '__main__':
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

    # change rym
    # change demand
