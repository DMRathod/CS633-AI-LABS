import scipy.stats as sci_stats
import numpy as np
# import matplotlib as mpltlib
import matplotlib.pyplot as mtplt
import seaborn as sbn
import math

class Gbike:
    def __init__(self):
        self.__init__all()

    def __init__all(self):
        self._max_gbike_num = 20 # maximum car number for each location
        self._gamma = 0.9      # discount rate
        self.__max_transfer_gbike_num = 5
        self.__accuracy = 0.01
        self._transfer_cost_per_gbike = 2
        self.__rental_credit_per_gbike = 10

        #Initialize policy and V(s) as zeros in 21X21 table, becauseof no more than 20 cars for each loaction
        self.__Vs = np.zeros((self._max_gbike_num + 1,self._max_gbike_num + 1))
        self.__policy = np.zeros(self.__Vs.shape, dtype = np.int32)

        #Record policy changes in iteration
        self.__history_policy = []

        # Record policy changes in iteration
        self.__history_policy = []

        self._requested_prob1 = self.__init_probabilities(self._max_gbike_num + 1, 3)
        self._returned_prob1 = self.__init_probabilities(self._max_gbike_num + 1, 3)
        self._requested_prob2 = self.__init_probabilities(self._max_gbike_num + 1, 4)
        self._returned_prob2 = self.__init_probabilities(self._max_gbike_num + 1, 2)

        # The probability that the request car number >= the car number in the morning.
        self._req_over_boundary_prob1 = self.__init_over_boundary_prob(self._requested_prob1)
        self._req_over_boundary_prob2 = self.__init_over_boundary_prob(self._requested_prob2)
        # The probability that the returned car number makes the car number >= the maximum car num in the evening.
        self._ret_over_boundary_prob1 = self.__init_over_boundary_prob(self._returned_prob1)
        self._ret_over_boundary_prob2 = self.__init_over_boundary_prob(self._returned_prob2)

    def __init_probabilities(self, array_size, poisson_lambda):
        arr = np.zeros(array_size)
        for i in range(0, array_size):
            arr[i] = sci_stats.poisson.pmf(k=i, mu=poisson_lambda)
        return arr

    def __init_over_boundary_prob(self, prob_in_boundary):

        # For example, when requested car number is 3, #
        # the car number in morning is 2, the self._req_over_boundary_prob1[2] stands for
        # all the request car number that makes the remain car number is 0,
        # include requested car number is 2, 3, 4 & ...
        # so self._req_over_boundary_prob1[2] = 1 - self._requseted_prob1[0]- self._requseted_prob1[1]
        prob = np.zeros(len(prob_in_boundary) + 1)
        tmp = 0
        prob[0] = 1
        for i in range(1, len(prob_in_boundary) + 1):
            tmp += prob_in_boundary[i - 1]
            prob[i] = 1 - tmp
        return prob

    def _get_rental_reward(self, request_num, gbike_num):
        return min(self._max_gbike_num, min(request_num, gbike_num)) * self.__rental_credit_per_gbike

    def _get_action_cost(self, action):
        return abs(action) * self._transfer_cost_per_gbike

    def _calculate_Vs_by_policy(self, Vs, gbike_num1_in_evening, gbike_num2_in_evening, action):
        tmp_vs = 0.0
        prob_of_requested_gbike_num1 = 0
        prob_of_requested_gbike_num2 = 0
        prob_of_returned_gbike_num1 = 0
        prob_of_returned_gbike_num2 = 0
        gbike_num1_in_next_morning = max(0, min(gbike_num1_in_evening - action, self._max_gbike_num))
        gbike_num2_in_next_morning = max(0, min(gbike_num2_in_evening + action, self._max_gbike_num))
        rented_gbike_num1 = 0
        rented_gbike_num2 = 0
        gbike_num1_in_next_evening = 0
        gbike_num2_in_next_evening = 0
        action_cost = self._get_action_cost(action)

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
                                                 gbike_num1_in_next_morning) + self._get_rental_reward(
                    requested_gbike_num2, gbike_num2_in_next_morning) \
                         - action_cost

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
                        gbike_num2_in_next_evening = min(
                            gbike_num2_in_next_morning - rented_gbike_num2 + returned_gbike_num2, self._max_gbike_num)

                        prob = prob_of_requested_gbike_num1 * prob_of_requested_gbike_num2 \
                               * prob_of_returned_gbike_num1 * prob_of_returned_gbike_num2
                        tmp_vs += prob * (
                                    reward + self._gamma * Vs[gbike_num1_in_next_evening][gbike_num2_in_next_evening])

                return tmp_vs

    def __calculate_Vs(self, Vs, gbike_num1_in_evening, gbike_num2_in_evening):
        return self._calculate_Vs_by_policy(Vs, gbike_num1_in_evening, gbike_num2_in_evening,
                                            self.__policy[gbike_num1_in_evening][gbike_num2_in_evening])

    def __policy_evaluation(self):
        delta = self.__accuracy + 1  # initialize delta to a number larger than accuracy to enable while loop.
        while delta >= self.__accuracy:
            delta = 0.0  # reinitialize delta to 0
            Vs = self.__Vs.copy()
            for gbike_num1_in_evening in range(0, self._max_gbike_num + 1):
                for gbike_num2_in_evening in range(0, self._max_gbike_num + 1):
                    v = self.__Vs[gbike_num1_in_evening][gbike_num2_in_evening]
                    self.__Vs[gbike_num1_in_evening][gbike_num2_in_evening] = self.__calculate_Vs(Vs,gbike_num1_in_evening,
                                                                                              gbike_num2_in_evening)
                    err = abs(v - self.__Vs[gbike_num1_in_evening][gbike_num2_in_evening])
                    delta = max(delta, err)
            # print(self.__Vs)
            print('delta = {}'.format(delta))

    def __argmax_a_for_Vs(self, gbike_num1, gbike_num2):
        a = -gbike_num2
        vs = self._calculate_Vs_by_policy(self.__Vs, gbike_num1, gbike_num2, a)
        for i in range(-gbike_num2 + 1, gbike_num1 + 1):
            tmp_vs = self._calculate_Vs_by_policy(self.__Vs, gbike_num1, gbike_num2, i)
            if tmp_vs > vs:
                a = i
                vs = tmp_vs
        return a, vs

    def __policy_improvement(self):
        policy_stable = True
        for i in range(0, self._max_gbike_num + 1):
            for j in range(0, self._max_gbike_num + 1):
                old_policy = self.__policy[i][j]
                old_vs = self.__Vs[i][j]
                self.__policy[i][j], vs = self.__argmax_a_for_Vs(i, j)
                if self.__policy[i][j] != old_policy and abs(old_vs - vs) > self.__accuracy:
                    policy_stable = False
        return policy_stable

    def policy_iteration(self, bRecord_iteration_history):
        self.__init__all()
        policy_stable = False
        if bRecord_iteration_history:
            self.__history_policy.append(self.__policy.copy())
        while not policy_stable:
            self.__policy_evaluation()
            policy_stable = self.__policy_improvement()
            print(self.__policy)
            if bRecord_iteration_history:
                self.__history_policy.append(self.__policy.copy())

    @property
    def policy(self):
        return self.__policy

    @property
    def history_policy(self):
        return self.__history_policy

    @property
    def max_gbike_num(self):
        return self._max_gbike_num

    @property
    def Vs(self):
        return self.__Vs


