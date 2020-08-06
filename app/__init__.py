
#!/usr/bin/python 

import os 
from flask import Flask 



# create an appliaction factory 
def create_app(test_config=None):
    ''' Creates a flask application object and performs all the necessary configuration.
    
    The 'test_config' parameter should be a python file containing relevant tests
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
                    SECRET_KEY = 'xsahjfka483'
                    )
    if test_config is not None:
        # load the tests configuration 
        app.config.from_pyfile(test_config)
    elif test_config is None and app.config['ENV']=='production':
        # only during production load configuration from instance folder 
        app.config.from_pyfile('config.py', silent=True)
    
    try:
        os.makedirs('instance')
    except OSError:
        pass 
    
    # import the blueprints 
    # and register them 
    from app import main 
    app.register_blueprint(main.bp)
    from app import auth 
    app.register_blueprint(auth.bp)
    
    return app 
    
    
    