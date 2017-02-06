"""
Problem 3:  analyze every US presidential inaugural address

Questions:
1. Comparing 2009's and 2013's addresses, which used the word "country" more often?
2. Comparing all of the addresses, which used the word "war" most often?
3. Which of the addresses contains the largest number of four-letter words?
4. Which of the addresses was longest?
5. Which of the addresses had the longest average word length?
6. What did sentiment of these addresses look like over time?

Answers:
1. 'Country' is used 6 times in 2013 and 2 times in 2009
2. Address of 1821 used word 'war' most at 16 times (run main() function to see analysis over time)
3. Address of 1841 had most 4 letter words at 1000
4. Address of 1841 was longest at 8424 words
5. Address of 1893 had longest average word at 5.0575
6. Run main() function to see analysis of sentiment over time
"""

import os
import os.path
from collections import defaultdict
from textblob import TextBlob
import numpy as np
import pylab as pl

# Plotting documentation: http://www.ast.uct.ac.za/~sarblyth/pythonGuide/PythonPlottingBeginnersGuide.pdf
# TextBlob documentation: https://textblob.readthedocs.io/en/latest/quickstart.html#quickstart

# Something wrong with counting 4 letter words


def main():
    """ function that analyzes inaugural addresses """
    data = "addresses"
    os.chdir(data)
    q1(data)
    rest(data)
    os.chdir('..')


def q1(data):
    """ helper function that answers subquestion 1 of question 3 that requires only looking @ 2009 and 2013
        1. Comparing 2009's and 2013's addresses, which used the word "country" more often? """
    relevant_addresses = []
    all_addresses = os.listdir()
    print(all_addresses)
    for address_title in all_addresses:
        if address_title == "2009.txt":
            relevant_addresses.append(address_title)
        elif address_title == "2013.txt":
            relevant_addresses.append(address_title)

    print(relevant_addresses)
    country_mentions = defaultdict(int)

    for address in relevant_addresses:
        try:

            clean_address = address.strip('.txt')
            f = open(address, "r", encoding="latin1")  # latin1 is a very safe encoding
            data = f.read()  # read all of the file's data
            clean_data = ''

            for character in data:      # this addition changed our totals for war and country
                if character.isalpha() or character == ' ' or character == '\n':
                    clean_data += character

            split_address = clean_data.split()
            # print(split_address)

            for word in split_address:

                if word.lower() == 'country':
                    # print(word)
                    country_mentions[clean_address] += 1

            f.close()         # close the file
        except PermissionError:  # example of "exceptions": atypical errors

            data = ""
        except UnicodeDecodeError:

            data = ""   # no data
        except FileNotFoundError:  # try it with and without this block...

            data = ""

    print("# of Times Word 'Country' is Used in 2009 vs. 2013: ", country_mentions)


