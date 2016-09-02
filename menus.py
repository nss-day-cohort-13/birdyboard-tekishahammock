import os
import sys
import datetime
from users import *
from chirps import *
from convo import *

user_list = None
chirps = None
conversations = None

def set_user_list():
  """deserializes users.txt on app start, saves to global variable"""
  global user_list
  user_list = deserialize_users()

def set_chirps():
  """deserializes chirps.txt on app start, saves to global variable"""
  global chirps
  chirps = deserialize_chirps()

def set_conversations():
  """deserializes convo.txt on app start, saves to global variable"""
  global conversations
  conversations = deserialize_convo()

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

  # menu error variables to toggle visible error states from within while loop
  name_length_error = False
  screenname_length_error = False
  screenname_match_error = False
  # name and screenname variables hold user input until both are filled out with valid input
  name = None
  screenname = None

  while True:

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
        # runs the function for instantiating a new class of user
        user = User(name, screenname)
        # adds the new user to the global user_list and serializes the new list
        global user_list
        user_list[user.uuid] = user
        serialize_users(user_list)

        # routes user to the logged_in menu screen, passes along current user uuid
        logged_in_user_menu(user.uuid)
        break
    except TypeError:
      pass

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
  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("PUBLIC CHIRPS")
    print("~~~~~~~~~~~~~")
    print("* Please return to main menu and select a user to reply to chirps *")
    print("")
    # runs loop to read and print first part of first chirp in each chirp convo
    # could also use enumerate
    counter = 1

    public_convo_list = list()
    for key, value in conversations.items():
      if value.public_status == True:
        public_convo_list.append([value.timestamp, value.uuid])

    last_public_chirps = list()
    for convo in public_convo_list:
      # for each convo, loop through chirps to find matching chirps
      public_chirp_list = list()
      for key, value in chirps.items():
        if convo[1] == value.convo_id:
          # for matching chirps, append chirp timestamp and ID to temp list
          public_chirp_list.append([value.timestamp, value.uuid])
      # now that convo_list is loaded, sort through chirps from newest to oldest
      sorted_chirp_list = sorted(public_chirp_list, reverse=True)
      # appends the item at index 0 (should be most recent chirp ID and timestamp) to end of last public chirps
      last_public_chirps.append(sorted_chirp_list[0])
    # now we need to sort last_public_chirps and print in order of most recent
    sorted_convo_by_chirp_list = sorted(last_public_chirps, reverse=True)

    for chirp in sorted_convo_by_chirp_list:
      for key, value in chirps.items():
        if value.uuid == chirp[1]:

          # formats time to be more human readable
          # could be a service function
          if value.timestamp.hour > 12:
            hour = value.timestamp.hour - 12
            time = "PM"
          else:
            hour = value.timestamp.hour
            time = "AM"
          if value.timestamp.minute < 10:
            minute = "0{}".format(value.timestamp.minute)
          else:
            minute = value.timestamp.minute

          day = value.timestamp.day
          month = value.timestamp.month
          year = value.timestamp.year

          chirp.append(counter)
          print("{}/{}/{} - {}:{} {}".format(month, day, year, hour, minute, time))
          print("{}. {}".format(counter, value.text))
          counter += 1

    print("")
    print("{}. RETURN TO PREVIOUS MENU".format(counter))
    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number next to your chosen chirp!")
    choice = input("> ")
    # if user choice is == counter, should run the function for logged in menu again
    # else if choice is in temp_chirp_list
    # toggles the error variables if the user has picked something outside of the range
    try:
      if int(choice) == counter:
        main_menu_start()
        break
      elif int(choice) in range(1, counter):
        for chirp in sorted_convo_by_chirp_list:
          if int(choice) == chirp[2]:
            view_chirp_thread(uuid, chirp[1], False)
        break
      else:
        menu_error = True
    except ValueError:
      menu_not_num = True

