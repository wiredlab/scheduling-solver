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
    """Input: 'xlsx' can be a path or the file contents itself.

    Outputs:
        output - formatted string version of original
        result - dict of results
    """

    df = pd.read_excel(xlsx)

    #
    # Figuring out the Professors
    #
    # Extract the first column with the profs names
    My_slice = df.iloc[:, 0].values.tolist()

    # ignore the first 4 rows containing the headers
    profs_slice = My_slice[4:]

    # Eliminate the empty rows
    profs = [x for x in profs_slice if str(x) != "nan"]
    n_profs = len(profs)

    #
    # Figuring out the Courses
    #
    # Extract the first row with the courses names
    My_slice = df.iloc[0, :].values.tolist()

    # Eliminating the first 2 cols with the headers
    courses_slice = My_slice[2:]

    # Eliminate the empty cols
    courses = [x for x in courses_slice if str(x) != "nan"]
    n_courses = len(courses)

    #
    # Preference Matrix
    #
    # creating the vector that will indicate the rows of interest
    row_index = []
    for i in range(n_profs):
        row_index.append(4 + i)

    # creating the vector that will indicate the columns of interest
    col_index = []
    for i in range(n_courses):
        col_index.append(2 + i)

    nslice = df.iloc[row_index, col_index]
    Pref_matrix = nslice.values.tolist()

    # section Demand array
    # Extract the third row with the number of needed sections
    My_slice = df.iloc[2, :].values.tolist()

    # eliminating the first 2 cols with the headers
    needs_slice = My_slice[2:]

    # Eliminate the empty cols
    course_needs = [x for x in needs_slice if str(x) != "nan"]

    #
    # Course Teaching Load Credits
    #
    # Extract the second row with the number of needed sections
    My_slice = df.iloc[ 1, : ].values.tolist()

    # eliminating the first 2 cols with the headers
    needs_slice = My_slice[2:]

    # Eliminate the empty cols
    TLC = [x for x in needs_slice if str(x) != "nan"]

    # Profs TLC Supply
    # Extract the second column with the profs capacities
    My_slice = df.iloc[ :, 1 ].values.tolist()

    # eliminating the first 4 rows with the headers
    profs_capacity = My_slice[4:]

    # Eliminate the empty rows
    TLC_capacity = [ x for x in profs_capacity if str(x) != "nan" ]

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
    obj_func = lpSum(allocation * Pref_matrix)
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

    #
    # The main event,
    # solve the model
    #
    model.solve()
    status = LpStatus[model.status]

    if DEBUG_PRINT:
        print("\nStatus:", status, "\n")
        # print("Objective Function:", model.objective.value(), "\n")

    print("Objective Function:", model.objective.value(), "\n")

    final_list = []  # This is a list of the courses assigned to each Prof
    TLC_count = [0] * n_profs  # This list tracks number of TLCs assigned to each prof

    # This will make final_list a list of n_profs x lists
    for i in range(n_profs):
        final_list.append([])

    # initialize dict for professors
    result = {}
    for i, prof in enumerate(profs):
        result[prof] = {"courses": [], "TLC": 0, "capacity": TLC_capacity[i]}

    for v in model.variables():
        n_sections = int(v.value())  # can only be an integer

        # Only care about non-zero assignments
        if n_sections != 0:
            prof_index = int(v.name[2:4])
            course_index = int(v.name[4:6])
            course_name = courses[course_index]
            # my_string = str(v.value()) + " x " + str(course_name)
            my_string = f"{v.value():.0f} x {course_name}"
            final_list[prof_index].append(my_string)
            TLC_count[prof_index] += v.value() * TLC[course_index]

            # collect results into dict
            # {'name':{'courses': [ ... ],
            #          'TLC': float,
            #          'capacity': int, }
            # }
            prof = profs[prof_index]
            result[prof]["courses"].append(my_string)
            result[prof]["TLC"] += v.value() * TLC[course_index]

    out = []
    for i in range(n_profs):
        prof = profs[i]
        assignments = final_list[i]
        tlc = TLC_count[i]
        cap = TLC_capacity[i]

        # print(profs[i]+":\t"+str(final_list[i])+"\t"+"TLCs = "+str(TLC_count[i])+"/"+str(TLC_capacity[i])+"\n", file = f)
        out.append(f"{prof}:\t{assignments}\tTLCs = {tlc:.0f}/{cap}")

    # original print() adds '\n' to the string, but print() already adds one
    # hence two here to match the behavior
    output = "\n\n".join(out)

    return output, result


# This runs only if called like "python schedulingLP.py"
if __name__ == "__main__":
    text, data = run("Sp24b.xlsx")
    print(data)
    print(text)
