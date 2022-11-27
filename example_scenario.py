from auction import AuctionGenerator


if __name__ == '__main__':
    Auctions = AuctionGenerator(active_players=16)

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
