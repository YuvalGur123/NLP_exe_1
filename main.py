import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import pandas as pd
import spacy.cli
from nltk import PorterStemmer
from functools import reduce
from collections import Counter
import requests
from bs4 import BeautifulSoup


##### Part 1: Data loading and basic analysis

#load the data into a panda's data frame and count spam/ham messages
print("########### PART 1 ###########")

data = pd.read_csv('spam.csv', encoding='ISO-8859-1')
spam = 0
ham = 0

type_list = data.get('v1').tolist()

for item in type_list:
    if item == 'ham':
        ham = ham + 1
    else:
        spam = spam + 1

print("number of spam: ", spam, " number of ham: ", ham, " total sms: ", spam + ham)

#count number of words per message

avg_words = 0
words_counter = 0

sms_list = data.get('v2').tolist()

for item in sms_list:
    words_counter = words_counter + len(item.split(" "))

avg_words = words_counter / (spam + ham)
print("Average number of words per message: ", avg_words)

#count 5 most frequent words

words_dict = {}

for item in sms_list:
    words = item.split(" ")
    for word in words:
        if word in words_dict:
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1

sorted_dict_reverse = {k: v for k, v in sorted(words_dict.items(), key=lambda x: x[1], reverse=True)}

for idx, k in enumerate(sorted_dict_reverse):
    if idx == 5:
        break
    print("5 most frequent words: ")
    print((k, sorted_dict_reverse[k]))

sorted_dict = {k: v for k, v in sorted(words_dict.items(), key=lambda x: x[1])}

#count the number of words that only appear once

count = 0

for item in sorted_dict:
    if sorted_dict[item] == 1:
        count += 1
print("number of words that only appear once: ", count)

#### Part 2: Text processing

#load the messages of the csv as a string

print("########### PART 2 ###########")

csv_as_string = data.get('v2').astype(str)
string_text = ' '.join(csv_as_string)

#tokenize the words with spacy and nltk

nlp = English()
tokenizer = Tokenizer(nlp.vocab)
tokens_spacy = tokenizer(string_text)


tokens_nltk = nltk.word_tokenize(string_text)

### Time complexity: Both algorithms finished executing almost instantly


#lemmatize the words with spacy and nltk

### nltk

