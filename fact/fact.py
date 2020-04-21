class Fact(object):
    # 1-5 of these will be generated based on how far the Opportunity parent gets
    def __init__(self, fact_id, opp_id, acc_id, pid, stage, timestamp):
        self.fact_id = int(fact_id)
        self.opp_id = int(opp_id)
        self.acc_id = int(acc_id)
        self.pid = int(pid)
        self.stage = int(stage)
        self.timestamp = timestamp

    def get_fact_info(self):
        return self.pid, self.acc_id, self.opp_id, self.fact_id, self.stage, self.timestamp
