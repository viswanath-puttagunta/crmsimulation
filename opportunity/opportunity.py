import datetime
import random
from config import config
from fact.fact import Fact


class Opportunity(object):
    # A number of these will be generated from the Account parent
    def __init__(self, opp_size, is_aligned, final_stage, pid, acc_id, last_opp_id=0, last_fact_id=0, owner_driven=True):
        self.opp_id = int(last_opp_id) + 1
        self.acc_id = int(acc_id)
        self.pid = int(pid)
        self.opp_size = opp_size
        self.is_aligned = is_aligned
        self.owner_driven = owner_driven
        self.final_stage = int(final_stage)
        self.create_date = self.get_random_date()
        self.last_fact_id = last_fact_id
        self.facts = self.generate_facts()

    def get_random_date(self):
        total_days = (config.leadEndDate - config.leadStartDate).days
        random_days = random.randint(1, total_days)
        return config.leadStartDate + datetime.timedelta(days=random_days)

    def add_to_date(self, start_date, delta):
        day = random.randint(delta[0] - delta[1], delta[0] + delta[1])
        return start_date + datetime.timedelta(days=day)

    def generate_facts(self):
        # def __init__(self, fact_id, opp_id, acc_id, pid, stage, timestamp):
        self.last_fact_id = self.last_fact_id + 1
        facts = [Fact(self.last_fact_id, self.opp_id, self.acc_id, self.pid, 1, self.create_date)]
        tmp_date = self.create_date
        for x in range(2, self.final_stage + 1):
            new_date = self.add_to_date(tmp_date, config.deltas[x-2])
            tmp_date = new_date
            self.last_fact_id = self.last_fact_id + 1
            facts.append(Fact(self.last_fact_id, self.opp_id, self.acc_id, self.pid, x, tmp_date))
        return facts

    def get_last_ids(self):
        return {
            'fact_id': int(self.last_fact_id),
            'opp_id': int(self.opp_id)
        }

    def get_opportunity_info(self):
        return self.pid, self.acc_id, self.opp_id, self.opp_size, self.is_aligned

    def get_fact_df(self):
        facts = []
        for fact in self.facts:
            facts.append(fact.get_fact_info())
        return facts  # returned list of tuples
