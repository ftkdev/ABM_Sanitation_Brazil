import pandas as pd
import numpy as np


def create_agents(loc, scale, size, max_alpha, atrat_range):
    agents_name = list(range(size))
    atratividade = np.random.normal(loc=loc, scale=scale, size=size)
    atratividade_min = [
        a-np.random.uniform(0, atrat_range) for a in atratividade]
    atratividade_max = [
        a+np.random.uniform(0, atrat_range) for a in atratividade]
    max_alpha = np.random.uniform(1, max_alpha, size=size)

    agents_list = {
        'agente': agents_name,
        'agente_atratividade_min': atratividade_min,
        'agente_atratividade_max': atratividade_max,
        'agente_alpha_max': max_alpha,
    }
    df_agents_listao = pd.DataFrame(agents_list)
    return df_agents_listao


# teste = create_agents(2.5, 0.25, 40, 1.4, 0.1)
# print(teste)
