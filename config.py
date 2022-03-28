import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "df5df5d4f65d4f654f56dss6ssa5d4"
    SQLALCHEMY_DATABASE_URI = "postgresql://fzcpptcdpeiuxh:5b0cfb537916c5e389fd1938aeec0277f1c35dcc14e20cdff7250e8be714ca17@ec2-34-194-171-47.compute-1.amazonaws.com:5432/d7fgnqa6hdktu8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5