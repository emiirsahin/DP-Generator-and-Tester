import random
import numpy as np
from dataGen import generate_custom_dataframe
from dp import differentially_private_query
from scipy.stats import kstest

def complete_test(iteration = 100, epsilon = 1, low_num_entries = 50, high_num_entries = 200, column = "INTU", condition = "FLOATN > 0"):
    
    # Column specs of the dataset
    column_specs = {
        "INTU": {"type": "int", "min": 1, "max": 10, "distribution": 'uniform'},
        "INTN": {"type": "int", "mean": 5, "stdev": 0.4, "distribution": 'normal'},
        "FLOATU": {"type": "float", "min": 0.5, "max": 2.5, "distribution": 'uniform'},
        "FLOATN": {"type": "float", "mean": 5, "stdev": 0.4, "distribution": 'normal'},
        "STR": {"type": "category", "values": ["Sunny", "Rainy", "Cloudy"]}
    }

    # Operations to be randomly selected
    operations = ["average", "sum", "count"]

    p_vals_a = []   # p values for average operation
    p_vals_s = []   # p values for sum operation
    p_vals_c = []   # p values for count operation

    j = 0

    while j < iteration:
        num_entries = np.random.randint(low_num_entries, high_num_entries)  # Randomly select the number of rows, this is to thwart DP implementation values having been implemented statically
        df = generate_custom_dataframe(num_entries, column_specs)   # Generate a random dataset with the number of rows and the specifications
        data = df.query(condition)  # Filter the data given a condition, by default it is "FLOATN > 0" which for the specifications described above essentially returns all rows in the dataset as all FLOATN values are greater than 0
        filteredData = data[column] # Get the filtered data on its own with only the requested column
        operation = random.choice(operations)   # Randomly select an operation for this iteration of the test
        actualVal = 0   # The actual value of the operation
        sensitivity = 0 # The actual sensitivity value of the operation
        if(operation == "average"):
            actualVal = filteredData.mean()
            sensitivity = max(filteredData)/filteredData.count() 
        elif(operation == "sum"):
            actualVal = filteredData.sum()
            sensitivity = max(filteredData)
        elif(operation == "count"):
            actualVal = filteredData.count()
            sensitivity = 1
        
        length = filteredData.shape[0]  # Length of the filtered data
        noiseDist = []  # List to hold the noise values 
        i = 0

        while i < length:
            res = differentially_private_query(df, column, condition, operation, epsilon)   # Get the returned value from the DP implementation for every row
            noiseDist.append(res - actualVal)   # Get the returned noise of the DP implementation
            i+=1

        loc = 0  # Mean value for the laplace distribution
        scale = sensitivity/epsilon  # Standard deviation value for the laplace distribution

        # Perform the Kolmogorov-Smirnov test
        ks_statistic, p_value = kstest(noiseDist, 'laplace', args=(loc, scale))
        if(operation == "average"):
            p_vals_a.append(p_value)
        elif(operation == "sum"):
            p_vals_s.append(p_value)
        elif(operation == "count"):
            p_vals_c.append(p_value)
        j+=1


    p_value_a_mean = sum(p_vals_a)/len(p_vals_a)    # Get the average of the p values for a given operation
    p_value_s_mean = sum(p_vals_s)/len(p_vals_s)    # Get the average of the p values for a given operation
    p_value_c_mean = sum(p_vals_c)/len(p_vals_c)    # Get the average of the p values for a given operation
    
    # The reason for the values I chose below are explained in the report, I chose them according to the analysis of the tester in the analysis program
    if(p_value_a_mean > 0.4 and p_value_s_mean > 0.4 and p_value_c_mean > 0.4):
        print("The implementation is correct")
    elif((p_value_a_mean > 0.2 and p_value_s_mean > 0.2 and p_value_c_mean > 0.2) and (p_value_a_mean < 0.4 or p_value_s_mean < 0.4 or p_value_c_mean < 0.4)):
        print("Most likely an incorrect implementation. The noise might be chosen from an incorrect distribution")
    else:
        print("The implementation is incorrect")
        
    return p_value_a_mean, p_value_s_mean, p_value_c_mean