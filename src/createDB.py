from configs import db, client, maxDateBorrow
from datetime import datetime, timedelta

def dateReturn(now):
    return now + timedelta(days = maxDateBorrow)

# -----------------------------------------------------------------------------
if False:
    for i in db.account.find():
        print(i)
else:
    client.drop_database('library')

    temp = {
				'username': 'duy',
				'bookId': 1,
				'status': 'On borrowing',
				'date_borrow': datetime.now(),
				'date_expire': dateReturn(datetime.now())
			}

    if db.list_collection_names() == []:
        # account
        try:
            db.account.insert_many([
                {'_id': 'duy', 'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'role': 'admin', 
                'borrowed': [temp]},
                {'_id': 'bui', 'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'role': 'manager', 'borrowed': []},
                {'_id': 'hieu', 'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'role': 'manager', 'borrowed': []},
            ])
        except Exception as e:
            print(e)

        # Author
        try:
            db.bookTitle.insert_many([
                {
                    '_id': 1, 
                    'name': 'Hello world', 
                    'author': 'David', 
                    'subject': ['ab', 'cd'],
                    'books': [ 'duy', '', '', '' ],
                    'image': ''
                },
                {
                    '_id': 2, 
                    'name': 'Angular', 
                    'author': 'Jacky', 
                    'subject': ['cd'],
                    'books': ['', ''],
                    'image': ''
                },
                {
                    '_id': 3, 
                    'name': 'Python', 
                    'author': 'Mao', 
                    'subject': ['ab'],
                    'books': [''],
                    'image': ''
                },
                {'_id': 4, 'name': 'Erlang', 'subject': ['a'],'author': 'Env', 'books': [], 'image': ''},
                {'_id': 5, 'name': 'Internship', 'author': 'Jame', 'books': [], 'image': ''},
                {'_id': 6, 'name': 'Machine Learning', 'author': 'Rock', 'books': [], 'image': ''},
            ])

        except Exception as e:
            print(e)

        # borrowed
        try:
            db.borrowed.insert_one(temp)

        except Exception as e:
            print(e)