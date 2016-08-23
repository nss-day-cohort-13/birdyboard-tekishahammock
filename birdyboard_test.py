import unittest
from birdyboard import *

class TestBehavior(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    """setting up test class"""
    self.birdyboard = BirdyBoard()

  def test_main_menu_selection(self):
    """Testing main menu handles user input correctly"""
    # Test that option 1 runs function to add new user
    self.assertEqual(self.birdyboard.main_menu_selection(1), "adding user")
    # Test that option 2 runs function to find existing user
    self.assertEqual(self.birdyboard.main_menu_selection(2), "finding user")
    # Test that option 3 runs function to view ONLY public chirps
    self.assertEqual(self.birdyboard.main_menu_selection(3), "viewing chirps")
    # Test that exception will be raised if user puts in anything other than integer between 1-4
    self.assertRaises(Exception, self.birdyboard.main_menu_selection(5))

  def test_public_chirp_view(self):
    """Testing that public chirps are displayed to anonymous users"""
    # Test that function successfully displays chirps marked public from chirps.txt
    # Test that function limits display of each chirp to x number of characters
    # Test that exception will be raised if user puts in anything other than integer between first and last selection number
    # Test that selection will run function to display full chirp's contents
    # Test that last option generated runs function for main menu

  def test_specific_public_chirp_view_read_only(self):
    """Testing that specific chirp will display as read-only for anonymous users"""
    # Test that function will return full length of chirp and all attached comments
    # Test that exception will be raised if user puts in anything other than integer == 1
    # Test that option 1 will run function to view all public chirps

  def test_adding_new_user(self):
    """Testing that new users are correctly added to users.txt"""
    # Test that function accepts two sets of alphanumeric input
    # Test that function generates new random userID
    # Test that user input and ID are successfully added to users.txt file
    # Test that on successful completion that function for user menu is run

  def test_selecting_existing_user(self):
    """Testing that existing users are correctly matched to users.txt"""
    # Test that input accepts alphanumeric input
    # Test that exception raised if input does not exist in users.txt
    # Test that successful matching of input to users.txt will run function for user menu

  def test_user_menu(self):
    """Testing that user menu handles user input correctly"""
    # Test that exception will be raised if user puts in anything other than integer between 1-4
    # Test that option 1 runs function to interact with all chirps
    # Test that option 2 runs function to make new public chirp
    # Test that option 3 runs function to make new private chirp
    # Test that option 4 returns option to end program

  def test_all_chirp_view(self):
    """Testing that public and privately addressed chirps are displayed to named users"""
    # Test that function successfully displays public chirps and private chirps addressed to user from chirps.txt
    # Test that function limits display of each chirp to x number of characters
    # Test that exception will be raised if user puts in anything other than integer between first and last option number
    # Test that selection will run function to display full chirp's contents
    # Test that last option generated runs function for user menu

  def test_specific_chirp_view_read_write(self):
    """Testing that specific chirp will display with read-reply access for named users"""
    # Test that function will return full length of chirp and all attached comments
    # Test that exception will be raised if user puts in anything other than either integer == 1 or 2
    # Test that option 1 will run function to reply to current chirp
    # Test that option 2 will run function to view all public and privately addressed chirps chirps

  def test_reply_to_existing_chirp(self):
    """Testing that users can successfully reply to existing chirps"""
    # Test that function successfully writes reply as comment to current chirp in chirp.txt
    # Test that function successfully includes username with chirp comment to chirps.txt
    # Test that submitting chirp runs function for chirp posting success

  def test_posted_chirp_success(self):
    """Testing that successful chirp post (reply, new-public, and new-private) route back to user menu"""
    # Test that any input will run function to display user menu

  def test_create_new_public_chirp(self):
    """Testing that users can successfully create new public chirps"""
    # Test that function successfully writes new chirp to chirps.txt
    # Test that successful write to chirps.txt includes username, chirp ID, public-chirp status, and chirp contents
    # Test that submitting chirp runs function for chirp posting success

  def test_create_new_private_chirp(self):
    """Testing that users can successfully create new private chirps addressed to other users"""
    # Test that function displays list of all available users to chirp at
    # Test that exception will be raised if user puts in anything other than integer between first and last option number
    # Test that function successfully writes new chirp to chirps.txt
    # Test that successful write to chirps.txt includes username, chirp ID, public-chirp status, and chirp contents
    # Test that submitting chirp runs function for chirp posting success

if __name__ == '__main__':
  unittest.main()
