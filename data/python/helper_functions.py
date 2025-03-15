import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag


def get_top_words(df):
    # concatenate all titles without keywords and split into words
    all_words = (df['title']
                 # convert to lowercase 
                .str.lower()                    
                # concatenate all titles with space separator
                .str.cat(sep=' ')              
                # split into list of words
                .split())                      

    # create Series of word frequencies 
    word_counts = pd.Series(all_words).value_counts()

    # remove stopwords and verbs
    stop_words = list(set(stopwords.words('english')))

    word_counts = word_counts[~word_counts.index.isin(stop_words)]

    return word_counts


def get_top_two_words(df):

    two_word_phrases = []

    for title in df['title']:
        words = title.split()
        phrases = [' '.join(pair) for pair in zip(words, words[1:])]
        two_word_phrases.extend(phrases)

    two_word_counts = pd.Series(two_word_phrases).value_counts()

    # filter out cases where both words are stop words
    stop_words = list(set(stopwords.words('english')))
    
    two_word_counts = two_word_counts[(~two_word_counts.index.str.split(' ').str[0].isin(stop_words)) & (~two_word_counts.index.str.split(' ').str[1].isin(stop_words))]
    
    
    # Return only phrases without verbs
    return two_word_counts


def get_top_three_words(df):
    three_word_phrases = []

    for title in df['title']:
        words = title.split()
        phrases = [' '.join(pair) for pair in zip(words, words[1:], words[2:])]
        three_word_phrases.extend(phrases)

    three_word_counts = pd.Series(three_word_phrases).value_counts()

    # filter out cases where both words are stop words
    stop_words = list(set(stopwords.words('english')))
    three_word_counts = three_word_counts[(~three_word_counts.index.str.split(' ').str[0].isin(stop_words)) & (~three_word_counts.index.str.split(' ').str[1].isin(stop_words)) & (~three_word_counts.index.str.split(' ').str[2].isin(stop_words))]

    return three_word_counts
    