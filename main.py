# Import function compute_tweets for use in main function
from sentiment_analysis import compute_tweets


# Main function
# @tweetFile the user's tweet filename input
# @keywordFile the user's keyword filename input
# Calls the compute_tweets function and stores its resulting list as timezoneHappinessList
# Prints the happiness value and number of tweets for each timezone in the US (Eastern, Central, Mountain, Pacific)
#
def main():
    tweetFile = input("Please enter the name of the file containing tweets: ")
    keywordFile = input("Please enter the name of the file containing keywords: ")
    timezoneHappinessList = compute_tweets(tweetFile, keywordFile)
    if timezoneHappinessList == []:
        print(timezoneHappinessList)
    else:
        eastern = timezoneHappinessList[0]
        central = timezoneHappinessList[1]
        mountain = timezoneHappinessList[2]
        pacific = timezoneHappinessList[3]
        print('Eastern timezone:  average "happiness value" = %s, number of tweets = %d' % (str(eastern[0]), eastern[1]))
        print('Central timezone: average "happiness value" = %s, number of tweets = %d' % (str(central[0]), central[1]))
        print('Mountain timezone: average "happiness value" = %s, number of tweets = %d' % (str(mountain[0]), mountain[1]))
        print('Pacific timezone: average "happiness value" = %s, number of tweets = %d' % (str(pacific[0]), pacific[1]))
    return


# Call main function to initiate the program
main()
