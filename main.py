import requests
from bs4 import BeautifulSoup as BS

# a function that goes through the pages and makes the soup


def get_soup(url):
    # get the html content of the page
    r = requests.get(url)
    content = r.content
    # parse the html content
    soup = BS(content, "html.parser")

    # find the next page button
    # next_page_url = "https://opencritic.com/"
    # buttons = soup.find_all('a', {'class': 'btn-sm'})
    # for button in buttons:
    #     if button.text == "Next":
    #         next_page_url += button['href']
    #         break

    # pass the soup to get_review_text function
    get_review_row(soup)

    # writing to a file
    # with open("output.html", "w") as file:
    #     file.write(soup.prettify())

# a function that gets the review text


def get_review_row(soup):
    reviews_row = soup.find_all('div', {'class': 'review-row'})
    for review in reviews_row:
        get_review_info(review)

        # write to a new file
        # with open("reviews.txt", "w") as file:
        #     for review in reviews:
        #         file.write(review.prettify())


def get_review_info(review):
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
            # print(read_full_review_href)
            break
    if external_url is None:
        return
    print(author_name, outlet_name, external_url, sep=" | ")


if __name__ == "__main__":
    urlList = ["https://opencritic.com/game/8525/cyberpunk-2077/reviews"]
    for url in urlList:
        get_soup(url)
