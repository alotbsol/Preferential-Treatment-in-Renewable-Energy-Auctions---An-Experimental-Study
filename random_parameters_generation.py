import random as random
import pandas as pd


def generate_random_parameters_to_csv(no_groups=4, plyers_per_group=4, no_rounds=100,
                                      ws_min=5, ws_max=9,
                                      oc_min=0.8, oc_max=1.2,
                                      random_seed=16180339,
                                      name="scenario_x"):
    random.seed(random_seed)

    parameters_dic = {"round": [],
                      "group": [],
                      "player_slot": [],
                      "ws": [],
                      "other_costs": [],
                      }

    current_round = 0

    for iii in range(no_rounds):
        current_round += 1
        current_group = 0
        for ii in range(no_groups):
            current_group += 1
            current_player = 0
            for i in range(plyers_per_group):
                current_player += 1
                """random generation of parameters"""
                ws = random.randint(ws_min * 10, ws_max * 10) / 10
                other_costs = random.randint(oc_min * 100, oc_max * 100) / 100

                parameters_dic["round"].append(current_round)
                parameters_dic["group"].append(current_group)
                parameters_dic["player_slot"].append(current_player)
                parameters_dic["ws"].append(ws)
                parameters_dic["other_costs"].append(other_costs)

    print(parameters_dic)

    df_out = pd.DataFrame.from_dict(parameters_dic)
    df_out.to_csv("{}.csv".format(name))

    print(df_out)


if __name__ == '__main__':
    generate_random_parameters_to_csv(random_seed=16180339, name="scenario_1")
    generate_random_parameters_to_csv(random_seed=1618033, name="scenario_2")
    generate_random_parameters_to_csv(random_seed=161803, name="scenario_3")
    generate_random_parameters_to_csv(random_seed=16180, name="scenario_4")


