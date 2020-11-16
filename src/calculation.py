import math
import parsefile
import re

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

""" Melakukan stemming pada teks dan penghapusan karakter tidak penting, parameter string """
def stemText(teks):
  # Stem teks
  factory2 = StemmerFactory()
  stemmer = factory2.create_stemmer()
  output = stemmer.stem(teks)
  # Hapus stopwords
  stop_factory = StopWordRemoverFactory().get_stop_words()
  
  dictionary = ArrayDictionary(stop_factory)
  str = StopWordRemover(dictionary)
  
  stop = str.remove(output)
  # Hapus karakter pada teks
  # ref = https://link.medium.com/yEtxO932Kab
  final_text = re.sub(r'[^\x00-\x7F]+', ' ', stop)
  final_text = re.sub(r'@\w+', '', final_text)
  final_text = final_text.lower()
  final_text = re.sub(r'[0-9]', '', final_text)
  final_text = re.sub(r'\s{2,}', ' ', final_text)
  # print(final_text)
  
  return final_text

""" Melakukan pembacaan file dengan nama filename dan ekstensi .txt dan mengubahnya menjadi string, parameter nama file"""
def readtextToString(filename):
  # PATH ADALAH
  with open("./static/docs/" + filename, 'r', encoding="utf8") as file:
    data = file.read().replace('\n', ' ')
  file.close()

  return data

""" Mengubah string teks, menjadi array of string dari, parameter string teks"""
def token(string):
  arrOfWords = string.split()
  return arrOfWords

""" Perhitungan dot product, X dan Y adalah array, salah array berupa karakter dan di casting ke int """
def dotProduct(X, Y):
  result = 0
  # X > Y
  for i in range (len(Y)):
    result += int(X[i]) * int(Y[i])
  
  return float(result)

""" Perhitungan besar vektor, parameter X adalah array of integer """
def distanceVektor(X):
  power = 0
  for i in range (len(X)):
    power += int(X[i]) * int(X[i])
  result = math.sqrt(float(power))

  return result

""" Perhitungan besar kemiripan menggunakan cosine similarity """
def cosineSimilarity(Q, D):
  if (distanceVektor(Q) == 0 or distanceVektor(D)==0):
    return None
  cos = float(dotProduct(Q, D)) / float(distanceVektor(Q) * distanceVektor(D))

  return cos*100

""" Program utuh stemming, penghapusan karakter dan tokenize, paramater nama file dapat berupa html maupun txt """
def stemm(filename):
  # TIPE TXT
  if (filename.split('.')[1] == 'txt'):
    text = readtextToString(filename)

    # Stemming
    stemmed_text = stemText(text)

    # Vectorize
    array_of_word = token(stemmed_text)

    return array_of_word
  
  # TIPE HTML
  elif (filename.split('.')[1] == 'html'):
    text = parsefile.htmlParser(filename)
    # Stemming
    stemmed_text = stemText(text)

    # Vectorize
    array_of_word = token(stemmed_text)

    return array_of_word
  else:
    return

""" Melakukan stemming dan penghapusan karakter dengan parameter teks dalam string, output array of words """
def stemm2(string):
  stemmed_text = stemText(string)

  array_of_word = token(stemmed_text)

  return array_of_word

""" Mencari kalimat pertama pada dokumen baik html atau txt """
def firstSentences(filename):
  # TIPE TXT
  if (filename.split('.')[1]=='txt'):
    content = open("./static/docs/" + filename, "r", encoding="utf8")
    lines = content.readlines()

    for line in lines:
      first_sentences = line.split('.')[0]
      break

    return first_sentences

  # TIPE HTML
  else:
    return parsefile.htmlFirst(filename)
  
""" Mengubah array yg disimpan ssebagai string di csv, kebentuk integer """
def stringToInt(array):
  x = array.replace('"', '').replace('[', '').replace(']','').replace(' ','')

  return x.split(',')
