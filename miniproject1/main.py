import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen, Request
from io import BytesIO
import scraper


def startScraping():
    scraper.scrape()
    status.config(text = "Done!", fg="green")
    startScrapingButton.config(state = "disabled")
    searchButton.config(state = "normal")

def query_recipes(entry):
    minmax = entry.split()
    count = 1
    if(minmax[1] > minmax[0]):
        recipes = scraper.get_list(int(minmax[0]), int(minmax[1]))

        for i in recipes:
            URL = Request(i.img_url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                u = urlopen(URL)
            except(UnicodeEncodeError):
                continue
            raw_data = u.read()
            u.close()

            im = Image.open(BytesIO(raw_data))
            im = im.resize((120, 120), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(im)

            label = tk.Label(image = photo)
            label.image = photo

            name = tk.Label(text = "{0} \n {1} calories\n {2}".format(i.name, i.calorie, i.summary),width = 60, font=("Courier", 8))


            name.grid(row = count+8, column = 2, sticky=tk.N+tk.E)
            label.grid(row = count+8, column = 1, sticky=tk.W)
            count = count + 1
    else:
        print("The max value cannot be smaller than the min value!")
    




root = tk.Tk()
root.geometry("")
root.resizable(False, False)
root.title("skinnytaste.com webscraper")


# --- creating widgets ---
startScrapingButton = tk.Button(text="Scrape!", command=lambda : startScraping())
status = tk.Label(root, text="No data, please scrape!", fg ="red")
info = tk.Label(root, text ="Please start with an initial scrape of the first 30 pages of skinnytaste.com")
note = tk.Label(root, text="NOTE! This may take up to 2 minutes")

calorieEntry = tk.Entry(root, text = "Calories")
searchButton = tk.Button(text="Search", state ="disabled", command=lambda : query_recipes(calorieEntry.get()))
tk.Label(root, text ="After scraping, please provide min and max calories.").grid(row= 4, column = 2)
tk.Label(root, text ="For example if you wish to see the range from 100 to 200 calories").grid(row= 5, column = 2)
tk.Label(root, text ="you would input '100 200'").grid(row= 6, column = 2)


# --- packing widgets ---
startScrapingButton.grid(row = 2, column = 2)
status.grid(row = 3, column = 2)
info.grid(row = 0, column = 2)
note.grid(row = 1, column = 2)
calorieEntry.grid(row = 7, column = 2)
searchButton.grid(row = 8, column = 2)

root.mainloop()