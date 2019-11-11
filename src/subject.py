# all the same import of api will be here
from src.package import *

##
class GetSubjects(Resource):
    def get(self):
        subjects = []
        for subject in db.subject.find():
            subjects.append(subject['_id'])

        return {'subjects': subjects}, 200

        