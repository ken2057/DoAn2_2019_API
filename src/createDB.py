from src.configs import db

if True:
    # client.drop_database('library')
    print(db.bookTitle.find_one({'_id': int('1')}))
else:
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
                {'_id': 1, 'name': 'Hello world', 'author': 'David', 'price': 200000},
                {'_id': 2, 'name': 'Angular', 'author': 'Jacky', 'price': 250000},
                {'_id': 3, 'name': 'Python', 'author': 'Mao', 'price': 500000},
                {'_id': 4, 'name': 'Erlang', 'author': 'Env', 'price': 25000},
                {'_id': 5, 'name': 'Internship', 'author': 'Jame', 'price': 150000},
                {'_id': 6, 'name': 'Machine Learning', 'author': 'Rock', 'price': 300000},
            ])
        except Exception as e:
            print(e)