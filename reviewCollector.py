'''This module is used to collect reviews from opencritic.com
It takes the url of the game as input and returns a list of reviews
call the main function to achieve functionality'''

import requests
from bs4 import BeautifulSoup as BS

reviewList = []

# a function that goes through the pages and makes the soup


def get_soup(url):
    '''This function goes through the pages and makes the soup
    takes the url as input(url should be from opencritic.com
    of the form 'https://opencritic.com/game/1234/game_name/reviews')
    '''
    # get the html content of the page
    r = requests.get(url)
    content = r.content
    # parse the html content
    soup = BS(content, "html.parser")

    # pass the soup to get_review_text function
    get_review_row(soup)

    if len(reviewList) < 30:
        # find the next page button
        next_page_url = ""
        buttons = soup.find_all('a', {'class': 'btn-sm'})
        for button in buttons:
            if button.text == "Next ":
                next_page_url = "https://opencritic.com/" + button['href']
                break
        get_soup(next_page_url)
    else:
        return

# a function that gets the review text


def get_review_row(soup):
    ''' This function finds all the reviews rows in the page and
    passes them to get_review_info function
    takes the soup as parameter and returns nothing
    '''
    print("in get_review_row function of reviewCollector.py")
    reviews_row = soup.find_all('div', {'class': 'review-row'})
    for review in reviews_row:
        if len(reviewList) < 30:
            get_review_info(review)
        else:
            break
    return


def get_review_info(review):
    ''' This function finds the author name, outlet name and the external url
    takes the review as parameter and returns nothing
    '''
    print("in get_review_info function of reviewCollector.py")
    author_name_div = review.find('app-author-list', {'class': 'author-name'})
    # if author_name_div is not None find the text
    if author_name_div is not None:
        author_name = author_name_div.find('a').text
    else:
        return

    outlet_name_div = review.find('span', {'class': 'outlet-name'})
    # if outlet_name_div is not None find the text
    if outlet_name_div is not None:
        outlet_name = outlet_name_div.find('a').text
    else:
        return

    # find all p tags with class "mb-0" and check whether the text is "Read full review", if yes, then get the href
    read_full_review = review.find_all('p', {'class': 'mb-0'})
    external_url = None
    for p in read_full_review:
        if p.text == "Read full review":
            read_full_review_href = p.find('a')['href']
            external_url = read_full_review_href
            print("got a usable external url")
            break
    if external_url is None:
        print("No usable external URL found")
        return
    # print(author_name, outlet_name, external_url, sep=" | ")

    # check the connection status of the url
    if checkConnection(external_url):
        # print("Connection Succesful, appending list")
        reviewList.append([author_name, outlet_name, external_url])
    else:
        # print("Connection Failed, Trying another URL")


def checkConnection(url):
    '''This function checks the connection status of the url
    if the connection is successful, it returns True
    else it returns False'''
    print("Checking connection status of", url)
    try:
        r = requests.get(url)
        if r.status_code >= 200 and r.status_code < 400:
            return True
        else:
            return False
    except:
        return False


def main(url):
    '''This function is the main function that calls all the other functions
    takes the url as input(url should be from opencritic.com
    of the form 'https://opencritic.com/game/1234/game_name/reviews')
    and returns the list of reviews.
    each item in the list is a list of the form [author_name, outlet_name, external_url]'''
    get_soup(url)
    print("Collected reviews")
    return reviewList


if __name__ == "__main__":
    url = "https://opencritic.com/game/8525/cyberpunk-2077/reviews"
    print("Running reviewCollector.py")
    reviewList = main(url)
    i = 1
    for review in reviewList:
        print(i, review)
        i += 1
    print("Done")
