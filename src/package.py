# all the same import of api will be here
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
import logging

from src.configs import db, client