import pandas as pd
import nltk
from nltk.corpus import stopwords


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

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    word_counts = word_counts[~word_counts.index.isin(stop_words)]

    return word_counts