def logged_in_user_menu(uuid):
  """Runs logged in user menu.

  Arguments:
  - uuid - passed in uuid from either new or selected user, allows to grab user information from global variable user_list

  Actions:
  - routes user to selected menu option and corresponding function
  - user can also log out or exit app from here
  """

  global user_list

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
        view_all_chirps_menu(uuid)
        break
      elif int(choice) == 2:
        # allows a user to WRITE a new public chirp and start a new chirp thread
        new_public_chirp_menu(uuid)
        break
      elif int(choice) == 3:
        # allows a user to WRITE a new private chirp addressed to a specific user and start a new chirp thread
        private_chirp_addressed_user(uuid)
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

def view_all_chirps_menu(uuid):
  """Runs all chirps menu.

  Actions:
  - displays all chirps marked "public"
  - displays all chirps marked "private" and addressed to the user
  - routes user to expanded chirp thread
  """

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False
  global conversations
  global chirps

  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    # runs loop to read and print first part of first chirp in each chirp convo
    # last chirp from the last 10 UPDATED convos
    # could also use enumerate


    counter = 1

    print("CHIRPS: PUBLIC AND PRIVATE")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("*Showing most recent chirp from last ten public and private conversations*")
    print("")
    print("PUBLIC CONVERSATIONS:")
    print("---------------------")
    public_convo_list = list()
    for key, value in conversations.items():
      if value.public_status == True:
        public_convo_list.append([value.timestamp, value.uuid])

    last_public_chirps = list()
    for convo in public_convo_list:
      # for each convo, loop through chirps to find matching chirps
      public_chirp_list = list()
      for key, value in chirps.items():
        if convo[1] == value.convo_id:
          # for matching chirps, append chirp timestamp and ID to temp list
          public_chirp_list.append([value.timestamp, value.uuid])
      # now that convo_list is loaded, sort through chirps from newest to oldest
      sorted_chirp_list = sorted(public_chirp_list, reverse=True)
      # appends the item at index 0 (should be most recent chirp ID and timestamp) to end of last public chirps
      last_public_chirps.append(sorted_chirp_list[0])
    # now we need to sort last_public_chirps and print in order of most recent
    sorted_convo_by_chirp_list = sorted(last_public_chirps, reverse=True)

    for chirp in sorted_convo_by_chirp_list:
      for key, value in chirps.items():
        if value.uuid == chirp[1]:

          # formats time to be more human readable
          # could be a service function
          if value.timestamp.hour > 12:
            hour = value.timestamp.hour - 12
            time = "PM"
          else:
            hour = value.timestamp.hour
            time = "AM"
          if value.timestamp.minute < 10:
            minute = "0{}".format(value.timestamp.minute)
          else:
            minute = value.timestamp.minute

          day = value.timestamp.day
          month = value.timestamp.month
          year = value.timestamp.year

          chirp.append(counter)
          print("{}/{}/{} - {}:{} {}".format(month, day, year, hour, minute, time))
          print("{}. {}".format(counter, value.text))
          counter += 1

    print("")
    print("PRIVATE CONVERSATIONS:")
    print("----------------------")
    private_convo_list = list()
    for key, value in conversations.items():
      if value.public_status == False and uuid in value.allowed_users:
        private_convo_list.append([value.timestamp, value.uuid])

    last_private_chirps = list()
    for convo in private_convo_list:
      # for each convo, loop through chirps to find matching chirps
      private_chirp_list = list()
      for key, value in chirps.items():
        if convo[1] == value.convo_id:
          # for matching chirps, append chirp timestamp and ID to temp list
          private_chirp_list.append([value.timestamp, value.uuid])
      # now that convo_list is loaded, sort through chirps from newest to oldest
      sorted_private_list = sorted(private_chirp_list, reverse=True)
      # appends the item at index 0 (should be most recent chirp ID and timestamp) to end of last public chirps
      last_private_chirps.append(sorted_private_list[0])
    # now we need to sort last_private_chirps and print in order of most recent
    sorted_private_by_chirp_list = sorted(last_private_chirps, reverse=True)

    for chirp in sorted_private_by_chirp_list:
      for key, value in chirps.items():
        if value.uuid == chirp[1]:

          # formats time to be more human readable
          # could be a service function
          if value.timestamp.hour > 12:
            hour = value.timestamp.hour - 12
            time = "PM"
          else:
            hour = value.timestamp.hour
            time = "AM"
          if value.timestamp.minute < 10:
            minute = "0{}".format(value.timestamp.minute)
          else:
            minute = value.timestamp.minute

          day = value.timestamp.day
          month = value.timestamp.month
          year = value.timestamp.year

          chirp.append(counter)
          print("{}/{}/{} - {}:{} {}".format(month, day, year, hour, minute, time))
          print("{}. {}".format(counter, value.text))
          counter += 1
    print("")
    print("{}. RETURN TO PREVIOUS MENU".format(counter))
    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number next to your chosen chirp!")

    choice = input("> ")
    # if user choice is == counter, should run the function for logged in menu again
    # else if choice is in the counter range (without actually being the current counter number), grab the corresponding chirp in either of the sorted lists
    # toggles the error variables if the user has picked something outside of the range
    try:
      if int(choice) == counter:
        logged_in_user_menu(uuid)
        break
      elif int(choice) in range(1, counter):
        for chirp in sorted_convo_by_chirp_list:
          if int(choice) == chirp[2]:
            view_chirp_thread(uuid, chirp[1])
        for chirp in sorted_private_by_chirp_list:
          if int(choice) == chirp[2]:
            view_chirp_thread(uuid, chirp[1])
        break
      else:
        menu_error = True
    except ValueError:
      menu_not_num = True

