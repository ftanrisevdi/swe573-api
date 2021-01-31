import os
from decouple import config
import emoji
import tagme
import re
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet','nltk_data')
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer 
from nltk.probability import FreqDist
module_dir = os.path.dirname(__file__)  # get current directory
file_path_w = os.path.join(module_dir, 'stopwords.txt')
file_path_c = os.path.join(module_dir, 'stopcharachers.txt')
file_path_msw = os.path.join(module_dir, 'stopcustomwords.txt')


tagme.GCUBE_TOKEN = config('Tagme')
ttkn = RegexpTokenizer("\s+", gaps=True)
lemmatizer = WordNetLemmatizer() 

def remore_br(text):
  text = text.replace("<br />", " ")
  return text

def get_stopwords():
  words = open(file_path_w,'r')
  stopwords = [word.strip() for word in words]
  return set(stopwords) 

def get_stopcharacters():
  characters = open(file_path_c,'r')
  stopcharacters = [word.strip() for word in characters]
  return set(stopcharacters) 

def get_stop_custom_word():
  characters = open(file_path_msw,'r')
  stopcharacters = [word.strip() for word in characters]
  return set(stopcharacters) 

def word_count(sentences):
  arr =[]
  tokens = ttkn.tokenize(sentences)
  fdist=FreqDist(tokens)
  d = fdist.most_common(20)
  for key, repeat in d:
    arr.append([key,repeat])
  return arr

def clean_text(text): 
  result = ""
  lower = text.lower()
  lemmatize = [] 
  filtered_sentence = ''.join([char for char in lower if not char in get_stopcharacters()] )
  word_tokens = ttkn.tokenize(filtered_sentence)
  filtered_sentence = [w for w in word_tokens if not w in get_stopwords()]
  filtered_sentence = [w for w in filtered_sentence if not w in get_stop_custom_word()]
  for w in filtered_sentence:
    lemma =lemmatizer.lemmatize(w, pos="v")
    lemmatize.append(lemma)
  result = result + ' '.join(lemmatize)
  return result 

def give_emoji_free_text(text):
  allchars = [str for str in text]
  emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
  strr = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
  return strr  

def mytagme_ann(data):
  annotations = tagme.annotate(data)
  dic ={}
  for ann in annotations.get_annotations(0.2):
      try:
          A, B, score = str(ann).split(" -> ")[0], str(ann).split(" -> ")[1].split(" (score: ")[0], str(ann).split(" -> ")[1].split(" (score: ")[1].split(")")[0]
          dic[A] = {
              "link":B,
              "score":score
            }
          
      except:
          print('error annotation about ' + ann)
  return dic

def remove_urls(text):   
  text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)   
  return text

