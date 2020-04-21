import random
from config import config
from utils.utils import dprint
from opportunity.opportunity import Opportunity
from config.ml_model import Model


class Account(object):
    def __init__(self, largness_list, location_list, num_leads, alignment, aligned_list, p1_devs, p2_devs, opp_sizes, pid, last_acc_id=0, last_opp_id=0, last_fact_id=0, name="Lorem Ipsum", owner_driven=True):
        self.size = largness_list[random.randint(0, len(largness_list) - 1)]
        self.location = location_list[random.randint(0, len(location_list) - 1)]
        self.num_leads = num_leads  # Number of Opportunity instances to create
        # Given alignment and alignment delta, this generates an alignment within that range
        self.alignment = alignment  # normal float
        self.alignment_list = aligned_list
        self.opp_sizes = opp_sizes  # High/low tuple
        self.p1_devs = p1_devs
        self.p2_devs = p2_devs
        self.name = name
        self.owner_driven = owner_driven
        self.pid = int(pid)
        self.acc_id = int(last_acc_id) + 1
        self.last_opp_id = int(last_opp_id)
        self.last_fact_id = int(last_fact_id)
        self.intel_model = Model(self.opp_sizes, self.alignment, self.p1_devs, self.p2_devs)
        self.opp_list = self.intel_model.generate_opp_list(self.opp_sizes, self.num_leads)

        self.lead_opp_ids = []
        self.qualify_opp_ids = []
        self.solution_opp_ids = []
        self.num_proposals = None
        self.proposal_opp_ids = []
        self.finalize_opp_ids = []
        self.stage_list = []  # A map of what stage each opportunity makes it to

        for idx in range(self.last_opp_id + 1, self.last_opp_id + self.num_leads + 1):
            self.lead_opp_ids.append(idx)
            self.stage_list.append(1)

        random.shuffle(self.lead_opp_ids)
        dprint(self.lead_opp_ids)
        self.qualify_opp_ids = self.chop(self.lead_opp_ids, int(config.leadToQualifySuccessRate * len(self.lead_opp_ids)))
        dprint(self.qualify_opp_ids)
        self.solution_opp_ids = self.chop(self.qualify_opp_ids, int(config.qualifyToSolutionSuccessRate * len(self.qualify_opp_ids)))
        self.num_proposals = self.intel_model.intel_chop(len(self.solution_opp_ids))
        self.proposal_opp_ids = self.chop(self.solution_opp_ids, self.num_proposals)
        self.finalize_opp_ids = self.chop(self.proposal_opp_ids, int(config.proposalToFinalizeSuccessRate * len(self.proposal_opp_ids)))

        for idx in self.qualify_opp_ids:
            self.stage_list[self.lead_opp_ids.index(idx)] = 2

        for idx in self.solution_opp_ids:
            self.stage_list[self.lead_opp_ids.index(idx)] = 3

        for idx in self.proposal_opp_ids:
            self.stage_list[self.lead_opp_ids.index(idx)] = 4

        for idx in self.finalize_opp_ids:
            self.stage_list[self.lead_opp_ids.index(idx)] = 5

        self.opportunities = self.generate_opportunities()

    def chop(self, target_list, desired_length):
        chopped_list = target_list[0:desired_length]
        random.shuffle(chopped_list)
        return chopped_list

    def generate_opportunities(self):
        opportunities = []
        for idx, stage in enumerate(self.stage_list):
            # def __init__(self, opp_size, final_stage, pid, acc_id, last_opp_id=0, last_fact_id=0,):
            opportunity = Opportunity(self.opp_list[idx], self.alignment_list[idx], stage, self.pid, self.acc_id, self.last_opp_id, self.last_fact_id, self.owner_driven)
            last_ids = opportunity.get_last_ids()
            self.last_opp_id = last_ids['opp_id']
            self.last_fact_id = last_ids['fact_id']
            opportunities.append(opportunity)

        return opportunities

    def get_last_ids(self):
        return {
            'acc_id': int(self.acc_id),
            'opp_id': int(self.last_opp_id),
            'fact_id': int(self.last_fact_id)
        }

    def get_account_info(self):
        return self.acc_id, self.name, self.size, self.location

    def get_opportunity_df(self):
        opportunities = []
        for opportunity in self.opportunities:
            opportunities.append(opportunity.get_opportunity_info())
        return opportunities  # return list of tuples

    def get_fact_df(self):
        facts = []
        for opportunity in self.opportunities:
            facts = facts + opportunity.get_fact_df()
        return facts