def view_chirp_thread(uuid, chirp_id, can_edit=True):
  """Runs view chirp thread menu.

  Arguments:
  - uuid - passed in uuid from user creation/selection
  - chirp_id - ID of the chosen chirp from view all chirps function

  Actions:
  - displays all chirps associated with a specific chirp convo
  - sorts them so they display in order of oldest to newest
  - allows user to reply and add to the thread
  """

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  global chirps
  global user_list

  while True:
    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    current_convo_chirps = list()
    for key, value in chirps.items():
      if value.convo_id == chirps[chirp_id].convo_id:
        current_convo_chirps.append([value.timestamp, value.text, value.user_id])
    sorted_current_convo_chirps = sorted(current_convo_chirps)

    print("CHIRP THREAD")
    print("~~~~~~~~~~~~")
    print("*Displaying chirps oldest to newest*")
    if can_edit == False:
      print("*Please return to the main menu and login in order to reply to this thread*")
    print("")

    for chirp in sorted_current_convo_chirps:

    # formats time to be more human readable
      # could be a service function
      if chirp[0].hour > 12:
        hour = chirp[0].hour - 12
        time = "PM"
      else:
        hour = chirp[0].hour
        time = "AM"
      if chirp[0].minute < 10:
        minute = "0{}".format(chirp[0].minute)
      else:
        minute = chirp[0].minute

      day = chirp[0].day
      month = chirp[0].month
      year = chirp[0].year

      print("{}/{}/{} - {}:{} {} --- {}".format(month, day, year, hour, minute, time, user_list[chirp[2]].screenname))
      print("--------------------------------------")
      print(chirp[1])
      print("")

    if can_edit == False:
      print("1. RETURN TO PREVIOUS MENU")
    else:
      print("1. REPLY")
      print("2. RETURN TO PREVIOUS MENU")
    # runs if user has put in number outside of menu range
    if menu_error == True:
      menu_error = False
      print("Please pick an available option!")

    # runs if user has put in a non-number/invalid selection
    if menu_not_num == True:
      menu_not_num = False
      print("Please choose the number next to your chosen chirp!")

    choice = input("> ")

    try:
      if int(choice) == 1 and can_edit == True:
        reply_to_thread_menu(uuid, chirps[chirp_id].convo_id)
        break
      elif int(choice) == 1 and can_edit == False:
        view_public_menu()
        break
      elif int(choice) == 2 and can_edit == True:
        view_all_chirps_menu(uuid)
        break
      else:
        menu_error = True
    except ValueError:
      menu_not_num = True

