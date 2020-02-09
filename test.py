# Module for tweet sentiment alanysis
# Objective is to determine which timezone is the "happiest"

# Import punctuation values for use in tweetHappiness function
from string import punctuation


# Minimun and maximum latitude and longitude values for timezones in the US
ALL_LAT_MIN = 24.660845
ALL_LAT_MAX = 49.189787
PACIFIC_LONG_MIN = -125.242264
PACIFIC_LONG_MAX = -115.236428
MOUNTAIN_LONG_MIN = -115.236428
MOUNTAIN_LONG_MAX = -101.998892
CENTRAL_LONG_MIN = -101.998892
CENTRAL_LONG_MAX = -87.518395
EASTERN_LONG_MIN = -87.518395
EASTERN_LONG_MAX = -67.444574


###
def compute_tweets(tweetFile, keywordFile):
    done = False
    while not done:
        try:
            tweetData = readFile(tweetFile)
            keywordData = readFile(keywordFile)
            # process data
            keywordDict = keywordExtraction(keywordData)
            coordinates = coordinateExtraction(tweetData)
            tweetList = tweetExtraction(tweetData)
            tweetScores = tweetHappiness(tweetList, keywordDict)
            easternHappiness = timezoneHappiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, EASTERN_LONG_MIN, EASTERN_LONG_MAX, tweetScores)
            centralHappiness = timezoneHappiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, CENTRAL_LONG_MIN, CENTRAL_LONG_MAX, tweetScores)
            mountainHappiness = timezoneHappiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, MOUNTAIN_LONG_MIN, MOUNTAIN_LONG_MAX, tweetScores)
            pacificHappiness = timezoneHappiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, PACIFIC_LONG_MIN, PACIFIC_LONG_MAX, tweetScores)

            print(keywordDict)
            print(coordinates)
            print(tweetList)
            print(tweetScores)
            print(easternHappiness)
            print(centralHappiness)
            print(mountainHappiness)
            print(pacificHappiness)
            done = True
        except IOError:
            print("Error: file not found.")
            return
        except ValueError:
            print("Error: file contents invalid.")
        except RuntimeError as error:
            print("Error:", str(error))


## Opens a file and reads a data set.
#  @param filename the name of the file holding the data
#  @return a list containing the data in the file
#
def readFile(filename):
    inFile = open(filename, "r", encoding="utf-8")
    try:
        return readData(inFile)
    finally:
        inFile.close()


## Reads a data set.
#  @param inFile the input file containing the data
#  @return the data set in a list
#
def readData(inFile):
    data = []
    for line in inFile:
        line = line.strip()
        # May raise a ValueError exception.
        data.append(line)
    return data


# Create a list of keywords and a list of their corresponding sentiment values
def keywordExtraction(keywordData):
    keywordDict = {}
    for line in keywordData:
        keywords = line.strip().split(",")
        keyword = keywords[0]
        sentimentValue = int(keywords[1])
        keywordDict[keyword] = sentimentValue
    return keywordDict


def coordinateExtraction(tweetData):
    coordinateList = []
    for line in tweetData:
        coordinates = []
        coordinateValues = line.split(" ", 2)
        latitude = coordinateValues[0].strip("[,")
        longitude = coordinateValues[1].strip("],")
        coordinates.append(latitude)
        coordinates.append(longitude)
        coordinateList.append(coordinates)
    return coordinateList


def tweetExtraction(tweetData):
    tweetList = []
    for line in tweetData:
        tweetValues = line.split(" ", 5)
        tweet = tweetValues[5].strip()
        tweetList.append(tweet)
    return tweetList


# Compute sentiment analysis for all tweets
def tweetHappiness(tweetString, keywordDict):
    tweetScores = []
    for tweet in tweetString:
        happinessScore = 0
        count = 0
        tweet = tweet.split()
        for words in tweet:
            word = words.strip(punctuation).lower()
            if word in keywordDict:
                wordSentiment = keywordDict[word]
                happinessScore = happinessScore + wordSentiment
                count = count + 1
        if count > 0:
            happinessScore = happinessScore/count
            tweetScores.append(happinessScore)
        if count == 0:
            tweetScores.append("None")
    return tweetScores


#TimeZones are Easter, Central, Mountain, Pacific)
def timezoneHappiness(coordinates, latMin, latMax, longMin, longMax, tweetScores):
    count = 0
    tweetHappinessTotal = 0
    timezoneTupple = ()
    for i in range(0,len(coordinates)):
        coordinate = coordinates[i]
        if float(coordinate[0])<=latMax and float(coordinate[0])>=latMin and float(coordinate[1])<=longMax and float(coordinate[1])>=longMin:
            tweetScore = tweetScores[i]
            if tweetScore != "None":
                tweetHappinessTotal = tweetHappinessTotal + tweetScore
                count = count + 1
    if count > 0:
        timezoneCount = count
        timezoneHappiness = tweetHappinessTotal/timezoneCount
        timezoneTupple = (timezoneHappiness, timezoneCount)
    elif count == 0:
        timezoneCount = count
        timezoneTupple = ("None", timezoneCount)
    return(timezoneTupple)

compute_tweets("tweets.txt", "keywords.txt")
