from mongo import db, client
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
client.drop_database('library')

authors = ['Isaak Melmar','Burtie Beagan','Barr Haliburn','Maryrose Huot','Hestia Baylie','Richy Perham','Beaufort Tarbert','Stephani Farrah','Ashlan Picker','Tucker Whoolehan','Marin Seatter','Basilius Farr','Hamid Powys','Curran Vasilik','Karl Cappleman','Haze Hunn','Jessamyn Harrald','Willabella Barthel','Danika Tapsell','Cornell Fullerd','Sarene Lindenbaum','Thorpe Suttill','Humphrey Marshal','Ram Antonopoulos','Jacklyn Napoleon','Rena Peltz','Tracee Acklands','Kinny Servante','Yehudi Seabright','Carlye Roseby','Berkley Ruggs','Quent Uc','Dolf Phythean','Rance Adderley','Amelina Cudbird','Thalia Fibben','Meredithe Bruntje','Dalston Calderon','Talyah Hansed','Dino Sweetmore','Johna Bradnam','Jolene Bowen','Fay McIlraith','Fonz Cartmel','Jewel Aldcorne','Charlie Limeburn','Tiffani Bowle','Marijn Stayte','Vida Algate','Saundra Coverlyn','Portia Halversen','Yalonda Calendar','Grantham Seston','Carmelita Papen','Moishe Gibbett','Mady Sommerfeld','Rolf Adamowitz','Cyndia Reddick','Welsh Point','Karl Pawnsford','Shela Keggin','Fanchon Izak','Sallyanne Brussels','Leone Robison','Dex Camps','Patrick Judkin','Shina Cheeld','Ramsay Basford','Niki Crenshaw','Cordell Heynen','Kendrick Henri','Prent Geratasch','Nona Hughson','Polly Amoss','Fidole Reggio','Lorianne Ghiriardelli','Hatty Coppin','Aggie Damp','Abagael Keelinge','Josias Laviste','Zena Rogliero','Rachel Bartolomeoni','Addy Heaysman','Den Daniaud','Joni Goodsell','Taffy Bilton','Leslie Chesnut','Bear Bonnett','Roth Bonnette','Westbrook Langhor','Gladys Fearn','Nettie Radenhurst','Smitty Oxtoby','Denys Medcalf','Wynnie Plomer','Othelia Duncanson','Wildon Hurrell','Urbanus Frome','Ferguson Francecione','Faustina Kondratenya']

# account
try:
	db.account.insert_many([
		{
			'_id': 'duy', 
			'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef',
			'user_type': 'X',
			'role': 'admin', 
			'borrowed': []
		},
		{
			'_id': 'bui', 
			'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef',
			'user_type': 'X',
			'role': 'admin', 
			'borrowed': []
		},
		{
			'_id': 'hieu', 
			'password': '40bd001563085fc35165329ea1ff5c5ecbdbbeef',
			'user_type': 'X',
			'role': 'admin', 
			'borrowed': []
		},
	])
except Exception as e:
	print(e)

# Author
try:
	db.bookTitle.insert_many([
		{
			'_id': 1,
			'name': 'Hello world',
			'author': 'Isaak Melmar',
			'subjects': ['C', 'B'],
			'books': ['', '', '', ''],
			'image': 'https://i2.wp.com/www.fatosmorina.com/wp-content/uploads/2018/11/hello-world.png?ssl=1',
			'deleted': False,
			'year_released': '2019',
			'date_added': '22/10/2019',
			'publisher': 'Tiki',
			'price': 100000
		},
		{
			'_id': 2,
			'name': 'Angular',
			'author': 'Burtie Beagan',
			'subjects': ['B'],
			'books': ['', ''],
			'image': 'https://cdn.auth0.com/blog/angular5/logo.png',
			'deleted': False,
			'year_released': '2019',
			'date_added': '11/10/2019',
			'publisher': 'Tiki',
			'price': 100000
		},
		{
			'_id': 3,
			'name': 'Python',
			'author': 'Barr Haliburn',
			'subjects': ['C'],
			'books': [''],
			'image': 'https://techtalk.vn/wp-content/uploads/2016/04/171-696x435.jpg',
			'deleted': False,
			'year_released': '2019',
			'date_added': '15/10/2019',
			'publisher': 'Amazon',
			'price': 200000
		},
		{
			'_id': 4,
			'name': 'Erlang',
			'subjects': ['C'],
			'author': 'Stephani Farrah',
			'books': [''],
			'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Erlang_logo.svg/220px-Erlang_logo.svg.png',
			'deleted': False,
			'year_released': '2010',
			'date_added': '1/11/2019',
			'publisher': 'Lazada',
			'price': 20000
		},
		{
			'_id': 5,
			'name': 'Internship',
			'author': 'Hestia Baylie',
			'subjects': ['C'],
			'books': [''],
			'image': 'https://crosstalk.cell.com/hs-fs/hubfs/Images/Ali%20Edraki/Lessons%20from%20the%20first%20ever%20Cell%20Press%20editorial%20internship/internship-featured.jpg?width=1000&name=internship-featured.jpg',
			'deleted': False,
			'year_released': '2019',
			'date_added': '22/12/2019',
			'publisher': 'C',
			'price': 212121
		},
		{
			'_id': 6,
			'name': 'Machine Learning',
			'author': 'Tucker Whoolehan',
			'subjects': ['C'],
			'books': [''],
			'image': 'https://miro.medium.com/max/2400/1*c_fiB-YgbnMl6nntYGBMHQ.jpeg',
			'deleted': False,
			'year_released': '2011',
			'date_added': '22/9/2019',
			'publisher': 'C',
			'price': 1111111
		},
	])

except Exception as e:
	print(e)

# borrowed
# create temp borrowed collection
try:
	db.borrowed.insert_one({'deleted': True})

except Exception as e:
	print(e)

# log
# create temp log collection
try:
	db.logging.insert_one({'deleted': True})

except Exception as e:
	print(e)

# user type
try:
	db.user_type.insert_many([{'_id': 'X'}, {'_id': 'Y'}])
except Exception as e:
	print(e)

# author
try:
	list_author = []
	for author in authors:
		list_author.append({'name': author})
	db.author.insert_many(list_author)
except Exception as e:
	print(e)

# subject
try:
	db.subject.insert_many([
		{'_id': 'A'},
		{'_id': 'B'},
		{'_id': 'C'},
	])
except Exception as e:
	print(e)

# config
try:
	db.config.insert_many([
		{'_id': 'min_age', 'value': 18},
		{'_id': 'max_age', 'value': 50},
		{'_id': 'max_month_account_expire', 'value': 6},
		{'_id': 'max_year_publised', 'value': 8},
		{'_id': 'max_book_borrow', 'value': 5},
		{'_id': 'max_date_borrowed', 'value': 6},
	])
except Exception as e:
	print(e)

statusBorrow = {
	'_id': 'status',
	'return': 'Returned',
	'sent': 'On borrowing',
	'order': 'Watting for avaialbe',
	'lost': 'Lost',
	'wait_to_get': 'Get book from librarian',
	'paid': 'Paid',
	'cancel': 'Canceled',
	'hold_timeout': 'Hold order too long',
	'finish_paid': 'Finish Paid'
}

# status of borrow
try:
	db.status_borrow.insert_one(statusBorrow)
except Exception as e:
	print(e)

