import pandas as pd
import matplotlib.pyplot as plt

import scraper

calorie_list = []
name_list = []
bluePoint_list = []
greenPoint_list = []
purplePoint_list = []
recipeKey_list = []

data = scraper.get_data()
for recipe in data:
	calorie_list.append(recipe.calorie)
	name_list.append(recipe.name)
	bluePoint_list.append(recipe.bluePoint)
	greenPoint_list.append(recipe.greenPoint)
	purplePoint_list.append(recipe.purplePoint)

	for recipeKey in recipe.recipeKeys:
		recipeKey_list.append(recipeKey)

df = pd.DataFrame(list(zip(name_list,calorie_list,bluePoint_list,greenPoint_list,purplePoint_list,recipeKey_list)), columns =["Name","calories","bluePoint","greenPoint","purplePoint","recipeKeys"])

	# Plotting a calorie frequency graph
df["calories"].hist(bins = 50, color = "orange")
plt.title("Distribution of calorie amounts")
plt.xlabel("Calories")
plt.ylabel("# of recipes")
plt.show()
	# Plotting bluepoint frequency..
df["bluePoint"].hist(bins = 20, color = "blue")
plt.title("Distribution of Blue points")
plt.xlabel("Blue points")
plt.ylabel("# of recipes")
plt.show()
	# Plotting greenpoint frequency..
df["greenPoint"].hist(bins = 20, color = "green")
plt.title("Distribution of Green points")
plt.xlabel("Green points")
plt.ylabel("# of recipes")
plt.show()
	# Plotting purplepoint frequency..
df["purplePoint"].hist(bins = 20, color = "purple")
plt.title("Distribution of Purple points")
plt.xlabel("Purple points")
plt.ylabel("# of recipes")
plt.show()

df["recipeKeys"].value_counts().plot(kind = "barh")
plt.title("Distribution of recipe keys")
plt.xlabel("# of recipes")
plt.show()