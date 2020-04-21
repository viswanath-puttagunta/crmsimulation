import numpy as np
import random
from utils.utils import dprint


class Model(object):
    def __init__(self, opp_sizes, alignment, p1=120, p2=40):
        self.bias = 0.2
        self.aligned_c = -0.6
        self.p1_c = 0.005
        self.p2_c = 0.05
        self.p1p2_c = -0.6

        self.opp_sizes = opp_sizes
        self.alignment = alignment
        self.p1_devs = p1
        self.p2_devs = p2
        self.aligned_prob = self.calc_prob(1)
        self.unaligned_prob = self.calc_prob(0)

    def calc_prob(self, is_aligned):
        lnr = self.bias + self.aligned_c * (1 - is_aligned) + self.p1_c * self.p1_devs + self.p2_c * self.p2_devs + self.p1p2_c * ((3 - (self.p1_devs / self.p2_devs)) ** 2)
        elnr = np.exp(-lnr)
        prob = 1 / (1 + elnr)
        dprint("Truth: {}; p1: {}, p2: {}\nlnr: {}\nelnr: {}\nprob: {}".format(is_aligned, self.p1_devs, self.p2_devs, lnr, elnr, prob))
        dprint("--------------------------------")
        return prob

    def generate_opp_list(self, opp_sizes, num_leads):
        opsize1_n = int(num_leads * 0.5)
        opsize2_n = num_leads - opsize1_n
        opsize_list = list(np.random.normal(opp_sizes[0], opp_sizes[0] / 10, opsize1_n)) + \
            list(np.random.normal(opp_sizes[1], opp_sizes[1] / 10, opsize2_n))
        opsize_list = [abs(int(x)) for x in opsize_list]
        random.shuffle(opsize_list)
        return opsize_list  # A list of single floats related to the value of the opportunity

    def intel_chop(self, num_proposals):
        # Aligned Opportunities
        num_aligned_ops = int(num_proposals * self.alignment)
        num_unaligned_ops = num_proposals - num_aligned_ops
        # isAlignedList = [1 for x in range(num_aligned_ops)] + [0 for x in range(num_unaligned_ops)]

        is_aligned_win = int(num_aligned_ops * self.aligned_prob)
        # is_aligned_loss = num_aligned_ops - is_aligned_win
        #
        is_not_aligned_win = int(num_unaligned_ops * self.unaligned_prob)
        # is_not_aligned_loss = num_unaligned_ops - is_not_aligned_win

        # won = [1 for x in range(is_aligned_win)] + [0 for x in range(is_aligned_loss)] \
        #       + [1 for x in range(is_not_aligned_win)] + [0 for x in range(is_not_aligned_loss)]
        return is_aligned_win + is_not_aligned_win  # This determines how many advance to stage 4
