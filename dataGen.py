import pandas as pd
import numpy as np
import random

# Given the number of rows and the column specifications this program generates the dataframe
def generate_custom_dataframe(num_entries, column_specs):
    data = {}
    for column_name, specs in column_specs.items():
        if specs['type'] == 'int':
            if specs['distribution'] == 'uniform':
                data[column_name] = np.random.randint(specs['min'], specs['max']+1, num_entries)
            elif specs['distribution'] == 'normal':
                data[column_name] = np.rint(np.random.normal(specs['mean'], specs['stdev'], num_entries)).astype(int)
        elif specs['type'] == 'float':
            if specs['distribution'] == 'uniform':
                data[column_name] = np.random.uniform(specs['min'], specs['max'], num_entries)
            elif specs['distribution'] == 'normal':
                data[column_name] = np.random.normal(specs['mean'], specs['stdev'], num_entries)
        elif specs['type'] == 'category':
            data[column_name] = [random.choice(specs['values']) for _ in range(num_entries)]
    
    return pd.DataFrame(data)


