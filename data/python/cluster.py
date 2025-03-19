from api import api_key
from openai import OpenAI
import pandas as pd
import os
from tqdm import tqdm

# set your OpenAI API key
client = OpenAI(api_key=api_key)

# Define the cost per 1000 tokens for gpt-4o-mini (update with actual values from OpenAI's pricing)
COST_PER_1M_TOKENS = 0.150  # gpt-4o-mini

# Initialize a cumulative cost tracker
total_cost = 0.0
threshold = 1.0

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

clean_df = df[~(df['one_word_with_numbers'])]  

unique_df = clean_df.drop_duplicates(subset=['title'])


# **************
# theme categorization
# **************

def categorize_text_by_theme(text):
    global total_cost, threshold  # Access the global cost tracker and threshold

    # Define the categorization prompt
    prompt = f"""
    You are a text categorization assistant. Your task is to categorize website titles from the military. The titles have recently been erased, and I want to group them into categories. You need to group each title into one of the following groups based on its content:

    1. Black: Titles with events, figures, or topics related to Black people. For example, titles related to Black History Month, African Americans, Juneteenth, the Tuskegee Airmen, etc.
    2. Women: Titles relating to women/females, including both women's cultural events like women's history month, and events specifically for/about female military personnel.
    3. Hispanic: Titles with events, figures, or topics related to Hispanic/Latino people. For example, titles related to Hispanic Heritage Month, Hispanic soldiers, Latin food, fiestas, etc.
    4. Native American: Titles with events, figures, or topics related to Native American/Indigenous people. For example, titles related to Native American Heritage Month, indigenous soldiers, the Navajo code talkers, powwows, various native tribes, etc.
    5. Asian or Pacific Islander: Titles with events, figures, or topics related to Asian and Pacific Islander people. For example, titles related to Asian Heritage Month, Asian soldiers, Asian food, Luaus, etc.
    6. LGBTQ+: Titles with events, figures, or topics related to LGBTQ+ people. For example, titles related to Pride Month, the LGBTQ+ community, the Stonewall Riots, etc. 
    7. Other ethnicities & religions: Titles with events, figures, or topics related to other ethnicities and religions not mentioned above (e.g. not black, not hispanic, not native american, not asian, not pacific islander, not LGBTQ+). For example, titles related to Jewish Heritage Month, the Holocaust, Irish American Heritage, German American Heritage, Iraqi heritage, etc.
    8. Generic DEI: Titles with events, figures, or topics related to diversity and inclusion, but not a specific racial or ethnic group. For example, titles related to diversity training, unconscious bias, equal employment, inclusivity, unspecified heritage, immigrants from unspecified places, barriers being broken, first-time achievements, etc.
    9. Other: Titles that don't fit into any of the above categories. 

    For each title, respond with just the  category name. Make sure to consider a title's context and meaning, and also whether titles were flagged for removal by accident. For example, a title about "Enola Gay" should be categorized as *LGBTQ+* because, even though it's about a plane, the plane's name has "gay" in it and that's probably why it was flagged. Another example: a title about "Vance Marchbanks" should be categorized as *Black* because, even though "black" isn't in the name, it's about a Black soldier.

    Here's the title to categorize: "{text}"
    """
    
    # Send the prompt to OpenAI's API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use gpt-4 for best results
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
    # Extract token usage and calculate cost
    tokens_used = response.usage.total_tokens

    cost = (tokens_used / 1e6) * COST_PER_1M_TOKENS
    total_cost += cost  # Add this call's cost to the cumulative tracker

    # Print cumulative cost only if it crosses the current threshold
    if total_cost >= threshold:
        print(f"Cumulative cost has reached: ${total_cost:.2f}")
        threshold += 1.0  # Increment the threshold to the next dollar amount
    
    # Extract and return the response
    return response.choices[0].message.content.strip()


if not os.path.exists('../../static/data/theme_classified_titles.csv'):
    tqdm.pandas(desc="Categorizing title themes")
    unique_df['theme'] = unique_df['title'].progress_apply(categorize_text_by_theme)

    unique_df.to_csv('../../static/data/theme_classified_titles.csv', index=False)


# **************
# type categorization
# **************


def categorize_text_by_type(text):
    global total_cost, threshold  # Access the global cost tracker and threshold
    # Define the categorization prompt
    prompt = f"""
    You are a text categorization assistant. Your task is to categorize website titles from the military. The titles have recently been erased, and I want to group them into categories. You need to group each title into one of the following groups based on its content:

    1. Explicit heritage events: Titles that celebrate a specific heritage month or event. For example, titles related to Black History Month, Hispanic Heritage Month, Native American Heritage Month, Asian Heritage Month, etc.
    2. Everyday celebrations of heritage or ethnicity: Titles that mention activities or celebrations related to a specific heritage group without explicitly mentioning a heritage month or event. For example, titles related to Asian food, gospel music, female-led movies, fiestas, powwows, etc.
    3. Mentions of personnel that highlight their ethnicity: any mentions of military personnel that call out the fact that these personnel are black, hispanic, native american, asian, etc.
    4. Military personnel that belong to a specific ethnic group, even if that isn't explicitly mentioned: Titles that mention military personnel who happen to a specific heritage group, even if that isn't in the title. For example, titles like Vance Marchbanks (who is black), the code talkers (who are native American), Nishimoto (who is asian), Eric Fanning (who is gay), etc.
    5. Facts of history that relate to a specific ethnic group: Titles that mention facts of history that relate to a specific ethnic group. For example, titles related to slavery, the civil rights movement, the holocaust (but not an official observence event, which would be in category #1), the niagara movement, etc.
    6. Other: Titles that don't fit into any of the above categories.

    For each title, respond with just the  category name (don't include the number).

    Here's the title to categorize: "{text}"
    """
    
    # Send the prompt to OpenAI's API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use gpt-4 for best results
        messages=[
            {"role": "system", "content": prompt},
        ]
    )

    # Extract token usage and calculate cost
    tokens_used = response.usage.total_tokens

    cost = (tokens_used / 1e6) * COST_PER_1M_TOKENS
    total_cost += cost  # Add this call's cost to the cumulative tracker

    # Print cumulative cost only if it crosses the current threshold
    if total_cost >= threshold:
        print(f"Cumulative cost has reached: ${total_cost:.2f}")
        threshold += 1.0  # Increment the threshold to the next dollar amount
    
    # Extract and return the response
    return response.choices[0].message.content.strip()


if not os.path.exists('../../static/data/type_classified_types.csv'):
    tqdm.pandas(desc="Categorizing title types")
    unique_df['type'] = unique_df['title'].progress_apply(categorize_text_by_type)

    unique_df.to_csv('../../static/data/theme_classified_types.csv', index=False)

