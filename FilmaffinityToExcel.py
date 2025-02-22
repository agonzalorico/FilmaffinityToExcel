import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.filmaffinity.com/us/userratings.php?user_id=9855289&orderby=0&p=1&chv=list"
h = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

res = requests.get(url, headers = h, timeout = 10)
soup = BeautifulSoup(res.text, "html.parser")

page_number = int(soup.find_all("li", class_ = "page-item")[-2].text.strip())
def update_url(old_url, new_page_number):
	return re.sub(r'(p=)\d+', rf'\g<1>{new_page_number}', old_url)

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

		dataset1 = {
			"Film" : film_list,
			"Rating" : ratings_list,
			"Date" : date_list,
			"Country" : country_list
		}
	return dataset1

dataset1 = get_films_data()

df1 = pd.DataFrame(dataset1)
df1.to_excel("Films_Test.xlsx", sheet_name= "Films")




    