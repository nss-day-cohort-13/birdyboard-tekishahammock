"""The Menus Module
- Handles displaying menu screens
- Sorts data for dynamic user experience
- Passes around user choices
"""

# imports
import os
import sys
import users
import chirps
import convo
import services

# constants
USER_LIST = None
CHIRP_LIST = None
CONVERSATIONS = None

def set_user_list():
    """deserializes users.txt on app start, saves to global variable"""
    global USER_LIST
    USER_LIST = services.deserialize("users.txt")

def set_chirps():
    """deserializes chirps.txt on app start, saves to global variable"""
    global CHIRP_LIST
    CHIRP_LIST = services.deserialize("chirps.txt")

def set_conversations():
    """deserializes convo.txt on app start, saves to global variable"""
    global CONVERSATIONS
    CONVERSATIONS = services.deserialize("convo.txt")

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
        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        # runs if user has put in a non-number/invalid selection
        if menu_not_num is True:
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
                view_chirps_menu(None)
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
    name_length_error = False
    screenname_length_error = False
    screenname_match_error = False
    # name and screenname variables hold user input until both are filled out with valid input
    name = None
    screenname = None

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("CREATE A NEW USER")
        print("~~~~~~~~~~~~~~~~~")

        # runs if user has hit enter without providing input
        if name_length_error is True:
            print("Name length cannot be 0 characters. Please provide valid input.")
        else:
            print("")

        print("Enter full name:")

        # checks to see if acceptable name input has been collected already
        if name is None:
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
        if screenname_length_error is True:
            print("Screenname length cannot be 0 characters. Please provide valid input.")
            # runs if user has picked a screenname that belongs to another user
        elif screenname_match_error is True:
            print("Screenname already belongs to another user, please pick another name")
        else:
            print("")

        print("Enter screenname:")
        screenname = input("> ")

        # checks to see if user has picked a unique screenname
        for value in USER_LIST.values():
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
                user = users.User(name, screenname)
                # adds the new user to the global USER_LIST and serializes the new list
                USER_LIST[user.uuid] = user
                services.serialize("users.txt", USER_LIST)

                # routes user to the logged_in menu screen, passes along current user uuid
                logged_in_user_menu(user.uuid)
                break
        # handles error associated with len(screenname), since Nonetype object has no length
        except TypeError:
            pass

def select_user_menu():
    """Runs the select user menu.

    Actions:
    - collects the chosen user information
    - passes chosen uuid to logged_in menu function
    """
    menu_error = False
    menu_not_num = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("SELECT USER")
        print("~~~~~~~~~~~")
        print("")
        # runs loop to read and print all usernames
        # assigns a number to each screenname based on counter
        # adds each number/uuid as key/value pair to temp dict
        # matches number and screenname printed in command line/shell
        # could also have used enumerate
        counter = 1
        temp_user_list = dict()
        for value in USER_LIST.values():
            temp_user_list[counter] = value.uuid
            print("{}. {}".format(counter, value.screenname))
            counter += 1

        print("{}. RETURN TO PREVIOUS MENU".format(counter))

        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number next to your screenname!")

        choice = input("> ")
        # if user choice is == counter, should run the function for the start menu again
        # else if choice is a key in the temp_user_list dict, will run logged_in menu
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

def logged_in_user_menu(uuid):
    """Runs logged in user menu.

    Arguments:
    - uuid - allows to grab user information from global variable USER_LIST

    Actions:
    - routes user to selected menu option and corresponding function
    - user can also log out or exit app from here
    """
    menu_error = False
    menu_not_num = False

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        print("WELCOME {}!".format((USER_LIST[uuid].screenname).upper()))
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print("1. View All Chirps")
        print("2. New Public Chirp")
        print("3. New Private Chirp")
        print("4. Log Out")
        print("5. Exit")

        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number of your chosen selection!")

        choice = input("> ")

        # attempts to route the user to the functions corresponding to their selection
        try:
            if int(choice) == 1:
                # allows user to READ/REPLY to all chirps they have access to
                view_chirps_menu(uuid)
                break
            elif int(choice) == 2:
                # allows a user to WRITE a new public chirp and start a new chirp thread
                new_public_chirp_menu(uuid)
                break
            elif int(choice) == 3:
                # allows a user to WRITE a new private chirp addressed to a specific user
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
                menu_error = True
        except ValueError:
            menu_not_num = True