if __name__ == '__main__':

    gbike_instance = Gbike()
    gbike_instance.policy_iteration(True)
    history_policy = gbike_instance.history_policy
    value = gbike_instance.Vs
    policy_num = len(history_policy)
    row = int(math.ceil((policy_num + 1) / 3))
    fig, axes = mtplt.subplots(row, 3, figsize=(20, row * 5))
    mtplt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.3)
    axes = axes.flatten()

    for i in range(0, policy_num):
        sbn_fig = sbn.heatmap(np.flipud(history_policy[i]), ax=axes[i])
        sbn_fig.set_ylabel("cars at first location")
        sbn_fig.set_xlabel("cars at second location")
        sbn_fig.set_title(r"$\pi${}".format(i))
        sbn_fig.set_yticks(list(reversed(range(0, gbike_instance.max_car_num + 1))))
        sbn_fig.tick_params(labelsize=8)

    sbn_fig = sbn.heatmap(np.flipud(value), ax=axes[-1], cmap="YlGnBu")
    sbn_fig.set_ylabel("cars at first location")
    sbn_fig.set_xlabel("cars at second location")
    sbn_fig.set_title(r"$v_*$")
    sbn_fig.set_yticks(list(reversed(range(0, gbike_instance.max_car_num + 1))))
    sbn_fig.tick_params(labelsize=8)

    mtplt.show()
    mtplt.close()
