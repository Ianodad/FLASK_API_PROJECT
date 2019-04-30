from werkzeug.security import safe_str_cmp
from user import User


def authenticate(username, password):
    '''
    used to authenticate a user given user and password by selecting correct username
    '''
    # get user from the sqlite for authentication 
    user = User.find_by_username(username)
    # safe_str_cmp compares string helps compare secu
    if user and safe_str_cmp(user.password, password):
        return user
    # if user and user.password == password:
    #     return user


def identify(payload):
    '''
    takes in a payload has contents of the JWT content. extract user id from that payload
    '''

    #  get the token to varify with th user after encryption 
    user_id = payload['identity']
    return User.find_by_id(user_id)
