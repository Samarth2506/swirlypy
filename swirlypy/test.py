from swirlytool import *
import argparse

print("Welcome to swirlpy! What can I call you? \n")

user_name = input("Please enter your name: ")

print("Thanks", user_name + "!", "Lets cover some basic commands in swirlpy\n")

print("Whenever you see '...', that means you should press Enter when you are ready. \n")

print("... <- your cue to press Enter to continue \n")

input("")

main(parse(["run", "courses/intro"]))