# martha_prep.py

# ------------------------------------- #
# IMPORTS
# ------------------------------------- #

import time 
import sqlite3
import requests
import pandas as pd 
from recipe_scrapers import scrape_me


# https://www.marthastewart.com/sitemaps/recipe/1/sitemap.xml
# https://www.marthastewart.com/sitemaps/recipe/2/sitemap.xml

# ------------------------------------- #
# VARIABLES
# ------------------------------------- #

# ------------------------------------- #
# FUNCTIONS
# ------------------------------------- #

# uploads links from the sitemap to the sqlite db
def create_recipe_db():

	conn = sqlite3.connect('recipe.db', check_same_thread=False)
	response = requests.get('https://www.marthastewart.com/sitemaps/recipe/2/sitemap.xml')
	df = pd.read_xml(response.text)
	df.to_sql(
		'martha_sitemap',
		con=conn,
		if_exists='append',
		index=False
	)
	conn.close()

# makes a list of the recipe links
def get_martha_recipe_url_list():
	
	statement = '''
		SELECT DISTINCT loc 
		FROM martha_sitemap 
		WHERE loc NOT IN (
			SELECT url
			FROM martha_scrapes
		)
	'''
	conn = sqlite3.connect('recipe.db', check_same_thread=False)
	recipe_url_df = pd.read_sql(statement, conn)
	recipe_url_list = recipe_url_df['loc']
	conn.close()

	return recipe_url_list

# scrapes a recipe link and writes results to db
def scrape_martha_link(link):

	conn = sqlite3.connect('recipe.db', check_same_thread=False)
	scraper = scrape_me(link)
	scraped_link = f'{link}'
	scraped_title = scraper.title()
	scraped_ingredients = ''
	for ingredient in scraper.ingredients():
		scraped_ingredients += ingredient
		scraped_ingredients += '\n'
	scraped_instructions = scraper.instructions()
	scraped_image = scraper.image()
	martha_dict = {
		'url':[scraped_link],
		'title':[scraped_title],
		'ingredients':[scraped_ingredients],
		'instructions':[scraped_instructions],
		'image':[scraped_image]
	}
	scraped_df = pd.DataFrame.from_dict(martha_dict)
	scraped_df.to_sql(
		'martha_scrapes',
		con=conn,
		if_exists='append',
		index=False
	)
	conn.close()
	print(scraped_title)

# make markdown file from the db
def make_markdown_recipe(url):
	statement = f'''
		SELECT DISTINCT * 
		FROM martha_scrapes 
		WHERE url = '{url}'
	'''
	conn = sqlite3.connect('recipe.db', check_same_thread=False)
	markdown_df = pd.read_sql(statement, conn)
	md_image_string = f"![]({markdown_df.iloc[0]['image']})"
	md_title_string = f"#{markdown_df.iloc[0]['title']}"
	print(md_image_string)
	print(md_title_string)
	
	with open('test1.md', 'a') as markdown_recipe:
		markdown_recipe.write(md_title_string)		
		markdown_recipe.write(md_image_string)
		markdown_recipe.write('<br>')

# ------------------------------------- #
# EXECUTE FUNCTIONS
# ------------------------------------- #

# get recipe links
recipe_links = get_martha_recipe_url_list()

# scrap the links and upload results to db
# for recipe_link in recipe_links[:25]:
# 	scrape_martha_link(recipe_link)
# 	time.sleep(3)

make_markdown_recipe('https://www.marthastewart.com/256978/pecan-crusted-catfish-with-wilted-greens')


# ------------------------------------- #
# SCRAP
# ------------------------------------- #

# create_recipe_db()

# response = requests.get('https://www.marthastewart.com/sitemaps/recipe/1/sitemap.xml')
# df = pd.read_xml(response.text)
# recipe_url_list = list(df['loc'])
# print(df)
# for recipe in recipe_url_list[:10]:
# 	print(recipe)

# url = 'https://www.marthastewart.com/344334/chris-biancos-pizza-dough'
# scraper = scrape_me(url)
# print(' -------- ')
# print(scraper.title())
# print(' ')
# print(scraper.total_time())
# print(' ')
# # print(scraper.yields()) #TODO: FIX THIS
# print(scraper.ingredients()) 
# print(' ')
# print(scraper.instructions())  # or alternatively for results as a Python list: scraper.instructions_list()
# print(' ')
# print(scraper.image())
# print(scraper.host()) #marthastewart.com (not sure if we need this. can always be added in the db)

# scraper.links()
# scraper.nutrients()  # if available

