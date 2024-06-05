# scripts/Module01_Review_preprocessing_script.py

import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import unicodedata

def load_data(file_path):
    return pd.read_csv(file_path)

def drop_columns(df, columns_to_drop):
    df.drop(columns=columns_to_drop, axis=1, inplace=True)
    return df

def handle_null_values(df, column_threshold, row_threshold, important_column):
    df = df.loc[:, (df.isna().sum() < column_threshold) | (df.columns == important_column)]
    df = df.loc[(df.isna().sum(axis=1) < row_threshold) & (df['text'].notna())]
    return df

def remove_duplicates(df):
    return df.drop_duplicates(keep='first')

def correct_area_names(df, area_column):
    valid_areas = [
        "Negombo", "Colombo", "Yala", "Sigiriya", "Mirissa", "Kandy", "Galle", "Nuwara Eliya",
        "Jaffna", "Trincomalee", "Batticaloa", "Anuradhapura", "Polonnaruwa", "Hambantota",
        "Kurunegala", "Puttalam", "Badulla", "Matara", "Ratnapura", "Dambulla", "Ella",
        "Hikkaduwa", "Arugam Bay", "Bentota", "Vavuniya"
    ]
    area_map = {area.lower(): area for area in valid_areas}
    
    def clean_area(area):
        if pd.isna(area):
            return area
        original_area = area.lower().strip()
        if original_area in area_map:
            return area_map[original_area]
        # Attempt to fix common issues such as trailing numbers or characters
        cleaned_area = re.sub(r'\s+\d+', '', original_area)
        cleaned_area = re.sub(r'\s+i+', '', cleaned_area)  # Remove trailing 'i' or 'ii' etc.
        return area_map.get(cleaned_area, original_area)

    df[area_column] = df[area_column].apply(clean_area)
    return df

def remove_html_tags(text):
    if pd.isna(text):
        return text
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def apply_text_cleaning(df, column):
    df[column] = df[column].apply(remove_html_tags)
    return df

def remove_urls(text):
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', str(text))

def remove_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, '', str(text))

def apply_url_email_removal(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: remove_urls(remove_emails(x)))
    return df

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', str(text))

def apply_emoji_removal(df, columns):
    for column in columns:
        df[column] = df[column].apply(remove_emojis)
    return df

def replace_non_english_reviews(df):
    translated_indices = df['textTranslated'].notna()
    df.loc[translated_indices, 'text'] = df.loc[translated_indices, 'textTranslated']
    df.loc[translated_indices, 'textTranslated'] = np.nan
    return df

def clean_text(column):
    column = re.sub(r'\s+', ' ', column)
    column = re.sub(r'[!\"#$%&\'()*+/;<=>?@\[\]^_`{|}~]', '', column)
    column = ' '.join(column.split())
    return column

def apply_text_cleaning_multiple_columns(df, columns):
    for column in columns:
        df[column] = df[column].apply(clean_text)
    return df

def normalize_text_to_lowercase(df, columns):
    for column in columns:
        df[column] = df[column].str.lower()
    return df

def normalize_characters(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize('NFC', text)
    replacements = {
        '“': '"', '”': '"', '‘': "'", '’': "'", '—': '-', '–': '-', '…': '...', '\u2010': '-', '\u2011': '-'
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def apply_normalization(df, columns):
    for column in columns:
        df[column] = df[column].apply(normalize_characters)
    return df

def process_text(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bpm\b', 'P.M.', text, flags=re.IGNORECASE)
    text = re.sub(r'\bam\b', 'A.M.', text, flags=re.IGNORECASE)
    slang_abbrev_dict = {
        "n't": " not", "i'm": "I am", "it's": "it is", "can't": "cannot",
        "don't": "do not", "ain't": "is not", "thx": "thanks", "u": "you",
        "ur": "your", "pls": "please", "asap": "as soon as possible",
        "l8r": "later", "btw": "by the way", "b4": "before", "k": "okay"
    }
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in slang_abbrev_dict.keys()) + r')\b')
    text = pattern.sub(lambda x: slang_abbrev_dict[x.group()], text)
    text = re.sub(r'[\!\?\.,]+(?=[\!\?\.,])', '', text)
    text = re.sub(r'(!){2,}', '!', text)
    text = re.sub(r'(\.){2,}', '.', text)
    return text

def apply_text_processing(df, columns):
    for column in columns:
        df[column] = df[column].apply(process_text)
    return df

def aggregate_reviews(df, group_by_columns, text_column, agg_column_name='Reviews'):
    df[text_column] = df[text_column].astype(str).replace('nan', '')
    grouped_reviews = df.groupby(group_by_columns)[text_column].agg(lambda x: ' || '.join(filter(lambda v: v != 'nan', x))).reset_index()
    grouped_reviews.rename(columns={text_column: agg_column_name}, inplace=True)
    return grouped_reviews

def create_hotel_id(hotel_name):
    if pd.isna(hotel_name):
        return np.nan
    initials = ''.join([word[0] for word in hotel_name.split() if word]).upper()
    name_length = len(hotel_name.replace(' ', ''))
    return f"{initials}{name_length}"

def apply_hotel_id_creation(df, hotel_name_column):
    df['HotelID'] = df[hotel_name_column].apply(create_hotel_id)
    return df

def preprocess(file_path, save_path):
    df = load_data(file_path)
    df = drop_columns(df, ['reviewerId', 'name', 'likesCount'])
    
    column_threshold = len(df) * 0.6
    row_threshold = len(df.columns) * 0.6
    
    df = handle_null_values(df, column_threshold, row_threshold, 'textTranslated')
    df = remove_duplicates(df)
    df = correct_area_names(df, 'Area')
    df = apply_text_cleaning(df, 'text')
    df = apply_text_cleaning(df, 'textTranslated')
    df = apply_url_email_removal(df, ['text', 'textTranslated'])
    df = drop_columns(df, ['reviewerNumberOfReviews', 'publishedAtDate', 'reviewsDistribution/twoStar', 'reviewsDistribution/threeStar', 'reviewsDistribution/oneStar', 'reviewsDistribution/fourStar', 'reviewsDistribution/fiveStar'])
    df = apply_emoji_removal(df, ['text', 'textTranslated'])
    df = replace_non_english_reviews(df)
    
    column_threshold = len(df) * 0.2
    df = df.loc[:, (df.isna().sum() < column_threshold)]

    df = apply_text_cleaning_multiple_columns(df, ['text', 'title', 'Area'])
    df = normalize_text_to_lowercase(df, df.select_dtypes(include=['object']).columns)
    df = apply_normalization(df, ['text'])
    df = apply_text_processing(df, ['text'])

    # Aggregate reviews and create Hotel IDs
    df = aggregate_reviews(df, ['title', 'Area'], 'text')
    df = apply_hotel_id_creation(df, 'title')
    
    # Save cleaned data
    df.to_csv(save_path, index=False)

    # Add this at the end of Module01_Review_preprocessing_script.py

print("Loaded functions:", dir())

