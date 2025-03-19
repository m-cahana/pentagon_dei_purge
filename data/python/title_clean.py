import pandas as pd

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

# clean up titles by standardizing apostrophes
df['title'] = df['title'].str.replace("’", "'")

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
# output
# **************

clean_df.to_csv('../../static/data/cleaned_titles.csv', index=False)