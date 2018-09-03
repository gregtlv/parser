# -*- coding: utf-8 -*-

from datetime import date, timedelta
import requests, os
from bs4 import BeautifulSoup

date_end = "2016/09/15"
date_start = date(2015,12,13) #-1

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
    try:
        request = requests.get(get_url())
    except:
        print ("make_request error")
        go()
    
    print (request)
    
    if request.status_code == 404:
        del request
        print ("no page - 404\n___________\nNEW Itteration")
        go()
    else:
        os.makedirs(str(current_date))
        
        request.connection.close()
        return request.content
        del request

def get_soup():
    soup_fle_name = current_date + ".html"
    soup_file = open("./", soup_fle_name)
    soup = BeautifulSoup(make_request(), "html.parser")
    
    for article in soup.find_all('article'):
        
        try:
            title = article.h3.text
        except:
            title = "Post haven't a title"
        try:    
            post_url = article.h3.a['href']
        except:
            post_url = "None Url"
        
        try:
            post_image = article.find("img", {"class":"wp-post-image"})['src']
        except:
            post_image = "Post without image"
            print (post_image)
            
        try:
            author = article.find("span", {"class":"fn"})
        except:
            author = "None Author"

        try:
            author_url = author.a['href']
        except:
            author_url = "None Author URL"
            
        try:
            category = article.find("a", {"rel":"category"})
        except:
            category = "None Category"

        try:
            category_url = category['href']
        except:
            category_url = "None Category URL"
            
        try:
            description = article.p.text
        except:
            description = "Post without desciption"
            print (description)
            
        print (
            title, "\n",
            post_url, "\n",
            post_image, "\n",
            author.text, "\n",
            author_url, "\n",
            category.text, "\n",
            category_url, "\n",
            description, "\n"
            )
            
        del title, post_url, post_image, author, author_url, category, category_url, description

    del soup
    get_soup()
    
def go():
    get_soup()


#Go
go()
