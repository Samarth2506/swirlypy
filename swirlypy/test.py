from swirlytool import *
import argparse
import os

print("Welcome to swirlpy! What can I call you? \n")

user_name = input("Please enter your name: \n")

print("Thanks", user_name + "!", "Lets cover some basic commands in swirlpy\n")

print("Whenever you see '...', that means you should press Enter when you are ready. \n")

print("... <- your cue to press Enter to continue \n")

input("")

print("Below are the available courses you can choose from: \n")

print(os.listdir("../courses"))

course_select = input("Select a course: ")

main(parse(["run", "courses/" + course_select]))