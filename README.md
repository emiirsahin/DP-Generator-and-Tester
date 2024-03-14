# DP-Generator-and-Tester
Custom Differentially Private Dataset Generator and Differential Privacy Implementation Tester

There are 3 programs to test the DP implementation and a 4th program to analyze the tester, the programs are:
* Tester (tester.py)
* DP (dp.py)
* Data Generator (dataGen.py)
* Analysis (analysis.py)

**DP Program:**
This program is the DP implementation of a given student; in our submission this is an actual DP implementation. Depending on the query, this program returns the sum, count or average of all values in the dataset that fit a certain condition with noise added to ensure DP. There are ways in which this program can be modified to obtain an incorrect DP implementation, the following attributes of the implementation can be modified:
* The distribution from which the noise values are drawn
* The sensitivity values for the different query operations
* The epsilon value
* How the noise is added to the data

The distribution by default is the Laplace distribution. The closest distribution to the Laplace distribution is the Gaussian distribution which is the best possible choice for an incorrect DP implementation, since the noise values drawn from the Gaussian distribution are the closest to the correct noise values while still being an incorrect implementation. If the noise values are chosen from another distribution or if the implementation is incorrect to such a degree that the noise values are not drawn from a distribution at all, the error will be much more apparent.
The sensitivity values can be modified to obtain an incorrect DP implementation. If the sensitivity values are calculated wrong or set statically, the tester program will detect this error since the tester program is randomized, this is also the case for the epsilon value, the DP program by default receives the epsilon value from the tester program but it can be changed manually within the DP program to see the effect of a wrong epsilon value on the tester programs ability to detect it.
The addition of noise is very straightforward, but it is technically another angle in which the DP implementation can be wrong.

**Data Generator Program:**
This program generates a dataset given the number of rows and the column specifications. The columns can be specified as follows:
* Integer with uniform distribution with a minimum and a maximum value
* Integer with normal distribution with a mean and a standard deviation
* Float with uniform distribution with a minimum and a maximum value
* Float with normal distribution with a mean and a standard deviation
* String chosen from a provided list of strings uniformly

Since the objective of this program is simply to generate a dataset to be queried with the DP program, these randomly generated specifications and values work well to test a DP implementation.

**Tester Program:**
This program is where the DP implementation is tested for correctness. The testing is done using the Kolmogorov-Smirnov test. This test returns the likeliness -The P value- that a given set belongs to a distribution. In our case the set is the set of noise values that the DP implementation adds to its returned query result, and the distribution is the Laplace distribution with the standard deviation being equal to the sensitivity value divided by the epsilon value. The test is done in many iterations, (The iterations variable is called “iteration” in the tester program and “inner_iter” in the analysis program) each iteration adds its noise value to the noises list and the process for each iteration is as follows:
* Generate a random dataset with the number of rows randomly chosen between the minimum and maximum value given by the user.
* Get the subset of the dataset that fits the given condition.
* Randomly choose one of the three operations (Average, sum, count).
* Depending on the operation, set the correct sensitivity value and set the actual result of the operation done on the subset without DP. 
* Query the DP program N times where N is the length of the subset, calculate the noise value and store it in the noise list
* Do the Kolmogorov-Smirnov test to obtain the P value for the given noise list
* Add the P value to its respective operation’s P values list

After these steps are taken for each iteration, the following are done:

* Get the mean P value for each operation
* Print the appropriate result regarding the correctness of the DP implementation depending on the mean P values of the 3 operations

The interpretation of the 3 mean P values for the 3 operations are done in a way that provides the most information regarding the correctness of the DP implementation. If the mean P values for all operations are above “0.4”, the test concludes that the tested DP implementation is indeed a correct DP implementation. If the mean P values for all operations are above “0.2” and if at least one of the mean P values is below “0.4”, the program concludes that there is a minor error in the DP implementation, this minor error could be many things such as; the distribution from which the noise values are drawn could be the normal distribution instead of the Laplace distribution, the standard deviation is off with 50% room (the calculated standard deviation is either 0.5 of the actual standard deviation or 1.5 of the actual standard deviation) this could be caused by the sensitivity values for one or more operations being calculated slightly incorrectly (double or half the expected value) or the epsilon value being slightly off. If the program concludes that the DP implementation is incorrect then there is a baser issue than the ones described above, and the DP implementation is done very incorrectly, the sensitivity value for one or more of the operations could have been completely miscalculated or the distribution from which the noises are drawn could be the uniform distribution. The values used in the interpretation were chosen by observing the mean P values by running the tester program many times; this was done in the analysis program.

**Analysis Program:**
The analysis program essentially tests the correctness of the tester program. It was initially used to observe the optimal P value cutoff points to best interpret the results of the tester program regarding the correctness of the DP implementation. This program allows us to run the tester program “iterations” number of times (“iterations” is the name of the variable in the analysis program that determines how many times the tester program is run) with different attributes. The attributes are as follows:
* “inner_iter”: The number of iterations done within the tester program
* “epsilon”: The epsilon value can be specified in the analysis program but defaults to “1.0” in the tester program if not specified
* “low_num_entries”: The minimum number of rows in the generated dataset
* “high_num_entries”: The maximum number of rows in the generated dataset
  
The tester program is run “iterations” number of times and the mean P values returned by the tester program are added to the list of mean P values for the respective operations.
This program allows us the monitor the mean P values returned by the tester program with the correct and many different incorrect DP implementations to determine the optimal cutoff points for interpretation and classification of the DP program by observing the mean P values. 
