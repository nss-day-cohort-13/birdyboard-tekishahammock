import os
import sys
from users import *

user_list = None

def set_user_list():
  """deserializes users.txt on app start, saves to global variable"""
  global user_list
  user_list = deserialize_users()

def set_chirps():
  """deserializes chirps.txt on app start, saves to global variable"""
  pass

def main_menu_start():
  """Runs the main menu. Routes user to chosen menu option and corresponding functions"""

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  # runs until loop is broken through picking a valid selection
  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("WELCOME TO BIRDYBOARD!")
    print("~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("1. New User Account")
    print("2. Select User")
    print("3. View Public Chirps")
    print("4. Exit")

    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number of your chosen selection!")

    choice = input("> ")

    # attempts to route the user to the functions corresponding to their selection
    # toggles global error variables if it reaches the end of the loop/hits an exception
    try:
      if int(choice) == 1:
        # run function to create a user
        new_user_menu()
        break
      elif int(choice) == 2:
        # run function to select an existing user
        select_user_menu()
        break
      elif int(choice) == 3:
        # run function to READ ONLY all public chirps from chirps.txt
        view_public_menu()
        break
      elif int(choice) == 4:
        # closes the program
        exit_app()
      else:
        # user has picked unavailable option, toggles global variable
        menu_error = True
    except ValueError:
      # user has picked NaN, toggles global variable
        menu_not_num = True

def new_user_menu():
  """Runs the new user menu.

  Actions:
  - collects the information to be passed to the User class
  - runs the serialize_users function
  - passes new uuid to logged_in menu function
  """

  # breaks the while loop once set to "False"
  getting_input = True
  # menu error variables to toggle visible error states from within while loop
  name_length_error = False
  screenname_length_error = False
  screenname_match_error = False
  # name and screenname variables hold user input until both are filled out with valid input
  name = None
  screenname = None

  while getting_input == True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("CREATE A NEW USER")
    print("~~~~~~~~~~~~~~~~~")

    # runs if user has hit enter without providing input
    if name_length_error == True:
      print("Name length cannot be 0 characters. Please provide valid input.")
    else:
      print("")

    print("Enter full name:")

    # checks to see if acceptable name input has been collected already(in the event of a screenname error)
    if name == None:
      name = input("> ")
    else:
      print("> {}".format(name))

    # toggles error variable for name_length if user has neglected to put in any input
    # restarts the loop without prompting for screenname until valid input has been provided
    if len(name) == 0:
      name = None
      name_length_error = True
      continue
    else:
      name_length_error = False

    print("")

    # runs if user has hit enter without providing input
    if screenname_length_error == True:
      print("Screenname length cannot be 0 characters. Please provide valid input.")
    # runs if user has picked a screenname that belongs to another user
    elif screenname_match_error == True:
      print("Screenname already belongs to another user, please pick another name")
    else:
      print("")

    print("Enter screenname:")
    screenname = input("> ")

    # checks to see if user has picked a unique screenname
    for key, value in user_list.items():
      if screenname == value.screenname:
        screenname = None
        screenname_match_error = True

    # forces loop until user puts something in the name field
    try:
      if len(screenname) == 0:
        screenname = None
        screenname_length_error = True
      else:
        screenname_length_error = False
        getting_input = False
    except TypeError:
      pass


  # runs the function for instantiating a new class of user
  user = User(name, screenname)
  # adds the new user to the global user_list and serializes the new list
  global user_list
  user_list[user.uuid] = user
  serialize_users(user_list)

  # routes user to the logged_in menu screen, passes along current user uuid
  logged_in_user_menu(user.uuid)

def select_user_menu():
  """Runs the select user menu.

  Actions:
  - collects the chosen user information
  - passes chosen uuid to logged_in menu function
  """

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("SELECT USER")
    print("~~~~~~~~~~~")
    print("")
    # runs loop to read and print all usernames
    # assigns a number to each screenname based on counter
    # adds each number/uuid as key/value pair to temp dict, matches number and screenname printed in command line/shell
    # could also have used enumerate
    counter = 1
    temp_user_list = dict()
    for key, value in user_list.items():
      temp_user_list[counter] = value.uuid
      print("{}. {}".format(counter, value.screenname))
      counter += 1

    print("{}. RETURN TO PREVIOUS MENU".format(counter))

    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number next to your screenname!")

    choice = input("> ")
    # if user choice is == counter, should run the function for the start menu again
    # else if choice is a key in the temp_user_list dict, will run logged_in menu and pass in matching uuid
    # toggles the error variables if the user has picked something outside of the temp dict range
    try:
      if int(choice) == counter:
        main_menu_start()
        break
      elif int(choice) in temp_user_list:
        logged_in_user_menu(temp_user_list[int(choice)])
        break
      else:
        menu_error = True
    except ValueError:
      menu_not_num = True

def view_public_menu():
  """Runs public chirps menu.

  Actions:
  - displays all chirps marked "public"
  - routes user to expanded chirp thread
  """

  # clears the command line/shell of other text outside of what prints in the while loop
  os.system('cls' if os.name == 'nt' else 'clear')

  print("PUBLIC CHIRPS")
  print("~~~~~~~~~~~~~")
  print("* Please return to main menu and select a user to reply to chirps *")
  print("")
  # runs loop to read and print first part of first chirp in each chirp convo
  # could also use enumerate
  counter = 1
  print("{}. RETURN TO PREVIOUS MENU".format(counter))
  choice = int(input("> "))
  # if user choice is == counter, should run the function for the start menu again
  if choice == counter:
    main_menu_display = True
    main_menu_start()

def logged_in_user_menu(uuid):
  """Runs logged in user menu.

  Arguments:
  - uuid - passed in uuid from either new or selected user, allows to grab user information from global variable user_list

  Actions:
  - routes user to selected menu option and corresponding function
  - user can also log out or exit app from here
  """

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  # runs until user picks a valid option that breaks the while loop
  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("WELCOME {}!".format((user_list[uuid].screenname).upper()))
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("1. View All Chirps")
    print("2. New Public Chirp")
    print("3. New Private Chirp")
    print("4. Log Out")
    print("5. Exit")

    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number of your chosen selection!")

    choice = input("> ")

    # attempts to route the user to the functions corresponding to their selection
    # toggles global error variables if it reaches the end of the loop/hits an exception
    try:
      if int(choice) == 1:
        # allows user to READ/REPLY to all public chirps and private chirp threads addressed to them
        break
      elif int(choice) == 2:
        # allows a user to WRITE a new public chirp and start a new chirp thread
        break
      elif int(choice) == 3:
        # allows a user to WRITE a new private chirp addressed to a specific user and start a new chirp thread
        break
      elif int(choice) == 4:
        # returns user to main menu
        main_menu_start()
        break
      elif int(choice) == 5:
        # closes the program
        exit_app()
      else:
        # user has picked unavailable option, toggle global variable
        menu_error = True
    except ValueError:
      # user has picked NaN, toggle global variable
        menu_not_num = True

def exit_app():
  """exits the program"""
  # clears the command line/shell of other text outside of what prints after this point
  os.system('cls' if os.name == 'nt' else 'clear')
  print("Bye!")
  # runs system exit, which is the same as using an exit command in the command line/shell
  sys.exit()

# runs these functions at app start
set_user_list()
set_chirps()
main_menu_start()
