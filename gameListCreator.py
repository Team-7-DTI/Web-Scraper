from bs4 import BeautifulSoup as BS
import requests


def getSoup(url):
    games = []
    r = requests.get(url)
    content = r.content
    soup = BS(content, "html.parser")

    games = getGameRow(soup)
    return games


def getGameRow(soup):
    games = []
    gameRows = soup.find_all('div', {'class': 'game-row'})
    # print("Getting game rows")
    for gameRow in gameRows:
        gameInfo = getGameInfo(gameRow)
        if gameInfo is not None:
            # print("Appending game info")
            games.append(gameInfo)
    return games


def getGameInfo(game):
    gameName = game.find('div', {'class': 'game-name'})
    href = gameName.find('a')
    if href is None:
        return None

    # print("Getting game info")
    gameUrl = "https://opencritic.com"+gameName.find('a')['href']+"/reviews"
    gameInfo = {'Name': gameName.text,
                'URL': gameUrl
                }
    # print(gameInfo)
    return gameInfo


def main(url):
    '''a function that returns a list of games with their name and url
    parameters:
    url: the url of the page from opencritic.com of the form
    'https://opencritic.com/browse/all/all-time/num-reviews'
    returns: a list of games each element of the list is a dictionary
    with the keys 'Name' and 'URL'
    '''
    games = []
    games = getSoup(url)
    print("Returning games")
    return games


if __name__ == "__main__":
    url = "https://opencritic.com/browse/all/all-time/num-reviews"
    soup = getSoup(url)
