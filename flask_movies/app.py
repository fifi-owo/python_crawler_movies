# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:16:58 2023

@author: user
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from flask import Flask, render_template, request
from gevent import pywsgi
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

@app.route('/',  methods=['GET', 'POST'])

def home():
    #return render_template('test.html', mLen = mLen,  moviesList = moviesList)
    if request.method == 'POST':
        if request.form.get('action1') == '本周新上映':
            #return "Hello, World!"
            return render_template('test.html', mLen = mLen, moviesList = moviesList, mLen1 = 0, imdbList = imdbList)
        elif  request.form.get('action2') == 'IMDB前25名':
            #return "Hello, World!"
            return render_template('test.html', mLen = 0, moviesList = moviesList, mLen1 = 25, imdbList = imdbList)
        else:
            pass
    return render_template('test.html', mLen = 0,  moviesList = moviesList, mLen1 = 0, imdbList = imdbList)

def fetch_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    movies = soup.find_all("article", class_="filmList")
    sheet = []
    for movie in movies:
        name = movie.find("div", class_="filmTitle")
        #print(name.a)
        time = movie.find("div", class_="runtime")
        long = time.text.split()[0]
        date = time.text.split()[1]
        cinema = time.text.split()[2]+"："+time.text.split()[3][1:-1]
        #print(cinema)
        link_tag = movie.find("a")['href']
        link = "http://www.atmovies.com.tw/" + link_tag if link_tag else "N/A"
        #print(link)
        intro = movie.find("p")
        sheet.append([name.text.strip(), long, date , cinema, intro.text.strip(), link])
    return sheet

url = "http://www.atmovies.com.tw/movie/new/"
fetch_data(url)
mLen = len(fetch_data(url))
moviesList = fetch_data(url)

def fetch_imdb(url):
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    movies1 = soup.find_all("li", class_="ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent", limit=25)
    #print(movies1[0])

    imdbList = []
    for movie1 in movies1:
        name1_tag = movie1.find("h3", class_="ipc-title__text")
        name1 = name1_tag.text.strip()[3:] if name1_tag else "N/A"

        # 獲取包含年份、時長和其他元素的所有 span
        metadata_div = movie1.find("div", class_="sc-43986a27-7 dBkaPT cli-title-metadata")
        #獲取評分
        metadata_div1 = movie1.find("div", class_="sc-e3e7b191-0 jlKVfJ sc-43986a27-2 bvCMEK cli-ratings-container")

        metadata_spans = metadata_div.find_all("span", class_="sc-43986a27-8 jHYIIK cli-title-metadata-item")
        #在抓分數
        metadata_spans1 = metadata_div1.find_all("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")

        # 根據內容進行篩選
        year = next((span.text.strip() for span in metadata_spans if span.text.strip().isdigit()), "N/A")
        time1 = next((span.text.strip() for span in metadata_spans if 'h' in span.text.strip()), "N/A")
        rate = next((span.text.strip().split("\xa0")[0] for span in metadata_spans1), "N/A")

        link1_tag = movie1.find("a")
        link1 = "https://www.imdb.com" + link1_tag['href'] if link1_tag else "N/A"

        imdbList.append([rate, name1, year, time1, link1])
    return imdbList


    driver.quit()

# IMDb網站的URL
imdb_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
imdbList = fetch_imdb(imdb_url)

