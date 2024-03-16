# Text-Analysis
Python script to perform text analysis

## Overview
This script extracts article text from URLs provided in an Excel file and then analyzes the extracted text to derive various linguistic features and sentiment scores. The analysis includes calculating positive and negative scores, polarity score, subjectivity score, average word length, average sentence length, percentage of complex words, fog index, syllable per word, personal pronouns count, and average word length. The extracted data is then saved to a CSV file for further analysis.

## Dependencies
- Python 3: Ensure you have Python 3 installed on your system.
- NLTK (Natural Language Toolkit): Used for text processing tasks such as tokenization and sentiment analysis.
- Beautiful Soup (bs4): Used for parsing HTML content when extracting article text from web pages.
- Requests: Used to make HTTP requests when fetching article content from URLs.
- Pandas: Used to read data from Excel files.

You can install these dependencies using pip:
```bash
pip install nltk beautifulsoup4 requests pandas



How to Use
Setup Environment:
Install Python 3 if not already installed.
Install the required dependencies using the provided command.
Prepare Input Data:
Create an Excel file (Input.xlsx) containing URLs of articles to be analyzed. Ensure that the Excel file has a column named URL containing the URLs.
Place the Excel file in the same directory as the script.
Run the Script:
Execute the script analysis.py using the following command:

bash
Copy code
python analysis.py
This will start the process of fetching article text from the provided URLs and analyzing the text to derive linguistic features and sentiment scores.

View Output:
Once the script completes execution, it will generate a CSV file (Output_Data_Structure.csv) containing the derived variables and scores for each article. You can open this CSV file using any spreadsheet software for further analysis and visualization.

Approach
Text Extraction:
The script fetches article text from the URLs provided in the Excel file using the requests library.
It parses the HTML content of the web pages using Beautiful Soup to extract the article text while excluding website headers, footers, and other irrelevant content.
Text Analysis:
After extracting the article text, the script analyzes the text to derive various linguistic features and sentiment scores.
It calculates positive and negative scores, polarity score, subjectivity score, average word length, average sentence length, percentage of complex words, fog index, syllable per word, personal pronouns count, and average word length.
Output
The derived variables and scores are saved to a CSV file for each article, with each row representing an article and each column representing a derived feature or score.

Note
Ensure that the MasterDictionary and StopWords directories containing the required dictionaries and stop words are present in the same directory as the script.
Make sure that the extracted_articles directory is created to store the extracted article text files.