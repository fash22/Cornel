class Configuration(object):
    """
    Base configuration, regardless of the environment.
    """
    SECRET_KEY='\x96\x0f\\\x8b\x9f=t\x07(pE\xfdku\xee\t'

class DevelopmentConfig(Configuration):
    """
    Configuration for development environment only
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'