tokens_nltk_lower = [x.lower() for x in tokens_nltk]
lemmatizer = WordNetLemmatizer()
lemmas_nltk = [lemmatizer.lemmatize(i, j[0].lower()) if j[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(i) for i, j in pos_tag(tokens_nltk_lower)]

### spacy

nlp2 = spacy.load('en_core_web_lg')
doc = nlp2(string_text.lower())
spacy_lemmas = ""
for token in doc:
    lemma = token.lemma_
    spacy_lemmas += lemma
    spacy_lemmas += " "

### nltk algorithm to lemmatize finished almost instantly. spacy algorithm takes around 10 seconds, and also requires more user processing

# stem the words with nltk

ps = PorterStemmer()
stemmed_text = reduce(lambda x, y: x + " " + ps.stem(y), tokens_nltk_lower, "")

### Comparing techniques:
### nltk: easy implementation of the different techniques, works fast. supported all parts of the given text.
### lemmatizer and tokenizer provides results in a list, stemmer provides result in a string
### spacy: also easy to implements, requires downloading laguage packages for lemmatizer. lemmatizer algorithm is a lot
### slower than nltk's algorithm, and is provided as a doc object instead of a list of string. doesn't have a stemmer.

### updated statistics:

frequent_words_nltk_tokens = Counter(tokens_nltk).most_common(5)
print("5 most frequent words in nltk tokens: ", frequent_words_nltk_tokens)

frequent_words_nltk_lemmas = Counter(lemmas_nltk).most_common(5)
print("5 most frequent words in nltk lemmas: ", frequent_words_nltk_lemmas)

spacy_tokens_as_words = [token.text for token in tokens_spacy if not token.is_stop and not token.is_punct]

frequent_words_spacy_tokens = Counter(spacy_tokens_as_words).most_common(5)
print("5 most frequent words in spacy tokens: ", frequent_words_spacy_tokens)

frequent_words_spacy_lemmas = Counter(spacy_lemmas.split()).most_common(5)
print("5 most frequent words in spacy lemmas: ", frequent_words_spacy_lemmas)


### Part 3: web scraping

### we will use beautifulsoup to scrape a reddit post

# define a url get function

print("########### PART 3 ###########")


def getData(url):
    r = requests.get(url)
    return r.text


url = "https://www.reddit.com/r/Jokes/comments/1d5jkkn/a_snail_wants_a_ferrari/"
url2 = "https://www.reddit.com/r/Jokes/comments/1dg18jg/the_age_in_the_mirror/"
url3 = "https://www.reddit.com/r/Jokes/comments/1df8i5p/my_dad_is_looking_for_his_keys/"

htmlData = getData(url)
htmlData2 = getData(url2)
htmlData3 = getData(url3)

soup1 = BeautifulSoup(htmlData, 'html.parser')
data_str1 = ""

soup2 = BeautifulSoup(htmlData2, 'html.parser')
data_str2 = ""

soup3 = BeautifulSoup(htmlData3, 'html.parser')
data_str3 = ""

for item in soup1.find_all("div", id="t3_1d5jkkn-post-rtjson-content"):
    data_str1 = data_str1 + item.get_text()
cleaned_text1 = ' '.join(data_str1.split())

for item in soup2.find_all("div", id="t3_1dg18jg-post-rtjson-content"):
    data_str2 = data_str2 + item.get_text()
cleaned_text2 = ' '.join(data_str2.split())

for item in soup3.find_all("div", id="t3_1df9i5p-post-rtjson-content"):
    data_str3 = data_str3 + item.get_text()
cleaned_text3 = ' '.join(data_str3.split())

cleaned_text = cleaned_text1 + " " + cleaned_text2 + " " + cleaned_text3

scrape_tokens = nltk.word_tokenize(cleaned_text)

scrape_tokens_lower = [x.lower() for x in scrape_tokens]
scrape_lemmas = [lemmatizer.lemmatize(i, j[0].lower()) if j[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(i) for i, j in pos_tag(scrape_tokens_lower)]
porter = PorterStemmer()
scrape_stems = [porter.stem(token) for token in scrape_tokens_lower]


frequent_words_scrape = Counter(cleaned_text.split(" ")).most_common(5)
print("5 most frequent words in scraped text: ", frequent_words_scrape)

frequent_words_scrape_tokens = Counter(scrape_tokens_lower).most_common(5)
print("5 most frequent words in nltk tokens: ", frequent_words_scrape_tokens)

frequent_words_scrape_lemmas = Counter(scrape_lemmas).most_common(5)
print("5 most frequent words in nltk lemmas: ", frequent_words_scrape_lemmas)

frequent_words_scrape_stems = Counter(scrape_stems).most_common(5)
print("5 most frequent words in nltk stems: ", frequent_words_scrape_stems)

### part 4: whatsapp analysis

### the text file used in the next part was artificially generated in order to avoid privacy concerns

print("########### PART 4 ###########")

with open("fake_whatsapp_chat.txt", "r", encoding="iso-8859-8") as file:
    lines = file.readlines()

string_text = ' '.join(lines)

whatsapp_tokens = nltk.word_tokenize(string_text)

whatsapp_tokens_lower = [x.lower() for x in whatsapp_tokens]
whatsapp_lemmas = [lemmatizer.lemmatize(i, j[0].lower()) if j[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(i) for i, j in pos_tag(whatsapp_tokens_lower)]
porter = PorterStemmer()
whatsapp_stems = [porter.stem(token) for token in whatsapp_tokens_lower]


frequent_words_whatsapp = Counter(string_text.split(" ")).most_common(5)
print("5 most frequent words in whatsapp text: ", frequent_words_whatsapp)

frequent_words_whatsapp_tokens = Counter(whatsapp_tokens_lower).most_common(5)
print("5 most frequent words in whatsapp tokens: ", frequent_words_whatsapp_tokens)

frequent_words_whatsapp_lemmas = Counter(whatsapp_lemmas).most_common(5)
print("5 most frequent words in whatsapp lemmas: ", frequent_words_whatsapp_lemmas)

frequent_words_whatsapp_stems = Counter(whatsapp_stems).most_common(5)
print("5 most frequent words in whatsapp stems: ", frequent_words_whatsapp_stems)
