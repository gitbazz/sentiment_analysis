# Sentiment Analysis

Performs sentiment analysis on Twitter data. The Twitter data contains comments from individuals about how they feel about their lives and comes from individuals across the continental United States. Determines which timezone (Eastern, Central, Mountain, Pacific is the “happiest”. 

**tweets.txt** contains the tweets

**keywords.txt** contains sentiment keywords and their “happiness scores”

**sentiment_analysis.py** processes the files of *keywords.txt* and *tweets.txt*. Computes the “happiness score” for each tweet and computes the “happiness score” for each timezone. Returns a list of tuples. The tuples contain the results of each of the regions, in order: Eastern, Central, Mountain, Pacific. Each tuple contains two values: (average, count), where average is the average “happiness value” of that region and count is the number of tweets found in that region.

**main.py** prompts the user for the name of the two files – the file containing the keywords and the file containing the tweets. Processes the tweets using the given keywords and prints the results in a readable fashion.

**tweets1.txt & tweets2.txt** small test files that contain tweets

**key1.txt & key2.txt** test files that contain keywords and “happiness values”

**driver.py** uses test files to test program
