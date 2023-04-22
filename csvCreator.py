''' a module that creates a csv file with the review data
call the main function to achieve functionality
'''
from bs4 import BeautifulSoup as BS
import requests
from csv import writer


def get_soup(url):
    ''' a function that goes through the pages and makes the soup
    parameters:
    url: the url of the page
    returns: the text buffer
    '''
    # print("in get_soup function of csvCreator.py")
    # get the html content of the page
    r = requests.get(url)
    content = r.content
    # parse the html content
    soup = BS(content, "html.parser")

    # pass the soup to get_review_text function
    textBuffer = get_review_text(soup)
    return textBuffer


def get_review_text(soup):
    ''' a function that gets the review text
    parameters:
    soup: the soup of the page
    returns: the text buffer
    '''
    # print("in get_review_text function of csvCreator.py")
    textBuffer = ""
    reviews = soup.find_all('p')
    for review in reviews:
        text = review.text
        textBuffer += text
    return textBuffer


def fileCreator(gameName, reviewList):
    ''' a function that creates a csv file with the review data
    parameters:
    fileName: the name of the file
    textBuffer: the text buffer
    '''
    # print("in fileCreator function of csvCreator.py")

    fileName = gameName + ".csv"
    with open("gameReviews/" + fileName, "w", encoding='utf-8-sig', newline='') as file:
        header = ["Game", "Author", "Outlet", "URL", "Review"]
        csv_writer = writer(file)
        csv_writer.writerow(header)
        for review in reviewList:
            textBuffer = get_soup(review[2])
            csv_writer.writerow(
                [gameName, review[0], review[1], review[2], textBuffer])
            print([gameName, review[0], review[1], review[2]])
    return


def main(gameName, reviewList):
    ''' a function that creates a csv file with the review data
    parameters:
    gameName: the name of the game
    reviewList: a list of reviews
    returns: nothing
    '''
    print("in main function of csvCreator.py")
    fileCreator(gameName, reviewList)
    return


if __name__ == "__main__":
    gameName = "cyberpunk-2077"
    url = "https://www.eurogamer.net/articles/2020-12-10-cyberpunk-2077-review-intoxicating-potential-half-undermined-half-met"
    print("running csvCreator.py for " + gameName + " and url " + url)
    reviewList = [["Author", "Outlet", url]]
    main(gameName, reviewList)
    print("csv file created")
