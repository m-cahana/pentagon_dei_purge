import pandas as pd
from helper_functions import get_top_words, get_top_two_words, get_top_three_words
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

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
df['numeric_title'] = df['title'].str.match(r'^\d{6}-[A-Z]-[A-Z0-9]+-\d+$') | df['title'].str.match(r'^\d{6}-[a-z]-[a-z0-9]+-\d+(\.[a-z]+)?$')

clean_df = df[~df['numeric_title']]

# remove duplicate titles
clean_df_no_duplicates = clean_df.drop_duplicates(subset=['title'])

print(clean_df.shape[0])

# ************** 
# cluster titles
# **************

# Load the pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert titles to embeddings
embeddings = model.encode(clean_df_no_duplicates.title.tolist())

# Perform clustering using KMeans
kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(embeddings)

# Add cluster labels to the DataFrame
clean_df_no_duplicates['cluster'] = kmeans.labels_

# **************
# top words
# **************

word_counts = get_top_words(clean_df)
print(word_counts.head(50))

two_word_counts = get_top_two_words(clean_df)
print(two_word_counts.head(50))

three_word_counts = get_top_three_words(clean_df)
print(three_word_counts.head(50))

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
    'dei',
    'unconscious bias',
    'equal employment',
    'pride', 
    'inclusion', 
    'inclusive',
    'included',
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
    # relatedly - Vance Marchbanks Jr., tuskegee airman who was purged
    'disability', 
    'disabilities',
    'martin luther king', 
    'mlk',
    'indigenous', 
    'bhm', #black history month
    'aahm', #african american heritage month,
    'aahc', #african american heritage celebration?
    'apahm', #asian pacific american heritage month
    'aanhpi', #asian american native hawaiian/pacific islander month
    'nahm', #native american heritage month
    'naih', #native american and indigenous heritage 
    'naihm', #native american and indigenous heritage month
    'hahm', #hispanic american heritage month
    'whm', #women's history month
    'culture', 
    'cultural', 
    'multicultural', 
    'multi-cultural', 
    'immigrant', 
    'refugee', 
    'slave', 
    'gospel',
    'yasuke', #https://en.wikipedia.org/wiki/Yasuke
    'latin',
    'unidos',
    'soul food',
    'code talker', 
    'navajo', 
    'cherokee', 
    'powwow', 
    'lumbee',
    'barrier', 
    'contraceptive',
    ]

# create a column that checks if any keyword is present
clean_df['has_keywords'] = clean_df['title'].str.lower().apply(
    lambda x: any(keyword in x for keyword in keywords)
)

# create a column that lists all present keywords
clean_df['keywords_present'] = clean_df['title'].str.lower().apply(
    lambda x: ', '.join([keyword for keyword in keywords if keyword in x])
)

clean_df = clean_df.merge(clean_df_no_duplicates[['title', 'cluster']], on='title', how='left')

# top keywords by cluster
for cluster in clean_df.cluster.unique():
    print(cluster)
    print(get_top_two_words(clean_df[clean_df.cluster == cluster]).head(50))
    print('\n')

print(get_top_two_words(clean_df[clean_df.keywords_present.str.contains('native')]).head(50))

# count the number of photos with each keyword, and the percentage of photos with each keyword
keyword_summary = pd.DataFrame(columns=['keyword', 'photos', 'percentage'])
for keyword in keywords:
    keyword_summary = pd.concat([keyword_summary, pd.DataFrame({'keyword': [keyword], 'photos': [clean_df[clean_df['keywords_present'].str.contains(keyword)].shape[0]], 'percentage': [clean_df[clean_df['keywords_present'].str.contains(keyword)].shape[0] / clean_df.shape[0]]})])

keyword_summary = keyword_summary.sort_values(by='percentage', ascending=False)

print(clean_df[clean_df.has_keywords].shape[0] / clean_df.shape[0]) 

# Create Series of word frequencies
word_counts_left = get_top_words(clean_df[~clean_df.has_keywords])

# View top words
print(word_counts_left.head(50))
print(word_counts_left.iloc[50:100])

# **************
# save the cleaned data
# **************

clean_df[~clean_df.has_keywords].to_csv('../processed/remaining_photos.csv', index=False)