def view_chirps_menu(uuid):
    """Runs all chirps menu.

    Actions:
    - displays all chirps marked "public"
    - displays all chirps marked "private" and addressed to the user
    - if anonymous user, only displays public
    - routes user to expanded chirp thread
    """
    menu_error = False
    menu_not_num = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        # list of most recent chirp for all conversations
        last_chirps = list()

        # loads last_chirp list
        for key in CONVERSATIONS:
            # creates a list to hold all chirp-IDs and timestamps associated with a conversation
            chirps_in_convo = list()
            for value in CHIRP_LIST.values():
                if key == value.convo_id:
                    chirps_in_convo.append([value.timestamp, value.uuid])
            # sorts chirps_in_convo so most recent chirp is index 0
            sorted_chirps_by_time = sorted(chirps_in_convo, reverse=True)
            # appends last chirp in each convo to last_chirps list
            last_chirps.append(sorted_chirps_by_time[0])

        # list of last chirp in each public and private conversation
        public_convo_list = list()
        private_convo_list = list()

        # loads public_convo_list and private_convo_list with last chirps
        for chirp in last_chirps:
            current_convo_id = CHIRP_LIST[chirp[1]].convo_id
            is_public = CONVERSATIONS[current_convo_id].public_status
            if is_public is True:
                public_convo_list.append(chirp)
            elif is_public is False and uuid in CONVERSATIONS[current_convo_id].allowed_users:
                private_convo_list.append(chirp)
            else:
                continue

        # list of last chirp in each public and private conversation, sorted by timestamp
        sorted_public_chirps = sorted(public_convo_list, reverse=True)
        sorted_private_chirps = sorted(private_convo_list, reverse=True)

        # # list of most recent 10 chirps each public and private conversations
        last_ten_public = sorted_public_chirps[:10]
        last_ten_private = sorted_private_chirps[:10]

        # "if uuid is None" will handle what happens if user is viewing chirps anonymously
        if uuid is None:
            print("CHIRPS: * PUBLIC ONLY *")
        else:
            print("CHIRPS: PUBLIC AND PRIVATE")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("* Showing most recent chirp from last ten public and private conversations *")

        if uuid is None:
            print("* Please return to main menu and select a user to reply to chirps *")

        print("")
        print("PUBLIC CONVERSATIONS:")
        print("---------------------")

        counter = 1

        # takes chirp ID from last 10 and loads the rest of the chirp info
        for chirp in last_ten_public:
            current_chirp = CHIRP_LIST[chirp[1]]

            # formats visible timestamp to be more human readable
            timestamp = services.readable_time(current_chirp.timestamp)

            # adds counter to individual chirp as temp option marker
            chirp.append(counter)
            print(counter, end="")
            print(". {}/{}/{} - {}:{} {}".format(*timestamp), end="")
            print(": {}".format(current_chirp.text))
            counter += 1

        if len(sorted_public_chirps) > 10:
            print("{}. VIEW MORE PUBLIC CONVERSATIONS".format(counter))
            counter += 1

        if uuid is not None:
            print("")
            print("PRIVATE CONVERSATIONS:")
            print("----------------------")

            for chirp in last_ten_private:
                current_chirp = CHIRP_LIST[chirp[1]]

                timestamp = services.readable_time(current_chirp.timestamp)

                chirp.append(counter)
                print(counter, end="")
                print(". {}/{}/{} - {}:{} {}".format(*timestamp), end="")
                print(": {}".format(current_chirp.text))
                counter += 1

            if len(sorted_private_chirps) > 10:
                print("{}. VIEW MORE PRIVATE CONVERSATIONS".format(counter))
                counter += 1

        print("")
        print("{}. RETURN TO PREVIOUS MENU".format(counter))
        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number next to your chosen chirp!")

        choice = input("> ")
        # if user choice is == counter, should run the function for logged in menu again
        # else if choice is in the counter range grab the corresponding chirp in either list
        try:
            if int(choice) == counter and uuid is None:
                main_menu_start()
                break
            elif int(choice) == counter and uuid is not None:
                logged_in_user_menu(uuid)
                break
            elif int(choice) == 11 and len(sorted_public_chirps) > 10:
                view_more_chirps(uuid, "public")
            elif int(choice) == (counter - 1) and len(sorted_private_chirps) > 10:
                view_more_chirps(uuid, "private")
            elif int(choice) in range(1, counter):
                for chirp in last_ten_public:
                    if int(choice) == chirp[2]:
                        view_chirp_thread(uuid, chirp[1])
                for chirp in last_ten_private:
                    if int(choice) == chirp[2]:
                        view_chirp_thread(uuid, chirp[1])
                break
            else:
                menu_error = True
        except ValueError:
            menu_not_num = True

