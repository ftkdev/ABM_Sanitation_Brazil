import pandas as pd
from bid import *
from create_agents import create_agents

# Import Projects Database
excel_projects = pd.read_excel('db.xlsx', sheet_name='Projects')

# Create empty dataframes to be filled with results
df_bid_details = pd.DataFrame()
df_bid_results = pd.DataFrame()

# Projects Parameters
BID_ALPHA = 1  # Avg that represents amount of discount/overprice of projects
STD_ALPHA = 0.1  # Standard deviation of BID_ALPHA (follows a normal distr.)

# Agents Parameters
ATRAT_AVG = 2.5  # Avg Atratividade that the agents are normally distributed
STD_DEV = 0.25  # Standard deviation of ATRAT_AVG
NUMBER_OF_AGENTS = 35  # Total number of agents bidding
MAX_ALPHA = 1.4  # Max value that agents are willing to go above fair bid price
ATRAT_RANGE = 0.1

# Governmennt Parameters
REATIVIDADE = 0.1  # How much the government is willing to reduce bid price

# Iteration Parameters
RUNS = 1000  # Number of iterations

print('Alpha selecionado: {}'.format(BID_ALPHA))

for run in range(RUNS):
    BID_NUMBER = 1
    print('Run number: {}'.format(run))
    df_projects = projects_index(BID_ALPHA, STD_ALPHA, excel_projects.copy())
    # df_agents = excel_agents.copy()
    df_agents = create_agents(
        ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS, MAX_ALPHA, ATRAT_RANGE)
    df_picture = pd.DataFrame()

    while df_projects.shape[0] > 0:
        # for bids in range(df_projects.shape[0]):
        project_selected = project_select(df_projects)
        current_project = project_selected[0]
        df_projects = project_selected[1]
        # print(current_project)
        df_agents_select = agents_select(current_project, df_agents)

        bid_result = run_bids(df_projects, df_agents_select,
                              BID_NUMBER, current_project, df_agents, run, REATIVIDADE)
        df_agents = bid_result[2]
        df_projects = bid_result[3]

        df_bid_details = pd.concat([df_bid_details, bid_result[0]])
        df_bid_results = pd.concat([df_bid_results, bid_result[1]])
        df_picture = pd.concat([df_picture, bid_result[1]])

        BID_NUMBER += 1
    print('FINAL RESULT')
    print(df_picture[['estado', 'pop_alvo', 'agente', 'agente_alpha_max', 'outorga',
                      'projeto_outorga', 'agente_alpha_ofertado', 'bid',
                      'bid_number', 'reruns', 'run']])

df_bid_details.to_csv(
    '/win/Users/faust/Documents/TCC_MBA/ABM_Project/Results/bid_details001.csv', index=False)
df_bid_results.to_csv(
    '/win/Users/faust/Documents/TCC_MBA/ABM_Project/Results/bid_results001.csv', index=False)
# filt = (
    # df_bid_results['agente'] == 'nobid'
# )
# print(df_bid_results.loc[filt, :].pivot_table(index='run', values='pop_alvo',
                                              # aggfunc=np.sum))
