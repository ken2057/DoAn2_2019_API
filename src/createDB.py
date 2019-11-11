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
                {'_id': 'duy', 'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'role': 'admin', 'borrowed': [temp]},
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
                    'subjects': ['ab', 'cd'],
                    'books': [ 'duy', '', '', '' ],
                    'image': 'https://i2.wp.com/www.fatosmorina.com/wp-content/uploads/2018/11/hello-world.png?ssl=1',
                    'deleted': False
                },
                {
                    '_id': 2, 
                    'name': 'Angular', 
                    'author': 'Jacky', 
                    'subjects': ['cd'],
                    'books': ['', ''],
                    'image': 'https://cdn.auth0.com/blog/angular5/logo.png',
                    'deleted': False
                },
                {
                    '_id': 3, 
                    'name': 'Python', 
                    'author': 'Mao', 
                    'subjects': ['ab'],
                    'books': [''],
                    'image': 'https://techtalk.vn/wp-content/uploads/2016/04/171-696x435.jpg',
                    'deleted': False
                },
                {
                    '_id': 4, 
                    'name': 'Erlang', 
                    'subjects': ['a'], 
                    'author': 'Env', 
                    'books': [], 
                    'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Erlang_logo.svg/220px-Erlang_logo.svg.png', 
                    'deleted': False
                },
                {
                    '_id': 5, 
                    'name': 'Internship',
                    'author': 'Jame', 
                    'subjects': ['a'],
                    'books': [], 
                    'image': 'https://crosstalk.cell.com/hs-fs/hubfs/Images/Ali%20Edraki/Lessons%20from%20the%20first%20ever%20Cell%20Press%20editorial%20internship/internship-featured.jpg?width=1000&name=internship-featured.jpg', 
                    'deleted': False
                },
                {
                    '_id': 6, 
                    'name': 'Machine Learning', 
                    'author': 'Rock', 
                    'subjects': ['a'],
                    'books': [], 
                    'image': 'https://miro.medium.com/max/2400/1*c_fiB-YgbnMl6nntYGBMHQ.jpeg', 
                    'deleted': False
                },
            ])

        except Exception as e:
            print(e)

        # borrowed
        try:
            db.borrowed.insert_one(temp)

        except Exception as e:
            print(e)

        #subject
        try:
            db.subject.insert_many([
                {'_id': 'a'},
                {'_id': 'ab'},
                {'_id': 'cd'},
            ])
        except Exception as e:
            print(e)