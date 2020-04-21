import random
from config import config
from account.account import Account
from utils.lipsum import Lipsum


class Partner(object):
    def __init__(
                    self,
                    name,
                    size,
                    location,
                    location_list,
                    acc_size_list,
                    opp_sizes,
                    alignment,
                    gold_ratio,
                    num_accounts=20,
                    num_opps=50,
                    last_pid=0,
                    last_acc_id=0,
                    last_opp_id=0,
                    last_fact_id=0,
                    partner_driven=True
                ):
        self.name = name
        self.size = size  # str containing small, medium, or large
        self.location = location
        self.location_list = location_list
        self.acc_size_list = acc_size_list  # A list of strings of account sizes this partner will consider. Account object will pick one itself at random
        self.opp_sizes = opp_sizes  # high/low tuple to pass down to the account
        self.alignment = alignment  # normalized float
        self.gold_ratio = gold_ratio  # desired ratio of the p1 to p2 dev to pass down
        self.p2_devs = random.randint(config.p2_dev_range[self.size][0], config.p2_dev_range[self.size][1])
        self.p1_devs = int(round(self.p2_devs * self.gold_ratio))
        self.num_accounts = num_accounts  # How many Account instances to generate off this Partner
        self.num_opps = num_opps  # How many Opportunity(s) each Account instance should generate
        self.lipsum = Lipsum()

        self.pid = int(last_pid) + 1
        self.last_acc_id = int(last_acc_id)
        self.last_opp_id = int(last_opp_id)
        self.last_fact_id = int(last_fact_id)
        self.partner_driven = partner_driven

        self.accounts = self.generate_accounts()

    def generate_accounts(self):
        accounts = []
        alignment_list = []
        num_aligned = int(self.num_accounts * self.num_opps * self.alignment)

        for idx in range(1, (self.num_accounts * self.num_opps) + 1):
            alignment_list.append(True if idx < num_aligned else False)
        random.shuffle(alignment_list)

        for idx in range(1, self.num_accounts + 1):
            name = self.lipsum.get_name()
            account = Account(self.acc_size_list,
                              self.location_list,
                              self.num_opps,
                              self.alignment,
                              alignment_list[((idx - 1) * self.num_opps):(idx * self.num_opps)],
                              self.p1_devs,
                              self.p2_devs,
                              self.opp_sizes,
                              self.pid,
                              self.last_acc_id,
                              self.last_opp_id,
                              self.last_fact_id,
                              name,
                              self.partner_driven)
            last_ids = account.get_last_ids()
            self.last_acc_id = last_ids['acc_id']
            self.last_opp_id = last_ids['opp_id']
            self.last_fact_id = last_ids['fact_id']
            accounts.append(account)

        return accounts

    def get_ids(self):
        return {
            'pid': int(self.pid),
            'acc_id': int(self.last_acc_id),
            'opp_id': int(self.last_opp_id),
            'fact_id': int(self.last_fact_id)
        }

    def get_partner_info(self):
        return self.pid, self.name, self.size, self.location, self.p1_devs, self.p2_devs, self.alignment, self.partner_driven  # Return tuple

    def get_account_df(self):
        accounts = []
        for account in self.accounts:
            accounts.append(account.get_account_info())
        return accounts  # Return list of tuples

    def get_opportunity_df(self):
        opportunities = []
        for account in self.accounts:
            opportunities = opportunities + account.get_opportunity_df()
        return opportunities  # return list of tuples

    def get_fact_df(self):
        facts = []
        for account in self.accounts:
            facts = facts + account.get_fact_df()
        return facts  # return list of tuples
