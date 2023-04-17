import reviewCollector
import csvCreator
import gameListCreator

if __name__ == "__main__":
    url = "https://opencritic.com/browse/all/all-time/num-reviews"
    games = []
    for i in range(1, 4):
        if i == 1:
            url = "https://opencritic.com/browse/all/all-time/num-reviews"
        else:
            url = "https://opencritic.com/browse/all/all-time/num-reviews?page=" + \
                str(i)
        temp = gameListCreator.main(url)
        games.extend(temp)

    count = 0

    for obj in games:
        print(games)
        gameName = obj['Name']
        url = obj['url']
        print("Getting reviews for", gameName)
        reviewList = reviewCollector.main(url)
        csvCreator.main(gameName, reviewList)
