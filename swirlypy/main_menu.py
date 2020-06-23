import os
from courses import import_course_path
from swirlypy.swirlytool import *
import argparse
import os
from courses import import_course_path
import swirlypy.colors as colors
from swirlypy.colors import color, colorize
import importlib


def menu():
    print("\n")
    print("Welcome to the course menu! If you like to exit to the main menu at any point, press Ctrl+D or enter '0'. \n")
    print("You have the following courses to choose from: \n")

    path = str(import_course_path.get_path())


    # # print(filter(os.path.isdir, os.listdir(path)))
    courses = next(os.walk( os.path.join(path,'.')))[1]
    courses.remove("__pycache__")

    for index, course in enumerate(courses):
        colors.print_option("%d: %s" % (index + 1, course))

    print("\n")

    try:
        course_select = input("| --  Select a course: ")
        print("\n")
    except EOFError:
        print("Returning to the main menu.. \n")
        return


    try:
        course_select = int(course_select)
    except ValueError or ModuleNotFoundError:
        colors.print_err("No course. Returning to Course menu.. \n")
        menu()
  

    if type(course_select) == int:
        if course_select == 0:
            print("Returning to the main menu.. \n")
            return
        try:
            course_select = courses[course_select - 1]
        except IndexError or ModuleNotFoundError:
            colors.print_err("No course. Returning to Course menu.. \n")
            menu()
    
    moduleNames = 'courses.'+ str(course_select)
    pkg  = '.initialize_lesson'

    m = importlib.import_module(moduleNames+pkg)
    # print(m)

    #print(globals())

    data = m.get_data()
    # print(m.pd.DataFrame())
    # print("| Choose from the following commands: ('run', 'info', 'create', 'test') \n")

    # command = input("| Enter a command for the course: ")

    main(m, data, parse(["run", os.path.join(path,course_select)]))
    
    