def reply_to_thread_menu(uuid, convo_id):
  """Runs reply to chirp thread menu.

  Arguments:
  - uuid - passed in uuid from user creation/selection
  - convo_id - ID of the chosen conversation that the reply will belong to

  Actions:
  - writes a new chirp
  - attaches chirp to existing conversation
  - serializes chirps
  """

  text_length_error = False

  while True:
    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("NEW REPLY CHIRP")
    print("~~~~~~~~~~~~~~~~~")
    print("Enter chirp text (or enter 'exit' to return):")

    # runs if user has hit enter without providing input
    if text_length_error == True:
      print("Chirp length cannot be 0 characters. Please provide valid input.")
    else:
      print("")
    reply_chirp = input("> ")

    # toggles error variable for text_length if user has neglected to put in any input
    if len(reply_chirp) == 0:
      text_length_error = True
      continue
    # lets user exit back to the previous menu
    elif reply_chirp == 'exit':
      getting_input = False
      logged_in_user_menu(uuid)
    # creates the new chirp and a new corresponding conversation
    # serializes global variables for conversations and chirps
    else:
      chirp = Chirp(uuid, convo_id, reply_chirp)
      global chirps
      chirps[chirp.uuid] = chirp
      serialize_chirps(chirps)

      new_reply_chirp_success(chirp, uuid)
      break

def new_reply_chirp_success(chirp_data, uuid):
  """confirms chirp success and transitions back to logged_in menu"""

  # clears the command line/shell of other text outside of what prints after this point
  os.system('cls' if os.name == 'nt' else 'clear')

  # formats time to be more human readable
  if chirp_data.timestamp.hour > 12:
    hour = chirp_data.timestamp.hour - 12
    time = "PM"
  else:
    hour = chirp_data.timestamp.hour
    time = "AM"
  if chirp_data.timestamp.minute < 10:
    minute = "0{}".format(chirp_data.timestamp.minute)
  else:
    minute = chirp_data.timestamp.minute

  print("SUCCESS!")
  print("~~~~~~~~")
  print("You have successfully sent a reply chirp at {}:{} {}. Please press any button to return to the main menu".format(hour, minute, time))
  input("")
  # sends user back to logged_in menu
  logged_in_user_menu(uuid)

def new_public_chirp_menu(uuid):
  """Runs new public chirp menu.

  Arguments:
  - uuid - passed in uuid from user creation/selection

  Actions:
  - creates new conversation based on default class values for allowed_users and public_status
  - creates new chirp with passed in uuid and convo.uuid
  - serializes global variables conversations and chirps
  """

  text_length_error = False

  while True:
    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("NEW CHIRP: PUBLIC")
    print("~~~~~~~~~~~~~~~~~")
    print("Enter chirp text (or enter 'exit' to return):")

    # runs if user has hit enter without providing input
    if text_length_error == True:
      print("Chirp length cannot be 0 characters. Please provide valid input.")
    else:
      print("")
    pub_chirp = input("> ")

    # toggles error variable for text_length if user has neglected to put in any input
    if len(pub_chirp) == 0:
      text_length_error = True
      continue
    # lets user exit back to the previous menu
    elif pub_chirp == 'exit':
      getting_input = False
      logged_in_user_menu(uuid)
    # creates the new chirp and a new corresponding conversation
    # serializes global variables for conversations and chirps
    else:
      convo = Conversation()
      global conversations
      conversations[convo.uuid] = convo
      serialize_convo(conversations)

      chirp = Chirp(uuid, convo.uuid, pub_chirp)
      global chirps
      chirps[chirp.uuid] = chirp
      serialize_chirps(chirps)

      new_public_chirp_success_menu(chirp, uuid)
      break

def new_public_chirp_success_menu(chirp_data, uuid):
  """confirms chirp success and transitions back to logged_in menu"""

  # clears the command line/shell of other text outside of what prints after this point
  os.system('cls' if os.name == 'nt' else 'clear')

  # formats time to be more human readable
  if chirp_data.timestamp.hour > 12:
    hour = chirp_data.timestamp.hour - 12
    time = "PM"
  else:
    hour = chirp_data.timestamp.hour
    time = "AM"
  if chirp_data.timestamp.minute < 10:
    minute = "0{}".format(chirp_data.timestamp.minute)
  else:
    minute = chirp_data.timestamp.minute

  print("SUCCESS!")
  print("~~~~~~~~")
  print("You have successfully created a new public chirp at {}:{} {}. Please press any button to return to the main menu".format(hour, minute, time))
  input("")
  # sends user back to logged_in menu
  logged_in_user_menu(uuid)

