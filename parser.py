# -*- coding: utf-8 -*-

from datetime import date, timedelta
import requests, os, codecs
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
        
def save_soup():
    file = open("./" + str(current_date) +
                "/" + str(current_date) + ".html", "w")
    file.write(str(make_request()))
    file.close()
    del file
    
def get_soup():
    soup = BeautifulSoup(make_request(), "html.parser")

    soup_file = codecs.open("./" + str(current_date) + "/" + str(current_date) + ".html", "w", encoding="utf-8")
    soup_file.write(str(soup))
    soup_file.close()
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
        file = codecs.open("general.txt", "a", encoding='utf-8')
        file.write(
            title + "|||" +
            post_url + "|||" +
            post_image + "|||" +
            author.text + "|||" +
            author_url + "|||" +
            category.text + "|||" +
            category_url + "|||" +
            description + "\n"
            )
        
        all_posts_url = codecs.open("all_posts_urls.txt", "a", encoding='utf-8')
        all_posts_url.write(post_url + "\n")
        all_posts_url.close()
        
        
        del title, post_url, post_image, author, author_url, category, category_url, description, all_posts_url
    file.close()
    
    del soup, file
    get_soup()
    
def go():
    get_soup()


#Go
go()
