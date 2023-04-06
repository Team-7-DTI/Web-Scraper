import reviewCollector
import csvCreator

if __name__ == "__main__":
    gameName = "Cyberpunk-2077"
    url = "https://opencritic.com/game/8525/cyberpunk-2077/reviews"
    reviewList = reviewCollector.main(url)
