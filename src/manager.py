# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role, limitBorrow, roleHigherThanUser
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
        return 'Invalid', 400