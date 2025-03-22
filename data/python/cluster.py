from api import api_key
from openai import OpenAI
import pandas as pd
import os
from tqdm import tqdm

# set your OpenAI API key
client = OpenAI(api_key=api_key)

# **************
# config
# **************

slight_redo = True

# **************
# data read-in
# **************

clean_df = pd.read_csv('../../static/data/cleaned_titles.csv')

unique_df = clean_df.drop_duplicates(subset=['title'])


# **************
# theme categorization
# **************

def categorize_text_by_theme(text):

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

    # Define the categorization prompt
    prompt = f"""
    You are a text categorization assistant. Your task is to categorize website titles from the military. The titles have recently been erased, and I want to group them into categories. You need to group each title into one of the following groups based on its content:

    1. Explicit heritage and DEI events: Titles that celebrate a specific heritage month or event, or an explicit Diversity, Equity, and Inclusion (DEI) program. For example, titles related to Black History Month, Hispanic Heritage Month, Native American Heritage Month, Asian Heritage Month, Inclusivity workshops, etc.
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

    # Extract and return the response
    return response.choices[0].message.content.strip()


# run in chunks to avoid timeouts
chunk_size = 250  # Process 250 titles at a time
num_chunks = len(unique_df) // chunk_size + (1 if len(unique_df) % chunk_size != 0 else 0)

print(f"Processing {len(unique_df)} titles in {num_chunks} chunks of {chunk_size}")

# Initialize an empty dataframe to collect all processed chunks
all_processed_df = pd.DataFrame()

total_na = 0

# Process each chunk
for i in range(num_chunks):
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(unique_df))

    print(f"Processing chunk {i+1}/{num_chunks} (titles {start_idx}-{end_idx-1})")

    # Get the current chunk
    chunk_df = unique_df.iloc[start_idx:end_idx].copy()

    # Check if this chunk was already processed
    chunk_file = f"../../data/processed/title_chunks/type_chunk_{i+1}.csv"
    if os.path.exists(chunk_file):
        print(f"Loading already processed chunk {i+1} from {chunk_file}")
        processed_chunk = pd.read_csv(chunk_file)

        print(f'nas in chunk: {processed_chunk.type.isna().sum()}')
        total_na += processed_chunk.type.isna().sum()
    else:
        # Process this chunk
        tqdm.pandas(desc=f"Categorizing titles in chunk {i+1}/{num_chunks}")
        chunk_df['type'] = chunk_df['title'].progress_apply(categorize_text_by_type)
        
        # Save this chunk
        chunk_df.to_csv(chunk_file, index=False)
        processed_chunk = chunk_df
    
    print(f"Completed and saved chunk {i+1}/{num_chunks}")

    # Append to the full results
    all_processed_df = pd.concat([all_processed_df, processed_chunk], ignore_index=True)
        
# Save the complete dataset
all_processed_df.to_csv('../../static/data/type_classified_titles.csv', index=False)

print("All chunks processed and combined into final output file")

if slight_redo:
    missing_chunk_filename = '../../data/processed/title_chunks/missing_titles_chunk.csv'
    if os.path.exists(missing_chunk_filename):
        print('no missing titles to categorize')
        missing_titles = pd.read_csv(missing_chunk_filename)

    else:
         
        print('classifying missing titles...')
        prev_df = pd.read_csv('../../static/data/type_classified_titles.csv')

        missing_titles = unique_df[~unique_df['title'].isin(prev_df['title'])]
        
        print(f'missing titles: {len(missing_titles)}')

        tqdm.pandas(desc="Categorizing missing titles")
        missing_titles['type'] = missing_titles['title'].progress_apply(categorize_text_by_type)

        missing_titles.to_csv(missing_chunk_filename, index=False)


    all_processed_df = pd.concat([all_processed_df, missing_titles], ignore_index=True)

    all_processed_df.to_csv('../../static/data/type_classified_titles.csv', index=False)

