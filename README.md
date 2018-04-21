# Amazon Review Scraper

#### haven't you always wanted to get reviews from amazon easily? now you can! 
#### this script will export reviews into a CSV file. it'll scrape the title, rating, date, author, and text of each review.


##### Set Up

all you need to start is the URL of the first page of reviews. Make sure the end of the URL says reviewerType=all_reviews

example - https://www.amazon.com/Alienware-Gaming-Mechanical-Keyboard-AW768/product-reviews/B072NHMYXX/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews


##### Running the Script
- Open terminal
- use cd to find the directory the script in is
- type "python3 amazon_scraper.py" to run


##### THINGS TO FIX
- sometimes crashes with items with a ton of pages
- sometimes the find_all won't work because Nonetype is returned
-let the user input the URL of the product page!
