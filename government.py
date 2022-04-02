import pandas as pd
import numpy as np


def government(reatividade, chosen_project, func_projects):
    rebid_project = chosen_project.copy()
    if ((reatividade > 0) & (chosen_project.iloc[0]['reruns'] < 1)):
        chosen_project['bid_alpha'] = chosen_project['bid_alpha'] - reatividade
        chosen_project['reruns'] = chosen_project['reruns'] + 1
        # print(chosen_project)

        func_projects = pd.concat([func_projects, chosen_project])
        chosen_project = rebid_project.copy()

        return func_projects, chosen_project
    else:
        pass
