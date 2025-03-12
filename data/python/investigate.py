import pandas as pd
from helper_functions import get_top_words

# **************
# data read-in
# **************

# read the JSON file
df = pd.read_json('../raw/photos.json')

# **************
# data cleaning
# **************

# convert the 'columns' arrays into separate columns
df = pd.DataFrame(df['rows'].tolist())
df = pd.DataFrame(df['columns'].tolist(), columns=['filename', 'title', 'url'])

# clean up the URLs by removing the markdown formatting
df['url'] = df['url'].str.extract(r'\[(.*?)\]')[0]

# mark and remove numeric titles
df['numeric_title'] = df['title'].str.match(r'^\d{6}-[A-Z]-[A-Z0-9]+-\d+$')

clean_df = df[~df['numeric_title']]

# remove duplicate titles
clean_df = clean_df.drop_duplicates(subset=['title'])

print(clean_df.shape[0])

# **************
# top words
# **************

word_counts = get_top_words(clean_df)
print(word_counts.head(50))

# **************
# keyword lookups
# **************

keywords = [
    'black', 
    'women', 
    'woman',
    'hispanic',
    'pacific', 
    'asian', 
    'native',
    'islander', 
    'diversity',
    'pride', 
    'inclusion', 
    'african',
    'indian',
    'aapi', 
    'female', 
    'lgbt', 
    'gender',
    'gay', 
    'heritage', 
    'juneteenth',
    'deia', 
    'tuskegee',
    'disability', 
    'disabilities',
    'martin luther king', 
    'indigenous', 
    'bhm', #black history month
    'apahm', #asian pacific american heritage month
    'aanhpi', #asian american native hawaiian/pacific islander month
    'cultural awareness', 
    'multicultural', 
    'multi-cultural', 
    ]

# create a column that checks if any keyword is present
clean_df['has_keywords'] = clean_df['title'].str.lower().apply(
    lambda x: any(keyword in x for keyword in keywords)
)

# create a column that lists all present keywords
clean_df['keywords_present'] = clean_df['title'].str.lower().apply(
    lambda x: [keyword for keyword in keywords if keyword in x]
)

print(clean_df[clean_df.has_keywords].shape[0] / clean_df.shape[0]) 

# Create Series of word frequencies
word_counts_left = get_top_words(clean_df[~clean_df.has_keywords])

# View top words
print(word_counts_left.head(50))
print(word_counts_left.iloc[50:100])