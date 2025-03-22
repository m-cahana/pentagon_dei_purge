import pandas as pd

# **************
# data read-in
# **************

df_themes = pd.read_csv('../../static/data/theme_classified_titles.csv')
df_types = pd.read_csv('../../static/data/type_classified_titles.csv')

# **************
# clean up
# **************

df_themes = df_themes[df_themes.title.notna()]

# Replace asterisks and numbers with empty strings
df_themes['theme'] = (df_themes['theme']
               .str.replace(r'\*', '', regex=True)
               .str.replace(r'\d+', '', regex=True)
               .str.replace('.', '')
               .str.lstrip())

df_types = df_types[df_types.title.notna()]

df_types['type'] = (df_types['type']
               .str.replace(r'(^|(?<=\s))4($|(?=\s))', "Military personnel that belong to a specific ethnic group, even if that isn't explicitly mentioned", regex=True)
               .str.replace(r'\*', '', regex=True)
               .str.replace(r'\d+', '', regex=True)
               .str.replace('.', '')
               .str.lstrip()
               .str.replace('Inclusive heritage and DEI events', 'Explicit heritage and DEI events')
               .str.replace(r'(^|(?<=\s))Military personnel that belong to a specific ethnic group($|(?=\s))', "Military personnel that belong to a specific ethnic group, even if that isn't explicitly mentioned", regex=True))

# map to simpler types
df_types['type'] = df_types['type'].replace(
    {
        "Everyday celebrations of heritage or ethnicity": "Everyday celebrations",
        "Mentions of personnel that highlight their ethnicity": "Military personnel - identity mentioned",
        "Military personnel that belong to a specific ethnic group, even if that isn't explicitly mentioned": "Military personnel - no stated identity",
        "Facts of history that relate to a specific ethnic group": "Facts of history",
    }
)

# **************
# analysis
# **************

summary_themes = df_themes.groupby('theme').agg(
    count = ('title', 'count')
)
summary_themes['share'] = summary_themes['count'] / summary_themes['count'].sum()

summary_themes.sort_values(by='count', ascending=False)

summary_types = df_types.groupby('type').agg(
    count = ('title', 'count')
)
summary_types['share'] = summary_types['count'] / summary_types['count'].sum()

summary_types.sort_values(by='count', ascending=False)

# **************
# merge with all titles
# **************

all_titles = pd.read_csv('../../static/data/cleaned_titles.csv')

all_titles = all_titles[all_titles.title.notna()]

all_titles = all_titles.merge(
    df_themes[['title', 'theme']],
    on='title',
    how='left'
).merge(
    df_types[['title', 'type']],
    on='title',
    how='left'
)

summary = all_titles.groupby(['theme', 'type']).agg(
    count = ('title', 'count')
)
summary['share'] = summary['count'] / summary['count'].sum()

summary.sort_values(by='count', ascending=False)

# **************
# save
# **************

all_titles.to_csv('../../static/data/cleaned_titles_with_themes_and_types.csv', index=False)