# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------

class GetAuthor(Resource):
    def get(self):
        authors = []
        for author in db.author.find():
            authors.append({'id': str(author['_id']), 'name': author['name']})
        return {'authors': authors}, 200
