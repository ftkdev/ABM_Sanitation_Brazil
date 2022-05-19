import time
import pandas as pd
from bid import *
from create_agents import create_agents

# Initialization
start = time.time()
np.random.seed(0)

# Import Projects Database
excel_projects = pd.read_csv('projects.csv')

# Create empty dataframes to be filled with results
df_bid_details = pd.DataFrame()
df_bid_results = pd.DataFrame()

# Projects Parameters
# [Vpj] Avg that represents amount of discount/overprice of projects
alpha_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
# [Spj] Standard deviation of BID_ALPHA (follows a normal distr.)
STD_ALPHA = 0.05

# Agents Creation Parameters
NUMBER_OF_AGENTS = 25  # [N] Total number of agents bidding
# [Mag] Max value that agents are willing to go above fair bid price
MAX_ALPHA = 1.40
ATRAT_LIM = 0.3  # [L] Agent flexibility regarding projects selection
ATRAT_AVG = 0.50  # Normal distribution for ag_tamanho and ag_investimento
STD_DEV = 0.25  # Standard deviation of ATRAT_AVG
DISTRIBUTION = 'g'  # Type of [L] distribution: 'g' for normal; 'u' for uniform

# Governmennt Parameters
# [R] How much the government is willing to reduce bid price
reat_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
RERUNS = 1  # How many rebids are allowed

# Iteration Parameters
RUNS = 1000  # Number of iterations

# print('Alpha selecionado: {}'.format(BID_ALPHA))

for BID_ALPHA in alpha_list:
    for REATIVIDADE in reat_list:
        df_bid_details = pd.DataFrame()
        df_bid_results = pd.DataFrame()
        for run in range(RUNS):
            BID_NUMBER = 1
            print('Run number: {}'.format(run))
            df_projects = projects_index(
                BID_ALPHA, STD_ALPHA, excel_projects.copy())
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
                df_agents_select = agents_select(
                    current_project, df_agents, ATRAT_LIM)

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
        # FILE_NAME = 'Vpj{}Spj{}Vag{}Sag{}N{}Mag{}L{}D{}R{}T{}It{}'.format(
        # FILE_NAME = 'Vpj{:.2f}Spj{:.2f}Vag{:.2f}Sag{:.2f}N{:0>3d}Mag{:.2f}L{:.2f}D{}R{:.2f}T{:0>2d}It{:0>4d}'.format(
        FILE_NAME = 'Vpj{:.2f}Spj{:.2f}Vag{:.2f}Sag{:.2f}N{:0>3d}Mag{:.2f}L{:.2f}D{}R{:.2f}T{:0>2d}It{:0>4d}'.format(
            BID_ALPHA, STD_ALPHA, ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS,
            MAX_ALPHA, ATRAT_LIM, DISTRIBUTION, REATIVIDADE, RERUNS, RUNS
        )
        # FILE_NAME = 'Vpj{}Spj{}N{}Mag{}L{}Vag{}Sag{}D{}R{}T{}It{}'.format(
        # # FILE_NAME = 'PJ-{}-{}-AG-{}-{}-{}-{}-{}-{}-GV-{}-{}-IT-{}'.format(
        # BID_ALPHA, STD_ALPHA, ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS,
        # MAX_ALPHA, ATRAT_LIM, DISTRIBUTION, REATIVIDADE, RERUNS, RUNS
        # )
        print(FILE_NAME)
        columns = ['par_bid_alpha', 'par_std_alpha', 'par_atrat_avg', 'par_std_dev',
                   'par_number_of_agents', 'par_max_alpha', 'par_atrat_lim',
                   'par_distribution',
                   'par_reatividade', 'par_reruns', 'par_runs', 'file_name']
        values = [BID_ALPHA, STD_ALPHA, ATRAT_AVG, STD_DEV, NUMBER_OF_AGENTS,
                  MAX_ALPHA, ATRAT_LIM, DISTRIBUTION, REATIVIDADE, RERUNS, RUNS, FILE_NAME]

        df_bid_details[columns] = values
        df_bid_results[columns] = values
        # df_bid_details.to_csv(
        # 'Results_temp/New_R/Details-{}.csv'.format(
        # FILE_NAME), index=False)
        df_bid_results.to_csv(
            'Results_temp/New_R/Results-{}.csv'.format(
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
