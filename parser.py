# -*- coding: utf-8 -*-

from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

date_end = "2016/09/15"
date_start = date(2015,11,12) #-1

def get_date():
    global current_date, date_start

    date_start += timedelta(days=1)

    current_date = date_start
    return current_date

def get_url():
    #https://drinkingculture.world/2018/05/08/
    date = get_date()
    
    url = "https://drinkingculture.world/" + date.strftime("%Y/%m/%d") + "/"
    print (url)
    return url

def make_request():
    request = requests.get(get_url())
    
    print (request)
    if request.status_code == 404:
        del request
        print ("no page - 404\n___________\nNEW Itteration")
        go()
    else:
        return request.content

def get_soup():
    soup = BeautifulSoup(make_request(), "html.parser")
    for article in soup.find_all('article'):
        
        title = article.h3.text
        post_url = article.h3.a['href']
        post_image = article.find("img", {"class":"wp-post-image"})['src']
        author = article.find("span", {"class":"fn"}).text
        category = article.find("a", {"rel":"category"}).text
        description = article.p.text
        
        print (
            title, "\n",
            post_url, "\n",
            post_image, "\n",
            author, "\n",
            category, "\n",
            description, "\n"
            )
    get_soup()
    
def go():
    get_soup()


#Go
go()
