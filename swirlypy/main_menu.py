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
    print("/n")
    print("Welcome to the course menu! You have the following courses to choose from:")

    path = str(import_course_path.get_path())


    # # print(filter(os.path.isdir, os.listdir(path)))
    courses = next(os.walk( os.path.join(path,'.')))[1]

    for index, course in enumerate(courses):
        colors.print_option("%d: %s" % (index + 1, course))

    print("\n")
    course_select = input("| Select a course: ")


    try:
        course_select = int(course_select)
    except ValueError:
        pass

    if type(course_select) == int:
        try:
            course_select = courses[course_select - 1]
        except IndexError:
            raise NoSuchLessonException("Invalid course index")
    
    moduleNames = 'courses.'+ str(course_select)
    pkg  = '.initialize_lesson'

    m = importlib.import_module(moduleNames+pkg)
    # print(m)

    #print(globals())

    data = m.get_data()
    # print(m.pd.DataFrame())
    print("| Choose from the following commands: ('run', 'info', 'create', 'test') \n")

    command = input("| Enter a command for the course: ")

    main(m, data, parse([command, os.path.join(path,course_select)]))
    
    