def view_more_chirps(uuid, chirp_type):
    """Runs view more chirps menu.

    Arguments:
    - uuid - passed in uuid from user creation/selection
    - chirp_type - determines if we are loading public or private chirps

    Actions:
    - displays last chirp of all conversations based of public/private status
    - sorts them so they display in order of newest to oldest
    - allows user to pick a thread to see more
    """

    if uuid is not None:
        username = (USER_LIST[uuid].screenname).upper()

    menu_error = False
    menu_not_num = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        last_chirps = list()

        # Had to rebuild chirp list because passed-in list inherited edits made to derivative lists
        for key in CONVERSATIONS:
            chirps_in_convo = list()
            for value in CHIRP_LIST.values():
                if key == value.convo_id:
                    chirps_in_convo.append([value.timestamp, value.uuid])
            sorted_chirps_by_time = sorted(chirps_in_convo, reverse=True)
            last_chirps.append(sorted_chirps_by_time[0])

        all_convo_list = list()

        requested_chirp_type = True if chirp_type is "public" else False

        for chirp in last_chirps:
            current_convo_id = CHIRP_LIST[chirp[1]].convo_id
            is_public = CONVERSATIONS[current_convo_id].public_status
            if is_public == requested_chirp_type:
                all_convo_list.append(chirp)
            else:
                continue

        sorted_convo_list = sorted(all_convo_list, reverse=True)

        print(sorted_convo_list)
        print("\n")

        if chirp_type == "private":
            print("VIEWING ALL PRIVATE CONVERSATIONS ADDRESSED TO {}".format(username))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            print("VIEWING ALL PUBLIC CONVERSATIONS")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~")

        print("* Showing with most recently updated conversations at the top *")

        if uuid is None:
            print("* Please return to main menu and select a user to reply to chirps *")

        print("")

        counter = 1

        for chirp in sorted_convo_list:
            current_chirp = CHIRP_LIST[chirp[1]]

            timestamp = services.readable_time(current_chirp.timestamp)

            chirp.append(counter)
            print(counter, end="")
            print(". {}/{}/{} - {}:{} {}".format(*timestamp), end="")
            print(": {}".format(current_chirp.text))
            counter += 1

        print("")
        print("{}. RETURN TO PREVIOUS MENU".format(counter))
        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number next to your chosen chirp!")

        choice = input("> ")

        try:
            if int(choice) == counter:
                view_chirps_menu(uuid)
                break
            elif int(choice) in range(1, counter):
                for chirp in sorted_convo_list:
                    if int(choice) == chirp[2]:
                        view_chirp_thread(uuid, chirp[1])
                break
            else:
                menu_error = True
        except ValueError:
            menu_not_num = True

def view_chirp_thread(uuid, chirp_id):
    """Runs view chirp thread menu.

    Arguments:
    - uuid - passed in uuid from user creation/selection
    - chirp_id - ID of the chosen chirp from view all chirps function

    Actions:
    - displays all chirps associated with a specific chirp convo
    - sorts them so they display in order of oldest to newest
    - allows user to reply and add to the thread
    """
    menu_error = False
    menu_not_num = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        # loads all chirps associated with conversation into list
        current_convo_chirps = list()
        for value in CHIRP_LIST.values():
            if value.convo_id == CHIRP_LIST[chirp_id].convo_id:
                current_convo_chirps.append([value.timestamp, value.text, value.user_id])

        # sorts current_convo_chirps from oldest to newest
        sorted_current_convo_chirps = sorted(current_convo_chirps)

        print("CHIRP THREAD")
        print("~~~~~~~~~~~~")
        print("*Displaying chirps oldest to newest*")

        if uuid is None:
            print("*Please return to the main menu and login in order to reply to this thread*")

        print("")

        for chirp in sorted_current_convo_chirps:
            timestamp = services.readable_time(chirp[0])

            print("{}/{}/{} - {}:{} {}".format(*timestamp))
            print(USER_LIST[chirp[2]].screenname, " --- ", chirp[1])
            print("")

        if uuid is None:
            print("1. RETURN TO PREVIOUS MENU")
        else:
            print("1. REPLY")
            print("2. RETURN TO PREVIOUS MENU")

        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number next to your chosen chirp!")

        choice = input("> ")

        try:
            if int(choice) == 1 and uuid is not None:
                reply_to_thread_menu(uuid, CHIRP_LIST[chirp_id].convo_id)
                break
            elif int(choice) == 1 and uuid is None:
                view_chirps_menu(None)
                break
            elif int(choice) == 2 and uuid is not None:
                view_chirps_menu(uuid)
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
        os.system('cls' if os.name == 'nt' else 'clear')

        print("NEW REPLY CHIRP")
        print("~~~~~~~~~~~~~~~~~")
        print("Enter chirp text (or enter 'exit' to return):")

        # runs if user has hit enter without providing input
        if text_length_error is True:
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
            logged_in_user_menu(uuid)
            break
        # creates the new chirp
        # serializes global variables for CHIRP_LIST
        else:
            chirp = chirps.Chirp(uuid, convo_id, reply_chirp)
            CHIRP_LIST[chirp.uuid] = chirp
            services.serialize("chirps.txt", CHIRP_LIST)

            new_chirp_success(chirp, uuid)
            break

