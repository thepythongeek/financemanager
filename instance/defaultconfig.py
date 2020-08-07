
import os 

SECRET_KEY = 'xsahjfka483'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(os.getcwd(), 'instance/accounts.db'))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:postgres@localhost/accounts'
SQLALCHEMY_TRACK_MODIFICATIONS = True 

