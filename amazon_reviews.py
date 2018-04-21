from bs4 import BeautifulSoup, Comment
import re, itertools, random
import urllib
import urllib.request
from datetime import datetime
from time import sleep
import csv
import requests



def review_pages(product_page):
    pagination_items = []
    review_urls = []


    site = "http://amazon.com"
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    #get product page request
    product_page = requests.get(product_page, headers = headers)

    #product page html
    product_soup = BeautifulSoup(product_page.text, "html.parser")


    #get the review link
    for all_review_url in product_soup.find_all("a", {"data-hook":"see-all-reviews-link"}):
        print (all_review_url.get("href"))
        top_page_url = site + all_review_url.get("href")  #LINK FOR ALL REVIEWS
        print (top_page_url)


    #this section gets all review URLS
    base_url = top_page_url.replace("ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews","")
    review_page_string = "ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=" #page number is missing!

    top_page = requests.get(top_page_url)

    top_soup = BeautifulSoup(top_page.text, "html.parser")

    page_nav = top_soup.find("div", {"class": "a-text-center celwidget a-text-base"}, {"id":"cm_cr-pagination_bar"})


    for lis in page_nav.find_all("li"):
        #print(lis)
        pagination_items.append(lis.get_text())

    #review urls
    review_urls.append(top_page_url) #first item in the list, top level review page

    if "," in pagination_items[6]: #get rid of commas in the number
        pagination_items[6] = pagination_items[6].replace(",","")
    print(("Number of review pages: " + str(pagination_items[6]))) #number of pages with reviews



    #create the rest of the review urls
    for i in range(2,int(pagination_items[6]) + 1):
        review_urls.append(base_url + review_page_string + str(i))

    return review_urls

#input the list of reviews!

def get_reviews(pageurl):
    #this function will make tuples of every review, and store all tuples in the review list
    reviews = []
    page_number = 1
    review_number = 0

    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    for url in pageurl:
        print("scraping page #"+str(page_number))
        url_page = requests.get(url, headers = headers)
        url_soup = BeautifulSoup(url_page.text, "html.parser")
        url_reviews = url_soup.find("div", {"class": "a-section a-spacing-none review-views celwidget"}, {"id":"cm_cr-review_list"}) #review div

        #print("type url_reviews: " + str(type(url_reviews)))

        page_reviews = []
        for review in url_reviews.find_all("div",{"class": "a-section review"}, {"data-hook":"review"}): #find all reviews on a page
            for review2 in review.find_all("div",{"class": "a-section celwidget"}): #each review
                review_elements = [] #list to hold a reviews data, with each item as an element (title, author, date, rating, text)
                print("scraping review #" + str(review_number))

                for review_title in review2.find_all("a", {"data-hook":"review-title"}, {"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"}):
                    #THIS SHOULD BE A REVIEWS TITLE
                    review_elements.append(str(review_title.get_text()))

                for review_author in review2.find_all("a", {"data-hook":"review-author"}, {"class":"a-size-base a-link-normal author"}):
                    #THIS SHOULD BE A REVIEWS AUTHOR
                    review_elements.append(str(review_author.get_text()))

                for review_date in review2.find_all("span", {"data-hook":"review-date"}, {"class":"a-size-base a-color-secondary review-date"}):
                    #THIS SHOULD BE A REVIEWS DATE
                    review_elements.append(str(review_date.get_text()))

                for review_rating in review2.find_all("i", {"data-hook":"review-star-rating"}, {"class":"a-icon a-icon-star a-star-5 review-rating"}):
                    for star_rating in review_rating.find("span", {"class":"a-icon-alt"}):
                        #THIS SHOULD BE A REVIEWS RATING
                        #just the first number of their review string, which is their rating
                        review_elements.append(str(star_rating)[0])

                for review_body in review2.find_all("span", {"data-hook":"review-body"}, {"class":"a-size-base review-text"}):
                    #THIS SHOULD BE A REVIEWS TEXT
                    review_elements.append(str(review_body.get_text()))

                review_number += 1
                reviews.append(tuple(review_elements))
        page_number += 1


    return reviews

def main():
    headers = ["title", "author", "date", "rating", "text"]

    print("What product do you want the reviews for?")
    review_url = input("Please paste the product page url. \n")

    print("The following reviews will be exported to a .csv file.")
    filename = input("What do you want to name file? \n")

    print("Thanks!")

    review_urls = review_pages(review_url)
    product_reviews = get_reviews(review_urls)

    #write csv files w/ reviews

    #create csv
    reviewcsv = open(str(filename)+".csv",'w')

    #write headers

    for i in range(len(headers)-1):
        reviewcsv.write(headers[i]+",")
    reviewcsv.write(headers[len(headers)-1]+"\n")

    for review in product_reviews:
        for i in range(len(review)-1):
            reviewcsv.write(review[i]+",")
        reviewcsv.write(review[len(review)-1]+"\n")

    reviewcsv.close()


if __name__ == '__main__':
    main()
