import pandas as pd
from helper_functions import get_top_words, get_top_two_words, get_top_three_words

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


# Identify titles that are one word long and contain numbers
df['one_word_with_numbers'] = df['title'].str.match(r'^\S*\d+\S*$') & ~df['title'].str.contains(r'\s')

# Print examples of one-word titles with numbers
one_word_examples = df[df['one_word_with_numbers']]['title'].head(10).tolist()
print(f"\nExamples of one-word titles with numbers: {one_word_examples}")
print(f"Total one-word titles with numbers: {df['one_word_with_numbers'].sum()}")

clean_df = df[~(df['one_word_with_numbers'])]   


print(f"Total titles: {df.shape[0]}")
print(f"Total titles after cleaning: {clean_df.shape[0]}")

# **************
# top words
# **************

top_three_words = pd.DataFrame(get_top_three_words(clean_df).head(10))


# **************
# keyword lookups
# **************

# it seems like there are a few large clusters that should be split into separate keyword groups
# 1. black (includes things like MLK, tuskegee, soul food, etc.)
# 2. women
# 3. hispanic
# 4. native american/indian (includes powwow, lumbee, code talker, etc.)
# 5. asian
# 6. lgbtq+ / pride (includes gay false pickups)
# 7. various other diversity keywords

keyword_groups = {
    'women': [
        'women', 
        'woman',
        "women's history month",
        "women's history",
        'female',
        'celebrating women',
        'honor women',
        'whm',
        'her shoes',
        'contraceptive', 
        'contraception', 
        'honoring sixtripleeight',
        'wasp', #women airforce service pilots
        'wps', #women, peace, and security
    ],
    'black': [
        'black',
        'black history month', 
        'african american',
        'african-american',
        'african american heritage',
        'african american history',
        'african american history month',
        'juneteenth',
        'tuskegee',
        'martin luther king',
        'martin luthor king',
        'mlk',
        'aahm',
        'aahc',
        'bhm',
        'gospel',
        'soul food', 
        'slave',
        'vance marchbanks',
        'elayne arrington',
    ],
    'hispanic': [
        'hispanic heritage month',
        'hispanic',
        'latin',
        'unidos',
        'latinx',
        'hahm',
        'latin american',
        'buen provecho',
        'fiesta'
    ],
     'asian/pacific islander': [
        'asian',
        'asian american',
        'asian american heritage',
        'asian american heritage month',
        'pacific island',
        'luau',
        'aloha',
        'haka',
        'aapi',
        'apahm', #asian pacific american heritage month
        'aanhpi', #asian american native hawaiian/pacific islander month
    ],
    'native american': [
        'native',
        'indian',
        'powwow',
        'lumbee',
        'indigenous',
        'code talker',
        'navajo', 
        'cherokee',
        'nahm', #native american heritage month
        'naih', #native american and indigenous heritage 
        'naihm', #native american and indigenous heritage month
        'filipino',
    ],
    'lgbtq+': [
        'lgbt',
        'lgbtq',
        'pride',
        'gay',
        'gender', 
        'rainbow',
    ],
    'other ethnicities & religions': [
        'jewish american heritage',
        'holocaust',
        'irish american heritage',
        'german american heritage',
        'eid',
        'french american heritage',
        'italian american heritage',
        'observance graphic',
    ],
    'diversity': [
        'heritage',
        'diversity',
        'dei',
        'deia',
        'unconscious bias',
        'equal employment',
        'inclusive',
        'inclusion',
        'inclusivity',
        'sexual assault prevention',
        'barrier',
        'breaking barriers',
        'multicultural', 
        'multi-cultural',
        'culture',
        'cultural',
        'cultural awareness',
        'immigrant',
        'refugee',
        'disability',
        'disabilities',
        'prosthetic',
        'included',
        'inspiring change', 
        'remembers past', 
        'mentoring moment', 
        'out of the shadows',
        'celebrating culture',
        'celebrating diversity',
        'celebrating history',
        'celebrating heritage',
        'spreading awareness',
        'first',
        'remembrance',
        'next generation',
    ],
    'no clear theme': [
        '', # catch call
        'medical care',
    ],
}

# **************
# keyword grouping
# **************

# create a column that lists all present keyword groups
clean_df['keyword_groups_present'] = clean_df['title'].str.lower().apply(
    lambda x: ', '.join([keyword_group for keyword_group in keyword_groups if any(keyword in x for keyword in keyword_groups[keyword_group])])
)

# create a column that lists top keyword group
clean_df['top_keyword_group'] = clean_df['keyword_groups_present'].str.split(',').str[0]

# create a column that lists all keywords beloning to to the top keyword group
clean_df['top_keyword_group_keywords'] = clean_df.apply(
    lambda x: ', '.join(keyword for keyword in keyword_groups[x['top_keyword_group']] if keyword in x['title'].lower()), 
    axis = 1
)

summary = clean_df['top_keyword_group'].value_counts().reset_index()
summary['share'] = summary['count'] / summary['count'].sum()

# get top keywords by keyword group
top_keywords_by_group = pd.DataFrame()
for keyword_group in keyword_groups:
    for keyword in keyword_groups[keyword_group]:
        count = clean_df[clean_df.title.str.lower().str.contains(keyword)].shape[0]

        top_keywords_by_group = pd.concat([
            top_keywords_by_group, 
            pd.DataFrame({
                'keyword_group': [keyword_group],
                'keyword': [keyword],
                'count': [count]
            })
        ])
# keep only the top 10 keywords by keyword group
top_keywords_by_group = top_keywords_by_group.sort_values(by=['keyword_group', 'count'], ascending=False).groupby('keyword_group').head(5)

# **************
# output
# **************

top_three_words.to_csv('../../static/data/top_three_words.csv', index=False)

summary.to_csv('../../static/data/keyword_summary.csv', index=False)

clean_df.to_csv('../../static/data/cleaned_titles_with_keywords.csv', index=False)

top_keywords_by_group.to_csv('../../static/data/top_keywords_by_group.csv', index=False)

# **************
# explore
# **************

clean_df[clean_df.keyword_groups_present == 'other'].title.sample(10)

get_top_words(clean_df[clean_df.keyword_groups_present == 'other']).head(20)

get_top_two_words(clean_df[clean_df.keyword_groups_present == 'other']).head(50)
