from configs import db, client
# -----------------------------------------------------------------------------
if True:
    for i in db.account.find():
        print(i)
else:
    client.drop_database('library')

    if db.list_collection_names() == []:
        # account
        try:
            db.account.insert_many([
                {'_id': 'duy', 'password': '123', 'role': 'admin', 'borrowed': []},
                {'_id': 'bui', 'password': '123', 'role': 'manager', 'borrowed': []},
                {'_id': 'hieu', 'password': '123', 'role': 'manager', 'borrowed': []},
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
                    'books': [
                        { 'id_borrow': '' },
                        { 'id_borrow': '' },
                        { 'id_borrow': '' }
                    ]
                },
                {
                    '_id': 2, 
                    'name': 'Angular', 
                    'author': 'Jacky', 
                    'subject': ['cd'],
                    'books': [
                        { 'id_borrow': '' }
                    ]
                },
                {
                    '_id': 3, 
                    'name': 'Python', 
                    'author': 'Mao', 
                    'subject': ['ab'],
                    'books': [
                        { 'id_borrow': '' },
                        { 'id_borrow': '' }
                    ]
                },
                {'_id': 4, 'name': 'Erlang', 'subject': ['a'],'author': 'Env', 'books': []},
                {'_id': 5, 'name': 'Internship', 'author': 'Jame', 'books': []},
                {'_id': 6, 'name': 'Machine Learning', 'author': 'Rock', 'books': []},
            ])
        except Exception as e:
            print(e)