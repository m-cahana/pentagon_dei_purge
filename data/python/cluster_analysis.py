import pandas as pd

# **************
# data read-in
# **************

df = pd.read_csv('../../static/data/theme_classified_titles.csv')

# **************
# clean up
# **************

df = df[df.title.notna()]

# Replace asterisks and numbers with empty strings
df['theme'] = (df['theme']
               .str.replace(r'\*', '', regex=True)
               .str.replace(r'\d+', '', regex=True)
               .str.replace('.', '')
               .str.lstrip())

# **************
# analysis
# **************

summary = df.groupby('theme').agg(
    count = ('title', 'count')
)
summary['share'] = summary['count'] / summary['count'].sum()

summary.sort_values(by='count', ascending=False)

# **************
# merge with all titles
# **************

all_titles = pd.read_csv('../../static/data/cleaned_titles.csv')

all_titles = all_titles.merge(
    df[['title', 'theme']],
    on='title',
    how='left'
)


summary = all_titles.groupby('theme').agg(
    count = ('title', 'count')
)
summary['share'] = summary['count'] / summary['count'].sum()

summary.sort_values(by='count', ascending=False)

# **************
# save
# **************

all_titles.to_csv('../../static/data/cleaned_titles_with_themes.csv', index=False)