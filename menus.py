import os
import sys
from users import *

main_menu_display = True

def main_menu_start():

  menu_error = False
  menu_not_num = False

  global main_menu_display
  while main_menu_display == True:

    os.system('cls' if os.name == 'nt' else 'clear')

    print("WELCOME TO BIRDYBOARD!")
    print("~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("1. New User Account")
    print("2. Select User")
    print("3. View Public Chirps")
    print("4. Exit")

    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number of your chosen selection!")

    choice = input("> ")

    try:
      if int(choice) == 1:
        # run function that gets user input for user/civilian name
        new_user_menu()
      elif int(choice) == 2:
        # run function that gets user input for existing username
        select_user_menu()
      elif int(choice) == 3:
        # run function to read all public chirps from chirps.txt
        view_public_menu()
      elif int(choice) == 4:
        # closes the program
        exit_app()
      else:
        # user has picked unavailable option, toggle global variable
        menu_error = True
    except ValueError:
      # user has picked NaN, toggle global variable
        menu_not_num = True

def new_user_menu():

  global main_menu_display
  main_menu_display = False

  getting_input = True
  name_length_error = False
  screenname_length_error = False
  name = None
  screenname = None

  while getting_input == True:

    os.system('cls' if os.name == 'nt' else 'clear')

    print("CREATE A NEW USER")
    print("~~~~~~~~~~~~~~~~~")

    if name_length_error == True:
      print("Name length cannot be 0 characters. Please provide valid input.")
    else:
      print("")

    print("Enter full name:")

    if name == None:
      name = input("> ")
    else:
      print("> {}".format(name))

    # Forces loop until user puts something in the name field
    if len(name) == 0:
      name = None
      name_length_error = True
      continue
    else:
      name_length_error = False

    print("\n")

    if screenname_length_error == True:
      print("Screenname length cannot be 0 characters. Please provide valid input.")
    else:
      print("")

    # Forces loop until user puts something in the name field
    # need to write logic to keep user from entering existing username
    print("Enter screenname:")
    screenname = input("> ")

    if len(screenname) == 0:
      screenname = None
      screenname_length_error = True
    else:
      screenname_length_error = False
      getting_input = False

  # runs the function for instantiating a new class of user
  user = User(name, screenname)
  print(user.name)
  input("")
    # Routes user to the next main screen

def select_user_menu():

  global main_menu_display
  main_menu_display = False

  os.system('cls' if os.name == 'nt' else 'clear')

  print("SELECT USER")
  print("~~~~~~~~~~~")
  print("")
  # runs loop to read and print all usernames
  counter = 1
  print("{}. RETURN TO PREVIOUS MENU".format(counter))
  username = int(input("> "))
  # if user username is == counter, should run the function for the start menu again
  if username == counter:
    main_menu_display = True
    main_menu_start()

def view_public_menu():

  global main_menu_display
  main_menu_display = False

  os.system('cls' if os.name == 'nt' else 'clear')

  print("PUBLIC CHIRPS")
  print("~~~~~~~~~~~~~")
  print("* Please return to main menu and select a user to reply to chirps *")
  print("")
  # runs loop to read and print first part of first chirp in each chirp convo
  counter = 1
  print("{}. RETURN TO PREVIOUS MENU".format(counter))
  choice = int(input("> "))
  # if user choice is == counter, should run the function for the start menu again
  if choice == counter:
    main_menu_display = True
    main_menu_start()

def exit_app():
  os.system('cls' if os.name == 'nt' else 'clear')
  print("Bye!")
  sys.exit()

main_menu_start()
