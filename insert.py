from collections import OrderedDict
from peewee import *;
import pandas as pd

db = MySQLDatabase("mychina", host="localhost",port=3306, user="root", password="photobooth")

file = "2021MarAllCapturedSorted.csv"

class Product(Model):
	barcode = CharField(unique = True)
	length = FloatField(default=8)
	width = FloatField(default=8)
	height = FloatField(default=8)

	class Meta:
		database = db

def initialize():
	"""Create database and the table if they dont exist"""
	db.connect()
	db.create_tables([Product], safe=True)

def menu_loop():
	"""Show the menu"""
	choice = None #initializing a var without a value

	while choice != 'q':
		print("Enter 'q' to exit the program.")
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__)) #value is going to be a function __doc__ print doc string for function
			choice = input('Action: ').lower().strip()

			if choice in menu:
				menu[choice]()

def read_csv(file):
	"""This function reads data using pandas """
	data = pd.read_csv(file)
	return data

def insert_data():
	"""Insert data into the database"""
	data = read_csv(file)
	inserted = 0
	updated = 0
	for row in data.itertuples():
		try:
			Product.create(barcode = row.barcode,
				length = row.length,
				width = row.width,
				height = row.height)
			inserted=+1

		except IntegrityError:
			product_record = Product.get(barcode=row.barcode)
			product_record.length = row.length
			product_record.width = row.width
			product_record.height = row.height
			product_record.save()
			updated = updated + 1

	print("Task completed: {} inserted, {} updated".format(inserted,updated))

def search_data():
	"""This function searches data using barcode as seacrch term """

menu = OrderedDict([
	('a', insert_data),
	('v', search_data),

	])

if __name__ == '__main__':
	initialize()
	menu_loop()