# Module to analyze tweet sentiment for all tweets in a given file
# Determines which timezone is the "happiest"

# Import punctuation values for use in tweet_happiness function
from string import punctuation


# Min and max latitude and longitude values defined for timezones in the US (Eastern, Central, Mountain, Pacific)
ALL_LAT_MIN = 24.660845
ALL_LAT_MAX = 49.189787
EASTERN_LONG_MIN = -87.518395
EASTERN_LONG_MAX = -67.444574
CENTRAL_LONG_MIN = -101.998892
CENTRAL_LONG_MAX = -87.518395
MOUNTAIN_LONG_MIN = -115.236428
MOUNTAIN_LONG_MAX = -101.998892
PACIFIC_LONG_MIN = -125.242264
PACIFIC_LONG_MAX = -115.236428


# Compute timezone happiness for eastern, central, mountain and pacific time zones in the US
# @param tweetFile the input file containing the tweet data
# @param keywordFile the input file containing the kewword data
# @return allTimezoneHappiness a list containing happiness results for each timezone as tuples (average happiness, tweet count)
#
def compute_tweets(tweetFile, keywordFile):
    done = False
    allTimezoneHappiness = []
    while not done:
        try:
            tweetData = read_file(tweetFile)
            keywordData = read_file(keywordFile)
            # Process data
            keywordDict = keyword_extraction(keywordData)            # Create a dictionary of all keywords and their happiness values (Key = keyword & Value = happiness value)
            coordinates = coordinate_extraction(tweetData)           # Create a list of all coordinates
            tweetList = tweet_extraction(tweetData)                  # Create a list of all tweets
            tweetScores = tweet_happiness(tweetList, keywordDict)    # Create a list of all tweet happiness scores
            # Compute the tuple (average happiness, tweet count) for each of the four timezones
            easternHappiness = timezone_happiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, EASTERN_LONG_MIN, EASTERN_LONG_MAX, tweetScores)
            centralHappiness = timezone_happiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, CENTRAL_LONG_MIN, CENTRAL_LONG_MAX, tweetScores)
            mountainHappiness = timezone_happiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, MOUNTAIN_LONG_MIN, MOUNTAIN_LONG_MAX, tweetScores)
            pacificHappiness = timezone_happiness(coordinates, ALL_LAT_MIN, ALL_LAT_MAX, PACIFIC_LONG_MIN, PACIFIC_LONG_MAX, tweetScores)
            # Add each tuple (average happiness, tweet count) to the list allTimeZoneHappiness
            allTimezoneHappiness.append(easternHappiness)
            allTimezoneHappiness.append(centralHappiness)
            allTimezoneHappiness.append(mountainHappiness)
            allTimezoneHappiness.append(pacificHappiness)
            done = True
        except IOError:
            print("Error: file not found.")
            return allTimezoneHappiness
        except ValueError:
            print("Error: file contents invalid.")
        except RuntimeError as error:
            print("Error:", str(error))
    return allTimezoneHappiness


# Opens a file and reads a data set
# @param filename the name of the file holding the data
# @return a list containing the data in the file
#
def read_file(filename):
    inFile = open(filename, "r", encoding="utf-8")
    try:
        return read_data(inFile)
    finally:
        inFile.close()


# Reads a data set
# @param inFile the input file containing the data
# @return the data set in a list
#
def read_data(inFile):
    data = []
    for line in inFile:
        if line != "\n":
            line = line.strip()
            # May raise a ValueError exception.
            data.append(line)
    return data


# Create a dictionary of keywords and their happiness value
# @param keywordData the list of all data in the keywordFile
# @return keywordDict the dictionary of all keywords and their happiness values (Key = keyword & Value = happiness value)
#
def keyword_extraction(keywordData):
    keywordDict = {}
    for line in keywordData:
        keywords = line.strip().split(",")
        keyword = keywords[0]
        sentimentValue = int(keywords[1])
        keywordDict[keyword] = sentimentValue
    return keywordDict


# Create a list of all coordinates
# @param tweetData the list of all data in the tweetFile
# @return coordinateList the list of all coordinates
#
def coordinate_extraction(tweetData):
    coordinateList = []
    for line in tweetData:
        coordinates = []
        coordinateValues = line.split(" ", 2)
        latitude = float(coordinateValues[0].strip("[,"))
        longitude = float(coordinateValues[1].strip("],"))
        coordinates.append(latitude)
        coordinates.append(longitude)
        coordinateList.append(coordinates)
    return coordinateList


# Create a list of all tweets
# @param tweetData the list of all data in the tweetFile
# @return tweetList the list of all tweets
#
def tweet_extraction(tweetData):
    tweetList = []
    for line in tweetData:
        tweetValues = line.split(" ", 5)
        tweet = tweetValues[5].strip()
        tweetList.append(tweet)
    return tweetList


# Compute happiness score for all tweets
# @param tweetList the list of all tweets
# @param keywordDict the dictionary of all keywords and their happiness values (Key = keyword & Value = happiness value)
# @return tweetScores the list of all tweet happiness scores
#
def tweet_happiness(tweetList, keywordDict):
    tweetScores = []
    for tweet in tweetList:
        happinessScore = 0
        count = 0
        tweet = tweet.split()       # Separate tweet into words based on white space
        for words in tweet:
            word = words.strip(punctuation).lower()     # Remove any punctuation from the beginning or end of the word and covert word to lower case
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


# Compute happiness score for a timezone. Uses the assumption that for a timezone boundary min values are inclusive, but max values are not inclusive
# @param coordinates the list of all coordinates
# @param latMin the minimum latitude value for the timezone (inclusive i.e. boundary value is considered part of timezone)
# @param latMax the maximum latitude value for the timezone (not inclusive i.e. boundary value is not considered part of timezone)
# @param longMin the minimum longitude value for the timezone (inclusive i.e. boundary value is considered part of timezone)
# @param longMax the maximum longitude value for the timezone (not inclusive i.e. boundary value is not considered part of timezone)
# @param tweetScores the list of all tweet happiness scores
# @return timezoneTupple the tuple (average happiness, tweet count) for the timezone
#
def timezone_happiness(coordinates, latMin, latMax, longMin, longMax, tweetScores):
    count = 0
    tweetHappinessTotal = 0
    timezoneTupple = ()
    for i in range(0, len(coordinates)):
        coordinate = coordinates[i]
        if coordinate[0]<latMax and coordinate[0]>=latMin and coordinate[1]<longMax and coordinate[1]>=longMin:    # Assumes that for a given timezone min boundary values are inclusive, but max boundary values are not
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
    return timezoneTupple
