from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import random as r

Foods = []	# This array will store all our Food objects

# This is our Food class, we will use this to store all the required data from
# a recipe as its own object.
class Food:
	def __init__(self, name, calorie, summary, img_url, bluePoint, greenPoint, purplePoint, recipeKeys):

		self.name = name
		self.calorie = calorie
		self.summary = summary
		self.img_url = img_url
		self.bluePoint = bluePoint
		self.greenPoint = greenPoint
		self.purplePoint = purplePoint
		self.recipeKeys = recipeKeys

def slice_summary(summary):	#slice_summary is used to slice the summaries into
	whitespaceCount = 0		# a more readable form with multiple lines.
	i = 0
	for char in summary:
		
		if(char == " "):
			whitespaceCount = whitespaceCount + 1
		if(whitespaceCount == 7):
			summary = summary[:i] + "\n" + summary[i:]
			whitespaceCount = 0
			i = i + 1
		
		i = i + 1

	return summary


def parseData(url):
	client = urlopen(url)
	html = client.read()
	client.close
	page_soup = soup(html, "html.parser")

	posts = []
	# Getting all posts from site
	posts.extend(page_soup.findAll("article",{"class":"post teaser-post even"}))
	posts.extend(page_soup.findAll("article",{"class":"post teaser-post odd"}))

	# Creating a Food object out of every post
	for post in posts:
		# Getting the name of the recipe
		name = post.find("h2",{"class":"title"}).get_text()

		# Getting the calorie amount for the recipe, if we fail then that means
		# that the post in question is not a recipe, so we just skip it
		# and move on. This way we get rid of posts like
		# "7 DAY HEALTHY MEAL PLAN (NOV 16-22)" that are not recipes
		try:
			calorie = float(post.find("span",{"class":"icon-star"}).get_text())
			calorie = int(round(calorie))
		except(AttributeError):
			continue

		# Getting the summary for the recipe
		summary = post.find("p",{"class":"excerpt"}).get_text()
		summary = slice_summary(summary)

		# Getting the image for the recipe
		# Notice how we only get the url for later use 
		# and wont download the image right away.
		image = post.find("img")
		img_url = (image["src"])

		# Getting the blue, green and purple point values, if there are none
		# assign -1.
		try:
			greenPoint = int(post.find("span",{"class":"smart-points green"}).get_text())
			bluePoint = int(post.find("span",{"class":"smart-points blue"}).get_text())
			purplePoint = int(post.find("span",{"class":"smart-points purple"}).get_text())

		except(AttributeError):
			greenPoint = -1
			bluePoint = -1
			purplePoint = -1

		# Getting the recipekeys for each recipe
		tmp = []
		icons = post.find("div",{"class":"post-meta"})
		recipeKey = icons.findAll("img")

		for i in recipeKey:
			tmp.append(i["alt"])

		# Casting the list as a dictionary to remove duplicate recipekeys
		recipeKeys = list(dict.fromkeys(tmp))


		Foods.append(Food(name, calorie, summary, img_url, bluePoint, greenPoint, purplePoint, recipeKeys))


def scrape():
		# Scraping the first 30 pages
	for i in range(1,31):
		print("{0}/30  pages scraped".format(i))
		# Utilizing a user-agent so that our requests will go through
		url = Request("https://skinnytaste.com/page/{0}".format(i), headers={'User-Agent': 'Mozilla/5.0'})
		parseData(url)
	print("Done!")


def get_list(minimum,maximum):
	arr = []
	for i in Foods:
		if(i.calorie >= minimum and i.calorie <= maximum):
			arr.append(i)
		if(len(arr) == 5):
			return arr
	return arr

def get_data():
	scrape()
	return Foods