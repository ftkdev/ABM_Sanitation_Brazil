import pandas as pd
# import random as rd
import numpy as np
from government import government


def projects_index(bid_alpha, std_alpha, func_projects):
    func_projects['bid_alpha'] = (
        np.random.normal(bid_alpha, std_alpha,
                         size=len(func_projects))
    )
    func_projects['reruns'] = 0
    func_projects['outorga'] = (func_projects['pop_alvo_ratio']
            * func_projects['bid_alpha']
            )
    # print(func_projects)
    return func_projects

def project_select(func_projects):
    # Randomly select and withdrawls one project from the projects list
    chosen_project = func_projects.sample()
    # chosen_project = func_projects.iloc[0]
    # print(chosen_project)
    func_projects.drop(index=chosen_project.index, axis=0, inplace=True)
    # print(func_projects)
    return chosen_project, func_projects


def agents_select(chosen_project, func_agents, atrat_lim):
    # Remove agents that do not satisfy the conditions
    # print(chosen_project)
    func_agents['ag_atratividade'] = (
            abs(func_agents['ag_tamanho'] - chosen_project.iloc[0]['pj_tamanho']) +
            abs(func_agents['ag_investimento'] - chosen_project.iloc[0]['pj_investimento'])
            )
    # print(func_agents)
    pj_atrat_lim = atrat_lim / chosen_project.iloc[0]['bid_alpha']
    # print(pj_atrat_lim)
    filter1 = (
        (func_agents['ag_atratividade'] > pj_atrat_lim
        ))
    # print(func_agents.loc[filter1, :])
    func_agents_select = func_agents.drop(func_agents[filter1].index)
    func_agents_select['factor'] = func_agents_select['ag_max_alpha']

    if chosen_project.iloc[0]['bid_alpha'] < 1:
        filter2 = (
            (func_agents['ag_atratividade'] < atrat_lim
            ))
        # print(func_agents_select.loc[filter2, 'factor'])
        func_agents_select.loc[filter2, 'factor'] = (
            func_agents_select['ag_max_alpha']
            + (1 - (chosen_project.iloc[0]['bid_alpha'])
               ))

    return func_agents_select

def run_bids(func_projects, func_agents_select, bid_number, chosen_project, func_agents, run, reatividade):
    # Qualified agents place their bids
    func_agents_select['agente_alpha_ofertado'] = (
        np.random.uniform(1,
                          func_agents_select['factor'])
    )
    func_agents_select['bid'] = (
        chosen_project.iloc[0]['outorga'] *
        (func_agents_select['agente_alpha_ofertado'])
    )
    if func_agents_select.empty is True:
        if (reatividade > 0) & (chosen_project.iloc[0]['reruns'] < 1):
            # Government allows discount
            gov_rebid = government(
                reatividade, chosen_project, func_projects)
            func_projects = gov_rebid[0]
            chosen_project = gov_rebid[1]

            df_bid_winner = pd.DataFrame()
            dic_nobid = {'agente': ['rebid', ], 'ag_tamanho': [0, ],
                    'ag_investimento': [0, ], 'ag_max_alpha': [0, ], 'ag_atratividade': [0. ],
                         'factor': [0, ], 'agente_alpha_ofertado': [0, ], 'bid': [0, ]}
            func_agents_select = pd.DataFrame(data=dic_nobid)

        else:
            dic_nobid = {'agente': ['nobid', ], 'ag_tamanho': [0, ],
                    'ag_investimento': [0, ], 'ag_max_alpha': [0, ], 'ag_atratividade': [0. ],
                         'factor': [0, ], 'agente_alpha_ofertado': [0, ], 'bid': [0, ]}
            func_agents_select = pd.DataFrame(data=dic_nobid)

    func_agents_select['bid_number'] = bid_number
    func_agents_select['estado'] = chosen_project.iloc[0]['estado']
    func_agents_select['pop_alvo'] = chosen_project.iloc[0]['pop_alvo']
    func_agents_select['pop_alvo_ratio'] = chosen_project.iloc[0]['pop_alvo_ratio']
    func_agents_select['pj_tamanho'] = chosen_project.iloc[0]['pj_tamanho']
    func_agents_select['pj_investimento'] = chosen_project.iloc[0]['pj_investimento']
    func_agents_select['bid_alpha'] = chosen_project.iloc[0]['bid_alpha']
    func_agents_select['outorga'] = chosen_project.iloc[0]['outorga']
    func_agents_select['bid_number'] = bid_number
    func_agents_select['run'] = run
    func_agents_select['reruns'] = chosen_project.iloc[0]['reruns']

    # print(func_agents_select)

    filter_winner = (
        func_agents_select['bid'] == func_agents_select['bid'].max()
    )
    df_bid_winner = (func_agents_select.loc[filter_winner, :])

    # Remove winner agent from the main agents list
    if (df_bid_winner.iloc[0]['agente'] != 'nobid') & (df_bid_winner.iloc[0]['agente'] != 'rebid'):
        # print(df_bid_winner.index)
        func_agents.drop(index=df_bid_winner.index, axis=0, inplace=True)
    return func_agents_select, df_bid_winner, func_agents, func_projects



