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
    print("| Welcome to swirlpy! What can I call you? \n", "yellow")

    user_name = input("Please enter your name: ")
    print("\n")
    print("| Thanks", user_name + "!", "Lets cover some basic commands in swirlpy\n")

    print("| Whenever you see '...', that means you should press Enter when you are ready. \n")

    print("... <- your cue to press Enter to continue \n")

    input("")

    while True:
        print("Welcome to the main menu of Swirlypy! You can choose to exit the application by typing bye() or continue learning by typing continue()")
        user_input = input("What do you want to do? ")
        if user_input == "bye()":
            print("Leaving Swilypy now..")
            exit()
        elif user_input == "continue()":
            menu()
          

