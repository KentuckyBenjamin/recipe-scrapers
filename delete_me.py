from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://www.marthastewart.com/344334/chris-biancos-pizza-dough')

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
# scraper = scrape_me('https://www.feastingathome.com/tomato-risotto/', wild_mode=True)

print(' -------- ')
print(scraper.title())
print(' ')
print(scraper.total_time())
print(' ')
# print(scraper.yields())
print(scraper.ingredients())
print(' ')
print(scraper.instructions())  # or alternatively for results as a Python list: scraper.instructions_list()
print(' ')
print(scraper.image())
# scraper.host()
# scraper.links()
# scraper.nutrients()  # if available

# Starting from version 14.0.0 you also have an option to scrape from html-like content
# import requests
# from recipe_scrapers import scrape_html

# url = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
# html = requests.get(url).content

# scraper = scrape_html(html=html, org_url=url)

# scraper.title()
# scraper.total_time()
# etc...