def rest(data):
    """ Answers the rest of the subquestions for question 3 that require analyzing all addresses
        2. Comparing all of the addresses, which used the word "war" most often?
        3. Which of the addresses contains the largest number of four-letter words?
        4. Which of the addresses was longest?
        5. Which of the addresses had the longest average word length?
        6. What did sentiment of these addresses look like over time? """

    addresses = os.listdir()

    # create dictionary, lists, and counter necessary to answer question 2
    war_mentions = defaultdict(int)
    year_most_war_mentions = 0
    most_war_mentions = 0
    war_mentions_x = []
    war_mentions_y = []

    # create dictionary and counters necessary to answer question 3
    four_letter_words = defaultdict(int)
    year_most_four_letter_words = 0
    most_four_letter_words = 0

    # create dictionary and counters necessary to answer question 4
    address_length = defaultdict(int)
    year_address_length = 0
    most_address_length = 0

    # create dictionaries and counters necesary to answer question 5
    number_of_characters = defaultdict(int)
    avg_word_length = defaultdict(int)
    year_most_avg_word_length = 0
    most_avg_word_length = 0

    # create lists necessary to graph sentiment (y) and year (x)
    sentiment_analysis_x_axis = []
    sentiment_analysis_y_axis = []

    for address in addresses:
        try:

            clean_address = address.strip('.txt')   # read in all of the addresses and remove '.txt' suffix'
            f = open(address, "r", encoding="latin1")  # latin1 is a very safe encoding
            data = f.read()

            clean_data = ''     # clean data by taking out all non-alphabetic characters
            for character in data:      # this addition changed our totals for war and country
                if character.isalpha() or character == ' ' or character == '\n':
                    clean_data += character

            text_for_sentiment_analysis = TextBlob(clean_data)      # perform textual analysis on specified address
            sentiment_analysis_x_axis.append(clean_address)         # store year for later ploting
            sentiment_analysis_y_axis.append(text_for_sentiment_analysis.sentiment[0])      # store sentiment value for later plotting
            print(clean_address, ' ', text_for_sentiment_analysis.sentiment[0])     # print year:sentiment pairs

            split_address = clean_data.split()  # split data by words

            for word in split_address:      # loops over every word in every address

                if word.lower() == 'war':       # checks to see if word is 'war'
                    war_mentions[clean_address] += 1

                # this appears to be off a little...
                elif len(word) == 4:            # checks length of every word
                    four_letter_words[clean_address] += 1

                address_length[clean_address] += 1      # tracks length of address (not efficient but hey loop/counter practice)
                number_of_characters[clean_address] += len(word)

            if war_mentions[clean_address] > most_war_mentions:     # process to find most 'war' mentions
                year_most_war_mentions = clean_address
                most_war_mentions = war_mentions[clean_address]

            if four_letter_words[clean_address] > most_four_letter_words:   # process to find most 4 letter words
                year_most_four_letter_words = clean_address
                most_four_letter_words = four_letter_words[clean_address]

            if address_length[clean_address] > most_address_length:     # process to find longest address
                year_address_length = clean_address
                most_address_length = address_length[clean_address]

            f.close()         # close the file
        except PermissionError:  # example of "exceptions": atypical errors

            data = ""
        except UnicodeDecodeError:

            data = ""   # no data
        except FileNotFoundError:  # try it with and without this block...

            data = ""

        war_mentions_x.append(clean_address)
        war_mentions_y.append(war_mentions[clean_address])

    for address in address_length:      # calculate avg. word length and determine maximum
        avg_word = number_of_characters[address]/address_length[address]
        avg_word_length[address] += avg_word
        if avg_word_length[address] > most_avg_word_length:
            year_most_avg_word_length = address
            most_avg_word_length = avg_word_length[address]

    mean_sentiment = sum(sentiment_analysis_y_axis)/len(sentiment_analysis_y_axis)  # create mean line on sentiment graph

    print("# of Times War is Mentioned: ", war_mentions)
    print("# of Four Letter Words Used: ", four_letter_words)
    print("Address Length (Word): ", address_length)
    print("Average Word Length: ", avg_word_length)

    print('Most Times War is Mentioned: ', most_war_mentions, ' in ', year_most_war_mentions)
    print('Most 4 Letter Words: ', most_four_letter_words, ' in ', year_most_four_letter_words)
    print('Longest Address: ', most_address_length, ' in ', year_address_length)
    print('Longest Average Word: ', most_avg_word_length, ' in ', year_most_avg_word_length)

    for x in range(len(sentiment_analysis_x_axis)):     # convert year labels (str) to floats for plotting/analysis
        sentiment_analysis_x_axis[x] = float(sentiment_analysis_x_axis[x])

    mean_sentiment_list = []       # extend mean sentiment across all x values
    for x in sentiment_analysis_x_axis:
        mean_sentiment_list.append(mean_sentiment)

    plot1 = pl.plot(sentiment_analysis_x_axis, sentiment_analysis_y_axis, 'r', label='Address Sentiment')   # line graph of address sentiment over time
    plot2 = pl.plot(sentiment_analysis_x_axis, mean_sentiment_list, 'g', label='Mean Sentiment')
    pl.xlabel('Year')
    pl.ylabel('Natural Language Processing Value for Address Sentiment (Range: -1, 1)')
    pl.xlim(1788, 2018)
    pl.legend(loc='best')
    pl.show()

    scatter_x = sentiment_analysis_x_axis       # create a scatter plot in order to facilitate linear regression
    scatter_y = sentiment_analysis_y_axis
    (m, b) = np.polyfit(scatter_x, scatter_y, 1)    # analyzes trend in sentiment over time
    yp = np.polyval([m, b], scatter_x)
    yp_slope = (yp[-1] - yp[0])/len(yp)
    print("Slope of sentiment trendline is: ", yp_slope)
    print("This contradicts downward trend in positive language noted in hw0pr0")
    pl.plot(scatter_x, yp, color='red', label='Sentiment Trend Line (Linear Regression)')
    pl.scatter(scatter_x, scatter_y)
    pl.xlabel('Year')
    pl.ylabel('Natural Language Processing Value for Address Sentiment (Range: -1, 1)')
    pl.xlim(1788, 2018)
    pl.legend(loc='best')
    pl.show()

    pl.plot(war_mentions_x, war_mentions_y)     # line graph to analyze usage of word 'war' over time
    pl.xlabel('Year')
    pl.ylabel('# of Times "War" Mentioned')
    pl.xlim(1788, 2018)
    pl.show()

    return sentiment_analysis_y_axis
