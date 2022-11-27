from auction import AuctionGenerator


if __name__ == '__main__':
    Auctions = AuctionGenerator(active_players=16)

    for itterations in range(100):
        Auctions.generate_parameters()

        for i in Auctions.players_dic:
            print("generated parameters:", i, Auctions.players_dic[i].parameters)

        for i in Auctions.players_dic:
           Auctions.players_dic[i].place_random_bid()
           print("placed bid:", i, Auctions.players_dic[i].my_bid)

        Auctions.split_players()
        Auctions.evaluate_round_per_group()
        Auctions.results_to_players()
        Auctions.store_round_results()

    Auctions.export_everything()
