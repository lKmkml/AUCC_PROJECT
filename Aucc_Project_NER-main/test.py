import spacy
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import translators as ts
text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
def list_word(text):
    article = text
    tokens = word_tokenize(article)
    lower_tokens = [t.lower() for t in tokens]
    alpha_only = [t for t in lower_tokens if t.isalpha()]
    no_stops = [t for t in alpha_only if t not in stopwords.words('english')]
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
    lemmatized.sort()
    return lemmatized
test_list = list_word(text)
def ts_to_thai(word):
  word_ts = ts.google(word, from_language='en', to_language='th')
  return word_ts

nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
for ent in doc.ents:
    print(ent.label_,ent.text)
test_list_ts = []
for i in test_list:
  x = ts_to_thai(i)
  test_list_ts.append(x)
  print(i,":",x)
