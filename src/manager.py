from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging
# -----------------------------------------------------------------------------
from src.configs import db, role, limitBorrow, roleHigherThanUser
from src.utils import isJsonValid, getToken, getAccountWithId, convertDateForSeria
# -----------------------------------------------------------------------------

class GetBorrowed(Resource):
    def get(self):
        try:
            # params
            token = getToken(request.args['token'])
            try:
                page = int(request.args['page'])
            except:
                page = 0
        
            # check permission
            if token['role'] not in roleHigherThanUser:
                raise Exception('Not admin or manager: %s', token)
            
            borrowed = []
            for i in db.borrowed.find().skip(page * limitBorrow).limit(limitBorrow):
                i.pop('_id')
                borrowed.append(convertDateForSeria(i))
            
            return { 'borrowed': borrowed }, 200

        except Exception as e:
            logging.info('error getBorrowed: %s', e)
        return '', 400