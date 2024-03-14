import pandas as pd
import numpy as np

# THIS FILE CAN BE MODIFIED TO CHANGE THE DP IMPLEMENTATION, BY DEFAULT IT IS A CORRECT DP IMPLEMENTATION
# The following can be changed to modify the DP implementation and are marked in their respective lines:
# The distribution from which the noise values are chosen
# The sensitivity for each of the operations
# The epsilon value
# How the noise is added to the data

def add_laplace_noise(data, epsilon, sensitivity):      
    noise = np.random.normal(0, sensitivity / epsilon) # The distribution from which the noise values are chosen AND the epsilon value
    return data + noise # How the noise is added to the data

def differentially_private_query(df, column, condition, operation, epsilon=1.0):
    filtered_df = df.query(condition)   # Filter the DataFrame
    
    # Perform the operation
    if operation == 'average':
        result = filtered_df[column].mean()
        sensitivity = max(filtered_df[column])/filtered_df[column].count()  # The sensitivity for each of the operations
    elif operation == 'sum':
        result = filtered_df[column].sum()
        sensitivity = max(filtered_df[column])  # The sensitivity for each of the operations
    elif operation == 'count':
        result = filtered_df[column].count()
        sensitivity = 1 # The sensitivity for each of the operations

    # Add Laplace noise
    result = add_laplace_noise(result, epsilon, sensitivity)

    return result