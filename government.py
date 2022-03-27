import pandas as pd
import numpy as np


def government(reatividade, chosen_project, func_projects):
    rebid_project = chosen_project.copy()
    if ((reatividade > 0) & (chosen_project.iloc[0]['reruns'] < 1)):
        chosen_project['bid_alpha'] = chosen_project['bid_alpha'] - reatividade
        chosen_project['reruns'] = chosen_project['reruns'] + 1
        bid_alpha = chosen_project.iloc[0]['bid_alpha']

        if bid_alpha >= 1:
            chosen_project['projeto_atratividade_std'] = (
                chosen_project['outorga']
                + chosen_project['investimento']
                + chosen_project['retorno_curto_prazo']
            )
            chosen_project['projeto_atratividade_min'] = (
                chosen_project['projeto_atratividade_std']
            )
            chosen_project['projeto_atratividade_max'] = (
                chosen_project['projeto_atratividade_std']
            )
            chosen_project['projeto_outorga'] = (
                chosen_project['outorga']
                * bid_alpha
            )
        else:
            chosen_project['projeto_atratividade_std'] = (
                chosen_project['outorga']
                + chosen_project['investimento']
                + chosen_project['retorno_curto_prazo']
            )
            chosen_project['projeto_atratividade_min'] = (
                (chosen_project['outorga'] * bid_alpha)
                + chosen_project['investimento']
                + chosen_project['retorno_curto_prazo']
            )
            chosen_project['projeto_atratividade_max'] = (
                (chosen_project['outorga'] * (1 + (1 - bid_alpha)))
                + chosen_project['investimento']
                + chosen_project['retorno_curto_prazo']
            )
            chosen_project['projeto_outorga'] = (
                chosen_project['outorga']
                * bid_alpha
            )
        func_projects = pd.concat([func_projects, chosen_project])
        chosen_project = rebid_project.copy()

        return func_projects, chosen_project
    else:
        pass
