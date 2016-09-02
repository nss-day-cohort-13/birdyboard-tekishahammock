"""The Services Module
- Handles serialization of all data
- Handles deserialization of all data
- Handles datetime formating
"""
import pickle

def deserialize(filename):
    """deserializes text files for Birdyboard

    Arguments:
    - filename - name of file deserialized content is being read from
    """

    # will load last dump (which is entire serialized file)
    try:
        file = open(filename, 'rb')
        content = pickle.load(file)
    # creates an empty dict as user_list if users.txt is empty
    except EOFError:
        content = {}
    return content

def serialize(filename, content):
    """serializes text files for Birdyboard

    Arguments:
    - filename - name of file serialized content is being written to
    - content - content being serialized
    """

    # re-writes the whole users.txt file with whatever is currently being held in user_list
    file = open(filename, 'wb')
    pickle.dump(content, file)
