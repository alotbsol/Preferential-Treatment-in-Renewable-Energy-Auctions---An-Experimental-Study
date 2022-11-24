from math import log
import numpy as np

class GenerateDistributions:
    def __init__(self, min_ws=5, max_ws=9, base_lcoe=50):
        self.min_ws = min_ws
        self.max_ws = max_ws
        self.base_lcoe = base_lcoe

        # https://en.wind-turbine-models.com/turbines/832-enercon-e-115-3.000
        self.power_curve = [0, 0, 3, 48, 155, 339, 627, 1035, 1549, 2090,
                            2580, 2900, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000,
                            3000, 3000, 3000, 3000, 3000, 3000, 0, 0, 0, 0, 0]

        self.hub_height = 128
        self.hours = 8760
        self.losses = 0.8

        self.distribution = {"ws": [],
                             "production": [],
                             "site_quality": [],
                             "correction_factor": [],
                             "lcoe": []}

        self.create_ws_dist()



    def create_ws_dist(self):
        scale = 10

        generated_list = [i for i in range(self.min_ws*scale, self.max_ws*scale + 1)]
        generated_list = [i/scale for i in generated_list]

        self.distribution["ws"] = generated_list

    def calculate_wsHH(self, ws100_input):
        reference_hub = 100
        roughness_length = 0.1

        return ws100_input*(log(self.hub_height/roughness_length)/log(reference_hub/roughness_length))

    def calculate_production(self, ws_input):
        wind_speed_dist = []

        constant = 1.12
        a = 2
        b = ws_input * constant
        x_min = 1
        x_max = 30
        e = np.exp(1)

        val = 0
        for i in range(x_min, x_max):
            cumulative = (1 - e ** -(i / b) ** a)

            wind_speed_dist.append(cumulative - val)
            val = cumulative

        production_list = []

        for i in range(0, len(wind_speed_dist)):
            production_list.append(((self.power_curve[i] + self.power_curve[i+1])/2) * wind_speed_dist[i]
                                   * self.hours * self.losses)

        return sum(production_list)/1000

    def calc_production(self):
        pass

    def calc_correction_f(self):
        pass

    def calc_lcoe(self):
        pass




if __name__ == '__main__':
    Distributions = GenerateDistributions()
    print(Distributions.distribution)