# def projects_index2(bid_alpha, std_alpha, func_projects):
    # func_projects['bid_alpha'] = (
        # np.random.normal(bid_alpha, std_alpha,
                         # size=len(func_projects))
    # )
    # func_projects['reruns'] = 0
    # # print(func_projects)
    # if bid_alpha >= 1:
        # func_projects['projeto_atratividade_std'] = (
            # func_projects['outorga']
            # + func_projects['investimento']
            # + func_projects['retorno_curto_prazo']
        # )
        # func_projects['projeto_atratividade_min'] = (
            # func_projects['projeto_atratividade_std']
        # )
        # func_projects['projeto_atratividade_max'] = (
            # func_projects['projeto_atratividade_std']
        # )
        # func_projects['projeto_outorga'] = (
            # func_projects['outorga']
            # * bid_alpha
        # )
    # else:
        # func_projects['projeto_atratividade_std'] = (
            # func_projects['outorga']
            # + func_projects['investimento']
            # + func_projects['retorno_curto_prazo']
        # )
        # func_projects['projeto_atratividade_min'] = (
            # (func_projects['outorga'] * bid_alpha)
            # + func_projects['investimento']
            # + func_projects['retorno_curto_prazo']
        # )
        # func_projects['projeto_atratividade_max'] = (
            # (func_projects['outorga'] * (1 + (1 - bid_alpha)))
            # + func_projects['investimento']
            # + func_projects['retorno_curto_prazo']
        # )
        # func_projects['projeto_outorga'] = (
            # func_projects['outorga']
            # * bid_alpha
        # )
    # return func_projects

# def agents_select2(chosen_project, func_agents):
    # # Remove agents that do not satisfy the conditions
    # filter1 = (
        # (chosen_project.iloc[0]['projeto_atratividade_min'] >
         # func_agents['agente_atratividade_max'])
        # | (chosen_project.iloc[0]['projeto_atratividade_max'] <
           # func_agents['agente_atratividade_min'])
        # | (chosen_project.iloc[0]['bid_alpha'] > func_agents['agente_alpha_max'])
    # )
    # func_agents_select = func_agents.drop(func_agents[filter1].index)
    # func_agents_select['factor'] = func_agents_select['agente_alpha_max']

    # if chosen_project.iloc[0]['bid_alpha'] < 1:
        # filter2 = (
            # (chosen_project.iloc[0]['projeto_atratividade_std'] <=
             # func_agents_select['agente_atratividade_max'])
            # & (chosen_project.iloc[0]['projeto_atratividade_std'] >=
               # func_agents_select['agente_atratividade_min'])
        # )
        # func_agents_select.loc[filter2, 'factor'] = (
            # func_agents_select['agente_alpha_max']
            # + (1 - (chosen_project.iloc[0]['bid_alpha'])
               # ))
    # # print(func_agents_select)

    # return func_agents_select


# def run_bids2(func_projects, func_agents_select, bid_number, chosen_project, func_agents, run, reatividade):
    # # Qualified agents place their bids
    # func_agents_select['agente_alpha_ofertado'] = (
        # np.random.uniform(1,
                          # func_agents_select['factor'])
    # )
    # func_agents_select['bid'] = (
        # chosen_project.iloc[0]['projeto_outorga'] *
        # (func_agents_select['agente_alpha_ofertado'])
    # )
    # if func_agents_select.empty is True:
        # if (reatividade > 0) & (chosen_project.iloc[0]['reruns'] < 1):
            # # Government allows discount
            # gov_rebid = government(
                # reatividade, chosen_project, func_projects)
            # func_projects = gov_rebid[0]
            # chosen_project = gov_rebid[1]

            # df_bid_winner = pd.DataFrame()
            # dic_nobid = {'agente': ['rebid', ], 'agente_atratividade_min': [0, ],
                         # 'agente_atratividade_max': [0, ], 'agente_alpha_max': [0, ],
                         # 'factor': [0, ], 'agente_alpha_ofertado': [0, ], 'bid': [0, ]}
            # func_agents_select = pd.DataFrame(data=dic_nobid)

        # else:
            # dic_nobid = {'agente': ['nobid', ], 'agente_atratividade_min': [0, ],
                         # 'agente_atratividade_max': [0, ], 'agente_alpha_max': [0, ],
                         # 'factor': [0, ], 'agente_alpha_ofertado': [0, ], 'bid': [0, ]}
            # func_agents_select = pd.DataFrame(data=dic_nobid)

    # func_agents_select['bid_number'] = bid_number
    # func_agents_select['estado'] = chosen_project.iloc[0]['estado']
    # func_agents_select['pop_alvo'] = chosen_project.iloc[0]['pop_alvo']
    # func_agents_select['outorga'] = chosen_project.iloc[0]['outorga']
    # func_agents_select['projeto_outorga'] = chosen_project.iloc[0]['projeto_outorga']
    # func_agents_select['investimento'] = chosen_project.iloc[0]['investimento']
    # func_agents_select['retorno_curto_prazo'] = chosen_project.iloc[0]['retorno_curto_prazo']
    # func_agents_select['bid_alpha'] = chosen_project.iloc[0]['bid_alpha']
    # func_agents_select['projeto_atratividade_std'] = chosen_project.iloc[0]['projeto_atratividade_std']
    # func_agents_select['projeto_atratividade_min'] = chosen_project.iloc[0]['projeto_atratividade_min']
    # func_agents_select['projeto_atratividade_max'] = chosen_project.iloc[0]['projeto_atratividade_max']
    # func_agents_select['bid_number'] = bid_number
    # func_agents_select['run'] = run
    # func_agents_select['reruns'] = chosen_project.iloc[0]['reruns']

    # filter_winner = (
        # func_agents_select['bid'] == func_agents_select['bid'].max()
    # )
    # df_bid_winner = (func_agents_select.loc[filter_winner, :])

    # # Remove winner agent from the main agents list
    # if (df_bid_winner.iloc[0]['agente'] != 'nobid') & (df_bid_winner.iloc[0]['agente'] != 'rebid'):
        # # print(df_bid_winner.index)
        # func_agents.drop(index=df_bid_winner.index, axis=0, inplace=True)
    # return func_agents_select, df_bid_winner, func_agents, func_projects
