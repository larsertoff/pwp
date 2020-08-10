# Config file for use with netlify
import os

DEBUG = False
ENVIRONMENT = 'production'
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
SECRET_KEY = os.environ['SECRET_KEY']