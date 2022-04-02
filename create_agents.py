import pandas as pd
import numpy as np


def create_agents(loc, scale, size, max_alpha):
    agents_name = list(range(size))
    tamanho = np.random.normal(loc=loc, scale=scale, size=size)
    investimento = np.random.normal(loc=loc, scale=scale, size=size)
    max_alpha = np.random.uniform(1, max_alpha, size=size)

    agents_list = {
        'agente': agents_name,
        'ag_tamanho': tamanho,
        'ag_investimento': investimento,
        'ag_max_alpha': max_alpha,
    }
    df_agents_listao = pd.DataFrame(agents_list)
    return df_agents_listao


# teste = create_agents(0.5, 0.25, 40, 1.41)
# print(teste)
