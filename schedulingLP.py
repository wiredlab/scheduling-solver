# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:43:44 2022

@author: skhorbot
"""

from io import StringIO

from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus
import pandas as pd
import numpy as np


def run(xlsx_file):
    df = pd.read_excel(xlsx_file)

    #Figuring out the Professors
    My_slice=df.iloc[:,0].values.tolist()  #Extract the first column with the profs names
    profs_slice = My_slice[4:]     # eliminating the first 4 rows with the headers
    profs = [x for x in profs_slice if str(x) != 'nan']     #Eliminate the empty rows
    n_profs = len(profs)        # Finding the number of Profs

    #Figuring out the Courses
    My_slice=df.iloc[0,:].values.tolist()  #Extract the first row with the courses names
    courses_slice = My_slice[2:]     # eliminating the first 2 cols with the headers
    courses = [x for x in courses_slice if str(x) != 'nan']     #Eliminate the empty cols
    n_courses = len(courses)        # Finding the number of courses

    # Preference Matrix
    # creating the vector that will indicate the rows of interest
    row_index = []
    for i in range(n_profs):
        row_index.append(4+i)

    # creating the vector that will indicate the columns of interest
    col_index = []
    for i in range(n_courses):
        col_index.append(2+i)

    nslice = df.iloc[row_index,col_index]
    Pref_matrix = nslice.values.tolist()

    # section Demand array
    My_slice=df.iloc[2,:].values.tolist()  #Extract the third row with the number of needed sections
    needs_slice = My_slice[2:]     # eliminating the first 2 cols with the headers
    course_needs = [x for x in needs_slice if str(x) != 'nan']     #Eliminate the empty cols

    # Course TLCs
    My_slice=df.iloc[1,:].values.tolist()  #Extract the second row with the number of needed sections
    needs_slice = My_slice[2:]     # eliminating the first 2 cols with the headers
    TLC = [x for x in needs_slice if str(x) != 'nan']     #Eliminate the empty cols

    # Profs TLC Supply
    My_slice=df.iloc[:,1].values.tolist()  #Extract the second column with the profs capacities
    profs_capacity = My_slice[4:]     # eliminating the first 4 rows with the headers
    TLC_capacity = [x for x in profs_capacity if str(x) != 'nan']     #Eliminate the empty rows

    model = LpProblem("Scheduling-Problem", LpMaximize)

    # Create the variables to be solved for
    variable_names = [str(i)+str(j) for j in range(10,10+n_courses) for i in range(n_profs)]
    variable_names.sort()
    DV_variables = LpVariable.matrix("X", variable_names, cat = "Integer", lowBound= 0, upBound = 2 )
    allocation = np.array(DV_variables).reshape(n_profs,n_courses)
    print("Decision Variable/Allocation Matrix: \n")
    print(allocation)
    print("\n")

    # Create an objective function and add it to the model
    obj_func = lpSum(allocation*Pref_matrix)
    model +=  obj_func
    #print(model)

    # Covering needed courses Constraints
    for j in range(n_courses):
        print(lpSum(allocation[i][j] for i in range(n_profs)) == course_needs[j])
        model += lpSum(allocation[i][j] for i in range(n_profs)) == course_needs[j] , "Course needs " + str(j)

    # Profs availability Constraints
    for i in range(n_profs):
        print(lpSum(allocation[i][j-10]*TLC[j-10] for j in range(10,10+n_courses)) <= TLC_capacity[i])
        model += lpSum(allocation[i][j-10]*TLC[j-10] for j in range(10,10+n_courses)) <= TLC_capacity[i] , "TLC capacity " + str(i)

    model.solve()

    status =  LpStatus[model.status]

    print("\nStatus:", status,"\n")

    print("Objective Function:", model.objective.value(),"\n")

    final_list = [] #This is a list of the courses assigned to each Prof
    TLC_count = [0]*n_profs  #This list tracks number of TLCs assigned to each prof

    # This will make final_list a list of n_profs x lists
    for i in range(n_profs):
        final_list.append([])

    for v in model.variables():
        if (v.value() != 0):
            prof_index = int(v.name[2])
            course_index = int(v.name[3:])-10
            course_name = courses[course_index]
            my_string = str(v.value()) + " x " + str(course_name)
            final_list[prof_index].append(my_string)
            TLC_count[prof_index] += v.value()*TLC[course_index]

    f = StringIO()
    for i in range(n_profs):
        print(profs[i]+":\t"+str(final_list[i])+"\t"+"TLCs = "+str(TLC_count[i])+"/"+str(TLC_capacity[i])+"\n", file = f)

    return f.getvalue()

if __name__ == "__main__":
    s = run("Sp24b.xlsx")
    print(s)