def private_chirp_addressed_user(uuid):
  """determines who private chirp is meant to be addressed to

  Arguments:
  - uuid - passed in uuid from user creation/selection

  Actions:
  - accepts user input to determine who the chosen recipient of private chirp is
  - runs new_private_chirp_menu() and passes along uuids
  """

  # menu error variables to toggle visible error states from within while loop
  menu_error = False
  menu_not_num = False

  while True:

    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("WHO IS THIS PRIVATE CHIRP ADDRESSED TO?")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    # runs loop to read and print all usernames
    # assigns a number to each screenname based on counter
    # adds each number/uuid as key/value pair to temp dict, matches number and screenname printed in command line/shell
    # does NOT include the name/uuid of the current user
    # could also have used enumerate
    counter = 1
    temp_user_list = dict()
    for key, value in user_list.items():
      if value.uuid == uuid:
        continue
      else:
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
        logged_in_user_menu(uuid)
        break
      elif int(choice) in temp_user_list:
        new_private_chirp_menu(uuid, temp_user_list[int(choice)])
        break
      else:
        menu_error = True
    except ValueError:
      menu_not_num = True

def new_private_chirp_menu(uuid, recip_uuid):
  """Runs new private chirp menu.

  Arguments:
  - uuid - passed in uuid from user creation/selection

  Actions:
  - creates new conversation and passes in values for class arguments allowed_users and public_status
  - creates new chirp with passed in uuid and convo.uuid
  - serializes global variables conversations and chirps
  """

  allowed_users = (uuid, recip_uuid)

  text_length_error = False

  while True:
    # clears the command line/shell of other text outside of what prints in the while loop
    os.system('cls' if os.name == 'nt' else 'clear')

    print("NEW CHIRP: PRIVATE")
    print("~~~~~~~~~~~~~~~~~")
    print("You are starting a new private conversation with {}".format(user_list[recip_uuid].screenname))
    print("Enter chirp text (or enter 'exit' to return):")

    # runs if user has hit enter without providing input
    if text_length_error == True:
      print("Chirp length cannot be 0 characters. Please provide valid input.")
    else:
      print("")
    priv_chirp = input("> ")

    # toggles error variable for text_length if user has neglected to put in any input
    if len(priv_chirp) == 0:
      text_length_error = True
      continue
    # lets user exit back to the previous menu
    elif priv_chirp == 'exit':
      getting_input = False
      logged_in_user_menu(uuid)
    # creates the new chirp and a new corresponding conversation
    # serializes global variables for conversations and chirps
    else:
      convo = Conversation(allowed_users, False)
      global conversations
      conversations[convo.uuid] = convo
      serialize_convo(conversations)

      chirp = Chirp(uuid, convo.uuid, priv_chirp)
      global chirps
      chirps[chirp.uuid] = chirp
      serialize_chirps(chirps)

      new_private_chirp_success_menu(chirp, uuid, recip_uuid)
      break

def new_private_chirp_success_menu(chirp_data, uuid, recip_uuid):
  """confirms chirp success and transitions back to logged_in menu"""

  global user_list

  # clears the command line/shell of other text outside of what prints after this point
  os.system('cls' if os.name == 'nt' else 'clear')

  # formats time to be more human readable
  if chirp_data.timestamp.hour > 12:
    hour = chirp_data.timestamp.hour - 12
    time = "PM"
  else:
    hour = chirp_data.timestamp.hour
    time = "AM"
  if chirp_data.timestamp.minute < 10:
    minute = "0{}".format(chirp_data.timestamp.minute)
  else:
    minute = chirp_data.timestamp.minute

  print("SUCCESS!")
  print("~~~~~~~~")
  print("You have successfully created a new private chirp sent to {} at {}:{} {}. Please press any button to return to the main menu".format(user_list[recip_uuid].screenname, hour, minute, time))
  input("")
  # sends user back to logged_in menu
  logged_in_user_menu(uuid)

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
set_conversations()
main_menu_start()
