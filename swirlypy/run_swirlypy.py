#!/usr/bin/env python3
from swirlypy.swirlytool import *
import argparse
import os
from courses import import_course_path
import swirlypy.colors as colors
from swirlypy.colors import color, colorize
from swirlypy.main_menu import menu
import importlib

def swirl():
    print("\n")
    colors.print_option("| Welcome to swirlpy! What can I call you? \n")

    user_name = input("Please enter your name: ")
    print("\n")
    print("| Thanks", user_name + "!", "Lets cover some basic commands in swirlpy\n")

    print("| Whenever you see '...', that means you should press Enter when you are ready. \n")

    print("... <- your cue to press Enter to continue \n")

    input("")

    while True:
        print("\n Welcome to the main menu of Swirlypy! You have the following options: \n")
        colors.print_option("| -- Typing learn() allows you to start a course. \n")
        colors.print_option("| -- Typing bye() causes Swirlypy to exit. \n")
        colors.print_option("| -- Typing menu() displays the main menu again. \n")

        user_input = input("Enter your choice:  ")
        if user_input == "bye()":
            print("\n")
            colors.print_exit("Leaving Swilypy now..Bye! \n")
            exit()
        elif user_input == "learn()":
            menu()
        elif user_input == "menu()":
            continue
          

