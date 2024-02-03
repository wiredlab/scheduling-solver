# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:43:44 2022

@author: skhorbot
"""

from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus
import pandas as pd
import numpy as np


DEBUG_PRINT = False


def run(xlsx):
    """Input:
        xlsx - can be a path to a spreadsheet or the file contents itself

    Outputs:
        output - formatted string version of original
        result - dict of results
    """

    df = pd.read_excel(
        xlsx,
        header=None, # first row is NOT DataFrame column labels
    )

    ###################################################################
    #
    # Extract configuration information from spreadsheet
    #
    ###################################################################
    # Figuring out the Professors
    #
    # Ignore the first 4 rows containing the headers
    # extract the first column containing the profs names
    # trim empty cells
    tmp = df.iloc[4:, 0]
    profs = list(filter(pd.notna, tmp))
    n_profs = len(profs)

    # Profs TLC Supply
    #
    # Extract the second column with the profs capacities
    # ignore the first 3 rows with the headers
    # trim empty cells
    tmp = df.iloc[3:, 1]
    TLC_capacity = list(filter(pd.notna, tmp))

    # Course names
    #
    # Extract the 1st row with the courses names
    # which begin with the 3rd column
    # trim empty cells
    tmp = df.iloc[0, 2:]
    courses = list(filter(pd.notna, tmp))
    n_courses = len(courses)

    # Course Teaching Load Credits
    #
    # Extract the second row with the TLCs per section
    # ignore the first 2 cols with the headers
    # trim empty cells
    tmp = df.iloc[1, 2:]
    TLC = list(filter(pd.notna, tmp))

    # Section Demand array
    #
    # Extract the third row with the number of needed sections
    # ignore the first 2 cols with the headers
    # trim empty cells
    tmp = df.iloc[2, 2:]
    course_needs = list(filter(pd.notna, tmp))

    # Preference Matrix
    #
    # Begins at the 5th row and 3rd column
    # extends only to the number of professors and courses
    pref_matrix = df.iloc[4:4+n_profs, 2:2+n_courses].values


    ###################################################################
    #
    # Construct the linear programming model
    #
    ###################################################################
    model = LpProblem("Scheduling-Problem", LpMaximize)

    # Create the variables to be solved for
    variable_names = [
        f"{i:02d}{j:02d}" for j in range(n_courses) for i in range(n_profs)
    ]
    variable_names.sort()
    DV_variables = LpVariable.matrix(
        "X", variable_names, cat="Integer", lowBound=0, upBound=2
    )
    allocation = np.array(DV_variables).reshape(n_profs, n_courses)

    if DEBUG_PRINT:
        print("Decision Variable/Allocation Matrix: \n")
        print(allocation)
        print("\n")

    # Create an objective function and add it to the model
    obj_func = lpSum(allocation * pref_matrix)
    model += obj_func

    # Covering needed courses Constraints
    for j in range(n_courses):
        model += lpSum(allocation[i][j] for i in range(n_profs)) == course_needs[j], "Course needs " + str(j)

        if DEBUG_PRINT:
            print(lpSum(allocation[i][j] for i in range(n_profs)) == course_needs[j])

    # Profs availability Constraints
    for i in range(n_profs):
        model += lpSum(allocation[i][j] * TLC[j] for j in range(n_courses)) <= TLC_capacity[i], "TLC capacity " + str(i)

        if DEBUG_PRINT:
            print(lpSum(allocation[i][j] * TLC[j] for j in range(n_courses)) <= TLC_capacity[i])


    ###################################################################
    # The main event,
    # solve the model
    ###################################################################
    model.solve()
    status = LpStatus[model.status]

    if DEBUG_PRINT:
        print("\nStatus:", status, "\n")
        # print("Objective Function:", model.objective.value(), "\n")


    ###################################################################
    #
    # Collect results into a usable form
    #
    ###################################################################
    # Initialize dict to hold results by professor
    result = {}
    for i, prof in enumerate(profs):
        result[prof] = {
            "courses": {},
            "TLC": 0,
            "capacity":
            TLC_capacity[i],
        }

    for v in model.variables():
        n_sections = int(v.value())  # can only be an integer

        # Only care about non-zero assignments
        if n_sections != 0:
            prof_index = int(v.name[2:4])
            course_index = int(v.name[4:6])
            course_name = courses[course_index]
            prof = profs[prof_index]

            result[prof]["courses"][course_name] = n_sections
            result[prof]["TLC"] += n_sections * TLC[course_index]

    if DEBUG_PRINT:
        import pprint
        pprint.pprint(result)

    return status, result


# This runs only if called like "python schedulingLP.py input_name.xlsx"
if __name__ == "__main__":
    import pprint
    import sys

    status, result = run(sys.argv[1])

    pprint.pprint(result)
    print(status)
