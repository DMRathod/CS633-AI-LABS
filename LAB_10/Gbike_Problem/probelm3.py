import main as gb
import matplotlib.pyplot as mtplt
import seaborn as sbn
import numpy as np
import math


class gbike_q3(gb.Gbike):
    def __init__(self):
        gb.Gbike.__init__(self)
        self.__max_gbike_num_per_parking_lot = 10
        self.__parking_cost = 4

    def _get_action_cost(self, action):
        if action == -1:
            return 0
        else:
            return abs(action) * self._transfer_cost_per_gbike

    def __get_parking_cost(self, gbike_num):
        if gbike_num > self.__max_gbike_num_per_parking_lot:
            return self.__parking_cost
        else:
            return 0

    def _calculate_Vs_by_policy(self, Vs, gbike_num1_in_evening, gbike_num2_in_evening, action):
        tmp_vs = 0.0
        prob_of_requested_car_num1 = 0
        prob_of_requested_car_num2 = 0
        prob_of_returned_car_num1 = 0
        prob_of_returned_car_num2 = 0
        gbike_num1_in_next_morning = max(0, min(gbike_num1_in_evening - action, self._max_gbike_num))
        gbike_num2_in_next_morning = max(0, min(gbike_num2_in_evening + action, self._max_gbike_num))
        rented_gbike_num1 = 0
        rented_gbike_num2 = 0
        gbike_num1_in_next_evening = 0
        gbike_num2_in_next_evening = 0
        action_cost = self._get_action_cost(action)
        parking_cost1 = self.__get_parking_cost(gbike_num1_in_next_morning)
        parking_cost2 = self.__get_parking_cost(gbike_num2_in_next_morning)

        for requested_gbike_num1 in range(0, gbike_num1_in_next_morning + 1):
            if requested_gbike_num1 >= gbike_num1_in_next_morning:
                # This case stands for all the request car numbers larger then the car number in next morning.
                prob_of_requested_gbike_num1 = self._req_over_boundary_prob1[gbike_num1_in_next_morning]
            else:
                prob_of_requested_gbike_num1 = self._requested_prob1[requested_gbike_num1]
            rented_gbike_num1 = min(requested_gbike_num1, gbike_num1_in_next_morning)

            for requested_gbike_num2 in range(0, gbike_num2_in_next_morning + 1):
                if requested_gbike_num2 >= gbike_num2_in_next_morning:
                    # This case stands for all the request car numbers larger then the car number in next morning.
                    prob_of_requested_gbike_num2 = self._req_over_boundary_prob2[gbike_num2_in_next_morning]
                else:
                    prob_of_requested_gbike_num2 = self._requested_prob2[requested_gbike_num2]
                rented_gbike_num2 = min(requested_gbike_num2, gbike_num2_in_next_morning)
                reward = self._get_rental_reward(requested_gbike_num1,
                                                 gbike_num1_in_next_morning) + self._get_rental_reward(requested_gbike_num2,
                                                                                                     gbike_num2_in_next_morning) \
                         - action_cost - parking_cost1 - parking_cost2

                ret_num1_to_boundary = self._max_gbike_num - (gbike_num1_in_next_morning - rented_gbike_num1)
                for returned_gbike_num1 in range(0, ret_num1_to_boundary + 1):
                    if returned_gbike_num1 >= ret_num1_to_boundary:
                        # This case stands for all the returned numbers larger then ret_num1_to_boundary
                        prob_of_returned_gbike_num1 = self._ret_over_boundary_prob1[ret_num1_to_boundary]
                    else:
                        prob_of_returned_gbike_num1 = self._returned_prob1[returned_gbike_num1]
                    gbike_num1_in_next_evening = min(gbike_num1_in_next_morning - rented_gbike_num1 + returned_gbike_num1,
                                                   self._max_gbike_num)

                    ret_num2_to_boundary = self._max_gbike_num - (gbike_num2_in_next_morning - rented_gbike_num2)
                    for returned_gbike_num2 in range(0, ret_num2_to_boundary + 1):
                        if returned_gbike_num2 >= ret_num2_to_boundary:
                            # This case stands for all the returned numbers larger then ret_num2_to_boundary
                            prob_of_returned_gbike_num2 = self._ret_over_boundary_prob2[ret_num2_to_boundary]
                        else:
                            prob_of_returned_gbike_num2 = self._returned_prob2[returned_gbike_num2]
                        gbike_num2_in_next_evening = min(gbike_num2_in_next_morning - rented_gbike_num2 + returned_gbike_num2,
                                                       self._max_gbike_num)

                        prob = prob_of_requested_gbike_num1 * prob_of_requested_gbike_num2 \
                               * prob_of_returned_gbike_num1 * prob_of_returned_gbike_num2
                        tmp_vs += prob * (reward + self._gamma * Vs[gbike_num1_in_next_evening][gbike_num2_in_next_evening])

        return tmp_vs


if __name__ == '__main__':

    gbike3_instance = gbike_q3()
    gbike3_instance.policy_iteration(True)
    history_policy = gbike3_instance.history_policy
    value = gbike3_instance.Vs
    policy_num = len(history_policy)
    row = math.ceil((policy_num + 1) / 3)
    fig, axes = mtplt.subplots(row, 3, figsize=(20, row * 5))
    mtplt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.3)
    axes = axes.flatten()

    for i in range(0, policy_num):
        sbn_fig = sbn.heatmap(np.flipud(history_policy[i]), ax=axes[i])
        sbn_fig.set_ylabel("cars at first location")
        sbn_fig.set_xlabel("cars at second location")
        sbn_fig.set_title(r"$\pi${}".format(i))
        sbn_fig.set_yticks(list(reversed(range(0, gbike3_instance.max_gbike_num + 1))))
        sbn_fig.tick_params(labelsize=8)

    sbn_fig = sbn.heatmap(np.flipud(value), ax=axes[-1], cmap="YlGnBu")
    sbn_fig.set_ylabel("cars at first location")
    sbn_fig.set_xlabel("cars at second location")
    sbn_fig.set_title(r"$v_*$")
    sbn_fig.set_yticks(list(reversed(range(0, gbike3_instance.max_gbike_num + 1))))
    sbn_fig.tick_params(labelsize=8)

    mtplt.show()
    mtplt.close()