def new_chirp_success(chirp_data, uuid, recip_uuid=None):
    """confirms chirp success and transitions back to logged_in menu"""
    os.system('cls' if os.name == 'nt' else 'clear')

    timestamp = services.readable_time(chirp_data.timestamp)

    print("SUCCESS!")
    print("~~~~~~~~")
    print("You have successfully sent a chirp on {}/{}/{} at {}:{} {}.".format(*timestamp))
    if recip_uuid is not None:
        print("It was sent to {}".format(USER_LIST[recip_uuid].screenname))
    print("Please press any button to return to the main menu.")
    input("")
    # sends user back to logged_in menu, regardless of input
    logged_in_user_menu(uuid)

def new_public_chirp_menu(uuid):
    """Runs new public chirp menu.

    Arguments:
    - uuid - passed in uuid from user creation/selection

    Actions:
    - creates new conversation based on default class values for allowed_users and public_status
    - creates new chirp with passed in uuid and convo.uuid
    - serializes global variables CONVERSATIONS and CHIRP_LIST
    """
    text_length_error = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("NEW CHIRP: PUBLIC")
        print("~~~~~~~~~~~~~~~~~")
        print("Enter chirp text (or enter 'exit' to return):")

        if text_length_error is True:
            print("Chirp length cannot be 0 characters. Please provide valid input.")
        else:
            print("")

        pub_chirp = input("> ")

        if len(pub_chirp) == 0:
            text_length_error = True
            continue
        elif pub_chirp == 'exit':
            logged_in_user_menu(uuid)
            break
        # creates the new chirp and a new corresponding conversation
        # serializes global variables for CONVERSATIONS and CHIRP LIST
        else:
            new_convo = convo.Conversation()
            CONVERSATIONS[new_convo.uuid] = new_convo
            services.serialize("convo.txt", CONVERSATIONS)

            chirp = chirps.Chirp(uuid, new_convo.uuid, pub_chirp)
            CHIRP_LIST[chirp.uuid] = chirp
            services.serialize("chirps.txt", CHIRP_LIST)

            new_chirp_success(chirp, uuid)
            break

def private_chirp_addressed_user(uuid):
    """determines who private chirp is meant to be addressed to

    Arguments:
    - uuid - passed in uuid from user creation/selection

    Actions:
    - accepts user input to determine who the chosen recipient of private chirp is
    - runs new_private_chirp_menu() and passes along uuids
    """
    menu_error = False
    menu_not_num = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("WHO IS THIS PRIVATE CHIRP ADDRESSED TO?")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        # does NOT include the name/uuid of the current user
        counter = 1
        temp_user_list = dict()
        for value in USER_LIST.values():
            if value.uuid == uuid:
                continue
            else:
                temp_user_list[counter] = value.uuid
                print("{}. {}".format(counter, value.screenname))
                counter += 1

        print("{}. RETURN TO PREVIOUS MENU".format(counter))

        if menu_error is True:
            menu_error = False
            print("Please pick an available option!")

        if menu_not_num is True:
            menu_not_num = False
            print("Please choose the number next to your screenname!")

        choice = input("> ")

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
    - creates new conversation
    - passes in values for class arguments allowed_users and public_status
    - creates new chirp with passed in uuid and convo.uuid
    - serializes global variables CONVERSATIONS and CHIRP_LIST
    """
    allowed_users = (uuid, recip_uuid)
    text_length_error = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        recip_screenname = USER_LIST[recip_uuid].screenname

        print("NEW CHIRP: PRIVATE")
        print("~~~~~~~~~~~~~~~~~")
        print("You are starting a new private conversation with {}".format(recip_screenname))
        print("Enter chirp text (or enter 'exit' to return):")

        if text_length_error is True:
            print("Chirp length cannot be 0 characters. Please provide valid input.")
        else:
            print("")

        priv_chirp = input("> ")

        if len(priv_chirp) == 0:
            text_length_error = True
            continue
        elif priv_chirp == 'exit':
            logged_in_user_menu(uuid)
            break
        # creates the new chirp and a new corresponding conversation
        # serializes global variables for CONVERSATIONS and CHIRP_LIST
        else:
            new_convo = convo.Conversation(allowed_users, False)
            CONVERSATIONS[new_convo.uuid] = new_convo
            services.serialize("convo.txt", CONVERSATIONS)

            chirp = chirps.Chirp(uuid, new_convo.uuid, priv_chirp)
            CHIRP_LIST[chirp.uuid] = chirp
            services.serialize("chirps.txt", CHIRP_LIST)

            new_chirp_success(chirp, uuid, recip_uuid)
            break

def exit_app():
    """exits the program"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Bye!")
    # runs system exit, which is the same as using an exit command in the command line/shell
    sys.exit()

# runs these functions at app start
set_user_list()
set_chirps()
set_conversations()
main_menu_start()
