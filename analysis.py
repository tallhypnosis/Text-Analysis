import os
import pandas as pd
import bs4 as BeautifulSoup
import requests
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict

def fetch_article_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        print(f"{response.status_code}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')
            
            # Find the article title
            title_element = soup.select_one('div.td-full-screen-header-image-wrap h1')

            # Find the article content
            article_content = soup.find('div', class_='td-post-content tagdiv-type')
            article_title = title_element.get_text() if title_element else "Title not found"

            # Initialize an empty string to store the article text
            article_text = ''
            
            # Extract text from paragraphs and ordered lists within the article content
            if article_content:
                for element in article_content.children:
                    if element.name == 'p' or element.name == 'ol' or element.name =='pre' or element.name == 'ul':
                        article_text += element.get_text(separator='\n') + '\n'
                
                # Return the article text
                return article_title, article_text
            else:
                print("Article content not found.")
                return None, None
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error occurred while fetching {url}:", e)
        return None, None

# Load URLs from Excel file
input_file = 'Input.xlsx'
data = pd.read_excel(input_file)

# Create directory to save text files
output_directory = 'extracted_articles1'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate through each URL
for index, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    print(f"Processing {url_id} {url}")
    article_title, article_text = fetch_article_text(url)
    # print(article_text)
    if article_text:
        # Save article text to a text file
        with open(os.path.join(output_directory, f"{url_id}.txt"), "a+", encoding="utf-8") as f:
            print(article_title)
            f.write(article_title + "\n" + "\n") # Write title
            f.write(article_text) # Write text
        print(f"Article text saved for {url_id}")
    else:
        print(f"Failed to fetch article text for {url_id}")

print("Extraction completed.")

# Download NLTK corpus
nltk.download('punkt')
nltk.download('cmudict')

# Function to load stop words
def load_stop_words(stop_words_dir):
    stop_words = set()
    for filename in os.listdir(stop_words_dir):
        with open(os.path.join(stop_words_dir, filename), 'r') as file:
            stop_words.update(file.read().splitlines())
    return stop_words

# Function to load master dictionary
def load_master_dictionary(master_dict_dir, stop_words):
    master_dict = {'positive-words':set(), 'negative-words':set()}
    for sentiment in master_dict.keys():
        with open(os.path.join(master_dict_dir, sentiment + ".txt"), 'r') as file:
            words = file.read().splitlines()
            master_dict[sentiment].update([word for word in words if word not in stop_words])
    return master_dict

# Function to calculate derived variables
def calculated_variables(text, stop_words, master_dict):
    # Tokenize text
    tokens = word_tokenize(text.lower())
    personal_pronouns_count = 0

    # Count personal pronouns
    for token in tokens:
        if token.lower() in ["i", "we", "my", "ours", "us"]:
            personal_pronouns_count += 1

    # Remove stop words and punctuation
    cleaned_tokens = [token for token in tokens if token not in stop_words and re.match(r'\w', token)]
    
    # Initialize scores and counts
    pos_score = 0
    neg_score = 0
    total_words = len(cleaned_tokens)
    complex_word_count = 0
    syllable_count = 0

    # Initialize CMU dictionary for syllable count
    cmu_dict = cmudict.dict()

    # Count positive and negative words, syllable, complex words, and person pronouns
    for token in cleaned_tokens:
        if token in master_dict['positive-words']:
            pos_score += 1
        elif token in master_dict['negative-words']:
            neg_score += 1


        # Count syllables using CMU dictionary
        if token.lower() in cmu_dict:
            syllable_count += max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[token.lower()]])


        # Count complex words
        if syllable_count > 2:
            complex_word_count += 1


    # Calculate derived variables
    polarity_score = (pos_score - neg_score)/((pos_score + neg_score) + 0.000001)
    subjectivity_score = (pos_score + neg_score)/ ((total_words) + 0.000001)
    average_word_length = sum(len(word) for word in cleaned_tokens) / (total_words + 0.000001)
    personal_pronouns_ratio = personal_pronouns_count / (total_words + 0.000001)
    average_sentence_length = len(sent_tokenize(text)) / (total_words + 0.0000001)
    percentage_complex_words = complex_word_count/ (total_words + 0.000001)
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    syllable_per_word = syllable_count / (0.000001 + syllable_count) 
    avg_num_words_per_sent = 1/(average_sentence_length)

    return {
        "Positive Score": pos_score,
        "Negative Score": neg_score,
        "Polarity Score": polarity_score,
        "Subjectivity Score": subjectivity_score,
        "Average Sentence Length": average_sentence_length,
        "Percentage of Complex Words": percentage_complex_words,
        "Fog Index": fog_index,
        "Avg Number of Words Per Sentence": avg_num_words_per_sent,
        "Complex Word Count": complex_word_count,
        "Word Count": total_words,
        "Syllable Per Word": syllable_per_word,
        "Personal Pronouns Count": personal_pronouns_count,
        "Personal Pronouns Ratio": personal_pronouns_ratio,
        "Average Word Length": average_word_length,
        }

# Folder paths
stop_words_dir = "StopWords"
master_dict_dir = "MasterDictionary"
extracted_articles_dir = "extracted_articles1"

# Load stop words and master dictionary
stop_words = load_stop_words(stop_words_dir)
master_dict = load_master_dictionary(master_dict_dir, stop_words)

# Output file path 
output_file = 'Output_Data_Structure1.csv'

# Open output file for writing
with open(output_file, 'w') as f:
    # Write header
    f.write('.'.join([
        "File Name", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
        "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
        "Avg Number of Words Per Sentence", "Complex Word Count", "Word Count", 
        "Syllable Per Word", "Personal Pronouns Count", "Personal Pronouns Ratio", "Average Word Length"
    ]) + '\n')

    # Iterate over each file in the folder
    for filename in os.listdir(extracted_articles_dir):
        # Read the content of each file
        with open(os.path.join(extracted_articles_dir, filename), 'r', encoding='utf-8') as article_file:
            text = article_file.read()

            # Calculate derived variables
            variables = calculated_variables(text, stop_words, master_dict)
            print(variables)

            # Format derived variables
            formatted_variables = [
                filename,
                variables["Positive Score"],
                variables["Negative Score"],
                variables["Polarity Score"],
                variables["Subjectivity Score"],
                variables["Average Sentence Length"],
                variables["Percentage of Complex Words"],
                variables["Fog Index"],
                variables["Avg Number of Words Per Sentence"],
                variables["Complex Word Count"],
                variables["Word Count"],
                variables["Syllable Per Word"],
                variables["Personal Pronouns Count"],
                variables["Personal Pronouns Ratio"],
                variables["Average Word Length"]
            ]
        
            # Write derived variables to output file
            f.write(f"{','.join(str(variable) for variable in formatted_variables)}\n")

print(f"Derived variables saved to: {output_file}")
