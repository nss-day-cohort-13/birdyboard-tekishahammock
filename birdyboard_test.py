import unittest
from birdyboard import *

class TestBehavior(unittest.TestCase):

  @classmethod
  def setUpClass(self):
  """setting up test class"""
    self.birdyboard = Birdyboard()

  def main_menu(self):
  """Testing main menu function handles user input correctly"""
    # Test that exception will be raised if user puts in anything other than integer between 1-4
    # Test that option 1 runs function to add new user
    # Test that option 2 runs function to find existing user
    # Test that option 3 runs function to view ONLY public chirps
    # Test that option 4 returns option to end program

  def public_chirp_view(self):
    # Test that function successfully displays chirps marked public from chirps.txt
    # Test that function limits display of each chirp to x number of characters
    # Test that exception will be raised if user puts in anything other than integer between first and last selection number
    # Test that selection will run function to display full chirp's contents
    # Test that last option generated runs function for main menu

  def specific_public_chirp_view_read_only(self):
    # Test that function will return full length of chirp and all attached comments
    # Test that exception will be raised if user puts in anything other than integer == 1
    # Test that option 1 will run function to view all public chirps

  def adding_new_user(self):
    # Test that function accepts two sets of alphanumeric input
    # Test that function generates new random userID
    # Test that user input and ID are successfully added to users.txt file
    # Test that on successful completion that function for user menu is run

  def selecting_existing_user(self):
    # Test that input accepts alphanumeric input
    # Test that exception raised if input does not exist in users.txt
    # Test that successful matching of input to users.txt will run function for user menu

  def user_menu(self):
    # Test that exception will be raised if user puts in anything other than integer between 1-4
    # Test that option 1 runs function to interact with all chirps
    # Test that option 2 runs function to make new public chirp
    # Test that option 3 runs function to make new private chirp
    # Test that option 4 returns option to end program

  def all_chirp_view(self):
    # Test that function successfully displays public chirps and private chirps addressed to user from chirps.txt
    # Test that function limits display of each chirp to x number of characters
    # Test that exception will be raised if user puts in anything other than integer between first and last option number
    # Test that selection will run function to display full chirp's contents
    # Test that last option generated runs function for user menu

  def specific_chirp_view_read_write(self):
    # Test that function will return full length of chirp and all attached comments
    # Test that exception will be raised if user puts in anything other than either integer == 1 or 2
    # Test that option 1 will run function to reply to current chirp
    # Test that option 2 will run function to view all public and privately addressed chirps chirps

  def reply_to_existing_chirp(self):
    # Test that function successfully writes reply as comment to current chirp in chirp.txt
    # Test that function successfully includes username with chirp comment to chirps.txt
    # Test that submitting chirp runs function for chirp posting success

  def posted_chirp_success(self):
    # Test that any input will run function to display user menu

  def create_new_public_chirp(self):
    # Test that function successfully writes new chirp to chirps.txt
    # Test that successful write to chirps.txt includes username, chirp ID, public-chirp status, and chirp contents
    # Test that submitting chirp runs function for chirp posting success

  def create_new_private_chirp(self):
    # Test that function displays list of all available users to chirp at
    # Test that exception will be raised if user puts in anything other than integer between first and last option number
    # Test that function successfully writes new chirp to chirps.txt
    # Test that successful write to chirps.txt includes username, chirp ID, public-chirp status, and chirp contents
    # Test that submitting chirp runs function for chirp posting success

if __name__ == '__main__':
  unittest.main()
