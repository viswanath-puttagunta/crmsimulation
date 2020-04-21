import pandas as pd
from partner.partner import Partner
from partner_list import partner_list


def get_partner_df(partners_list):
    partner_tuples = []
    for partner_deets in partners_list:
        partner_tuples.append(partner_deets.get_partner_info())  # Returned a tuple per call

    return pd.DataFrame(partner_tuples, columns=['pid', 'name', 'size', 'location', 'p1_devs', 'p2_devs', 'alignment', 'partner_driven'])


def get_account_df(partners_list):
    account_tuples = []
    for partner_deets in partners_list:
        account_tuples = account_tuples + partner_deets.get_account_df()  # returned a list of tuples per call

    return pd.DataFrame(account_tuples, columns=['acc_id', 'name', 'size', 'location'])


def get_opportunity_df(partners_list):
    opportunity_tuples = []
    for partner_deets in partners_list:
        opportunity_tuples = opportunity_tuples + partner_deets.get_opportunity_df()  # returned a list of tuples per call

    return pd.DataFrame(opportunity_tuples, columns=['pid', 'acc_id', 'opp_id', 'opp_size', 'is_aligned'])


def get_fact_df(partners_list):
    fact_tuples = []
    for partner_deets in partners_list:
        fact_tuples = fact_tuples + partner_deets.get_fact_df()

    return pd.DataFrame(fact_tuples, columns=['pid', 'acc_id', 'opp_id', 'fact_id', 'stage_id', 'timestamp'])


# MAIN -----------------------------------------------------------------------------------------------------------------
def generate_csv():
    last_pid = 0
    last_acc_id = 0
    last_opp_id = 0
    last_fact_id = 0

    partners = []
    for partner in partner_list:
        new_partner = Partner(
            partner['name'],
            partner['size'],
            partner['location'],
            partner['location_list'],
            partner['acc_size_list'],
            partner['opp_sizes'],
            partner['alignment'],
            partner['gold_ratio'],
            partner['num_accounts'],
            partner['num_opps'],
            last_pid,
            last_acc_id,
            last_opp_id,
            last_fact_id,
            partner['partner_driven']
        )
        last_ids = new_partner.get_ids()
        last_pid = last_ids['pid']
        last_acc_id = last_ids['acc_id']
        last_opp_id = last_ids['opp_id']
        last_fact_id = last_ids['fact_id']

        partners.append(new_partner)

    with open('./output/partners.csv', 'w') as f:
        tdf = get_partner_df(partners)
        tdf.to_csv(f, index=False, line_terminator='\n', columns=['pid', 'name', 'size', 'location', 'p1_devs', 'p2_devs', 'alignment', 'partner_driven'])
        f.close()

    with open('./output/accounts.csv', 'w') as f:
        tdf = get_account_df(partners)
        tdf.to_csv(f, index=False, line_terminator='\n', columns=['acc_id', 'name', 'size', 'location'])
        f.close()

    with open('./output/opportunities.csv', 'w') as f:
        tdf = get_opportunity_df(partners)
        tdf.to_csv(f, index=False, line_terminator='\n', columns=['pid', 'acc_id', 'opp_id', 'opp_size', 'is_aligned'])
        f.close()

    with open('./output/facts.csv', 'w') as f:
        tdf = get_fact_df(partners)
        tdf.to_csv(f, index=False, line_terminator='\n', columns=['pid', 'acc_id', 'opp_id', 'fact_id', 'stage_id', 'timestamp'])
        f.close()
