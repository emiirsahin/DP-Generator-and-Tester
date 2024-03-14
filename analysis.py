from tester import complete_test 

p_a_means = []  # fit values of the DP implementation of average operation
p_s_means = []  # fit values of the DP implementation of sum operation
p_c_means = []  # fit values of the DP implementation of count operation

j = 0
iterations = 1  # Iterations for the analysis of the tester

inner_iter = 100 # Iterations in the tester. The test is done with a random dataset and a random operation this many times 
epsilon = 0.5   # Epsilon value
low_num_entries = 50    # Lowest value for the number of rows in the dataset
high_num_entries = 200  # Highest value for the number of rows in the dataset

while j < iterations:
    results = complete_test(inner_iter, epsilon, low_num_entries, high_num_entries)
    p_a_means.append(results[0])    # fit values of the DP implementation of average operation appended to the analysis list
    p_s_means.append(results[1])    # fit values of the DP implementation of sum operation appended to the analysis list
    p_c_means.append(results[2])    # fit values of the DP implementation of count operation appended to the analysis list
    j+=1

#The maximum and minimum average fit values for the operations are printed along with the values themselves
print(p_a_means)
print("For the average operation, maximum average fit is: ", max(p_a_means), " an the minimum average fit is: ", min(p_a_means))
print(p_s_means)
print("For the sum operation, maximum average fit is: ", max(p_s_means), " an the minimum average fit is: ", min(p_s_means))
print(p_c_means)
print("For the count operation, maximum average fit is: ", max(p_c_means), " an the minimum average fit is: ", min(p_c_means))