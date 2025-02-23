import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#The url is the main page of the profile you want to scrape

user_id = "9008848"
base_url = "https://www.filmaffinity.com/us/userratings.php?user_id=0000000&orderby=0&p=1&chv=list"
h = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

#Function to add the chosen user_id to the generic url

def update_user_id(base_url, new_user_id):
 
    updated_url = re.sub(r"(user_id=)\d{7}", rf"\g<1>{new_user_id}", base_url)
    return updated_url

url = update_user_id(base_url, user_id)

#The request is made, and the total page number is obtained

res = requests.get(url, headers = h, timeout = 10)
soup = BeautifulSoup(res.text, "html.parser")

page_number = int(soup.find_all("li", class_ = "page-item")[-2].text.strip())

#Function to change the url page number
def update_url(old_url, new_page_number):
	return re.sub(r'(p=)\d+', rf'\g<1>{new_page_number}', old_url)

#Function to get the data from the profile.
def get_films_data():
	film_list = []
	ratings_list = []
	date_list = []
	country_list = []
	for i in range(page_number):
		new_url = update_url(url, i+1)
		new_req = requests.get(new_url, headers = h, timeout = 10)
		soup = BeautifulSoup(new_req.text, "html.parser")
		films_in_page = soup.find_all("div", class_ = "fs-6 mc-title")
		ratings_in_page =  soup.find_all("div", class_ = "fa-user-rat-box")
		date_in_page =  soup.find_all("span", class_ = "mc-year")
		images_in_card_in_page = soup.find_all("div", class_ = "fa-card")
		
		for j in range(len(films_in_page)):
			film_list.append(films_in_page[j].find("a", class_="d-none d-md-inline-block").text.strip())
			ratings_list.append(ratings_in_page[j].text.strip())
			date_list.append(date_in_page[j].text.strip())
			country_list.append(images_in_card_in_page[j].find("img", class_ = "nflag").attrs["alt"])
		
		#All the imformation is stored in a dictionary
		dataset1 = {
			"Film" : film_list,
			"Rating" : ratings_list,
			"Date" : date_list,
			"Country" : country_list
		}
	return dataset1


dataset1 = get_films_data()

df1 = pd.DataFrame(dataset1)

#The dataset is exported to an Excel
df1.to_excel("Films_Test.xlsx", sheet_name= "Films")




    