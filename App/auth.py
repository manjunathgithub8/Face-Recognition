
from pyrebase import pyrebase
from getpass import getpass
import pydb

firebaseConfig = {
    
  }



firebase = pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()



def signin(email,password):
    try:
        signinv=auth.sign_in_with_email_and_password(email,password)
        
        print(signinv)
        pydb.init_db()
        pydb.init_company(signinv['email'])
        return True
    except Exception as e:
        print(e)
        return False



