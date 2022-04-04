import time
import pandas as pd
from bid import *
from create_agents import create_agents

start = time.time()

# Import Projects Database
excel_projects = pd.read_excel('db.xlsx', sheet_name='Projects')

# Create empty dataframes to be filled with results
df_bid_details = pd.DataFrame()
df_bid_results = pd.DataFrame()

# Projects Parameters
BID_ALPHA = 1  # Avg that represents amount of discount/overprice of projects
STD_ALPHA = 0.05  # Standard deviation of BID_ALPHA (follows a normal distr.)

# Agents Parameters
ATRAT_AVG = 0.50  # Normal distribution for ag_tamanho and ag_investimento
STD_DEV = 0.25  # Standard deviation of ATRAT_AVG
NUMBER_OF_AGENTS = 100  # Total number of agents bidding
MAX_ALPHA = 1.40  # Max value that agents are willing to go above fair bid price
ATRAT_LIM = 0.3  # Agent flexibility regarding projects selection
DISTRIBUTION = 'g'  # Type of parameters distribution: 'g' for normal; 'u' for uniform

# Governmennt Parameters
REATIVIDADE = 0  # How much the government is willing to reduce bid price
RERUNS = 1  # How many rebids are allowed

# Iteration Parameters
RUNS = 2000  # Number of iterations

print('Alpha selecionado: {}'.format(BID_ALPHA))

for run in range(RUNS):
    BID_NUMBER = 1
    print('Run number: {}'.format(run))
    df_projects = projects_index(BID_ALPHA, STD_ALPHA, excel_projects.copy())
    # df_agents = excel_agents.copy()
    df_agents = create_agents(
        ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS, MAX_ALPHA, DISTRIBUTION)
    df_picture = pd.DataFrame()

    while df_projects.shape[0] > 0:
        # for bids in range(df_projects.shape[0]):
        project_selected = project_select(df_projects)
        current_project = project_selected[0]
        df_projects = project_selected[1]
        # print(current_project)
        df_agents_select = agents_select(current_project, df_agents, ATRAT_LIM)

        bid_result = run_bids(df_projects, df_agents_select,
                              BID_NUMBER, current_project, df_agents, run,
                              REATIVIDADE, RERUNS)
        df_agents = bid_result[2]
        df_projects = bid_result[3]

        df_bid_details = pd.concat([df_bid_details, bid_result[0]])
        df_bid_results = pd.concat([df_bid_results, bid_result[1]])
        df_picture = pd.concat([df_picture, bid_result[1]])

        BID_NUMBER += 1
    print('FINAL RESULT')
    print(df_picture[['estado', 'pop_alvo', 'pop_alvo_ratio', 'agente', 'ag_max_alpha', 'outorga',
                      'ag_atratividade', 'agente_alpha_ofertado', 'bid',
                      'bid_number', 'reruns', 'run']])

# Export Final Databases
FILE_NAME = 'PJ-{}-{}-AG-{}-{}-{}-{}-{}-{}-GV-{}-{}-IT-{}'.format(
    BID_ALPHA, STD_ALPHA, ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS,
    MAX_ALPHA, ATRAT_LIM, DISTRIBUTION, REATIVIDADE, RERUNS, RUNS
)
print(FILE_NAME)
columns = ['par_bid_alpha', 'par_std_alpha', 'par_atrat_avg', 'par_std_dev',
           'par_number_of_agents', 'par_max_alpha', 'par_atrat_lim',
           'par_distribution',
           'par_reatividade', 'par_reruns', 'par_runs', 'file_name']
values = [BID_ALPHA, STD_ALPHA, ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS,
          MAX_ALPHA, ATRAT_LIM, DISTRIBUTION, REATIVIDADE, RERUNS, RUNS, FILE_NAME]

df_bid_details[columns] = values
df_bid_results[columns] = values
df_bid_details.to_csv(
    '/win/Users/faust/Documents/TCC_MBA/ABM_Project/Results_temp/Details-{}.csv'.format(
        FILE_NAME), index=False)
df_bid_results.to_csv(
    '/win/Users/faust/Documents/TCC_MBA/ABM_Project/Results_temp/Results-{}.csv'.format(
        FILE_NAME), index=False)

end = time.time()
exec_time = round((end - start)/60, 2)
print('Execution Time: ' + str(exec_time))

# Check total nobids
filter_pivot = (
    df_bid_results['agente'] == 'nobid'
)
df_pivot = df_bid_results.loc[filter_pivot, :].pivot_table(index='run',
                                                           values='pop_alvo_ratio',
                                                           aggfunc=np.sum)
# print(df_pivot)
print(df_pivot.mean())


df_pivot2 = df_bid_results.pivot_table(index='run',
                                       values='bid',
                                       aggfunc=np.sum)

print(df_pivot2.mean())
