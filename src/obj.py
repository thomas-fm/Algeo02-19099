import math
import parsefile
import re
import calculation
import pandas as pd

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

class Dokumen:

  def __init__(self, filename):
    self.filename = filename

  def ProsesFile(self, dfDatabase):
    # Melakukan pembacaan dan pemrosesan file, fungsi stem mengembalikan array of string
    self.stem = calculation.stemm(self.filename)
    self.count_words = [0 for i in range (len(dfDatabase))]

    # Iterasi per kata dalam stem, apabila belum pada dfDatabase maka append, lalu isi jumlah kata dengan 1
    # Apabila sudah ada, maka jumlah kata ditambah 1
    for i in range(0, len(self.stem)):
      ada = False
      for index, row in dfDatabase.iterrows():
        if (row['term']==self.stem[i]):
          ada = True
          self.count_words[index] += 1
          break

      if not ada:
          dfDatabase = dfDatabase.append({'term':self.stem[i]}, ignore_index=True)
          self.count_words.append(1)

    # Mengembalikan kalimat pertama pada teks
    self.first = calculation.firstSentences(self.filename)

    # Membentuk sebuah dict baru yang nantinya akan di tambahkan ke dataframe sebagai informasi dari dokumen yang telah dibaca
    self.data_info = {
        'name': self.filename,
        'title': self.filename.split('.')[0].replace('_', ' '),
        'vektor': self.count_words,
        'cos_sim': 0,
        'first_sentence': self.first,
        'count_words': int(len(self.stem))
    }
    self.vektor = self.count_words
    self.cos_sim = 0
    return dfDatabase

  def Name(self):
    return self.filename

  def Vektor(self, array):
    return self.vektor

  def cosSim(self):
    return self.cos_sim

  def firstSentence(self):
    return self.first

  def dokumenInfo(self):
    return self.data_info

class CustomDf:
  def __init__(self, df):
    self.df = df
  
  # Membuka dataframe
  def openDf(self, path):
    self.df = pd.read_csv(path)
  
  # Membuat data frame baru dengan kolom
  def createDf(self, column):
    self.df = pd.DataFrame(columns=column)

  # Menambahkan data pada baris baru
  def insertfRowDf(self, data_dict):
    self.df = self.df.append(data_dict, ignore_index = True)

  # Menyimpan ke dalam csv
  def save(self, path):
    self.df.to_csv(path, index=False)
  
  # Mengupdate dataframe dengan database
  def updateDf(self, database):
    self.df = database

  # Mengembalikan dataframe
  def getDf(self):
    return self.df

class Query:
  def __init__(self, query):
    self.query = query

  # Meminimalisai term pada query
  def termQuery(self):
    # Melakukan stem dan penghapusan stopwords pada query dan menyimpan dalam token
    stemQuery = calculation.stemText(self.query)
    self.vektor_query = calculation.token(stemQuery)
    
    vektor_q = self.vektor_query
    self.vektor_query = list(dict.fromkeys(vektor_q))

    self.count_query = [0 for i in range(len(self.vektor_query))]
    
    for i in range (0, len(self.vektor_query)):
      for j in range (0, len(vektor_q)):
        if (vektor_q[j] == self.vektor_query[i]):
          self.count_query[i] += 1
    
    #print(self.vektor_query)
  # Mencari jumlah kemunculan query pada tiap dokumen
  def countQuery(self, dfdatabase):
    self.count_words_query = [0 for i in range(len(dfdatabase))]
    for i in range (len(self.vektor_query)):
      ada = False
      for index, row in dfdatabase.iterrows():
        if (self.vektor_query[i]==row['term']):
          self.count_words_query[index] += 1
          ada=True
          break
    
      if not ada:
        self.count_words_query.append(1)
        dfdatabase = dfdatabase.append({'term':self.vektor_query[i]}, ignore_index=True)

  # Menghitung kemiripan masing-masing dokumen
  def cosSim(self, dfQ, dfDatabase):
    self.termQuery()
    self.countQuery(dfDatabase)
    # Untuk mengisi tabel term query
    dfQTerm1 = pd.DataFrame({'term': self.vektor_query,'query': self.count_query})
    
    # Inisiasi dataframe kosong
    dfQTerm2 = pd.DataFrame()
    array_cos = []
    QTerm = [] # jumlah term dari tiap dokumen
    
    # Mengambil informasi dari setiap dokumen yang ada
    for index, row in dfQ.iterrows():
      # Ubah array yang tersimpan sebagai string ke integer
      arr = calculation.stringToInt(row['vektor'])
      arrQ = [0 for i in range (len(self.vektor_query))]

      # Hitung similarity dan append ke dfQ
      cos_sim = round(calculation.cosineSimilarity(self.count_words_query, arr), 2)
      row['cos_sim'] = cos_sim
      
      array_cos.append(cos_sim)

      # Masukkan ke arrQ
      for i in range (0, len(self.vektor_query)):
        for j in range (0, len(arr)):
          if (dfDatabase.at[j, 'term'] == self.vektor_query[i]):
            arrQ[i] = (int(arr[j]))

      x = [row['name'], arrQ]
      QTerm.append(x)

    # Isi value
    for i in dfQ.index:
      dfQ.at[i, "cos_sim"] = array_cos[i]

    # Sort dataframe dari cos_sim terbesar
    dF_sort = dfQ.sort_values(by=["cos_sim"],  ascending=False)

    # Kalau cos_sim = 0 maka tidak ditampilkan ke layar
    for index, row in dF_sort.iterrows():
      if row['cos_sim'] == 0:
        dF_sort.drop(index, inplace=True)
        continue
      for array in QTerm:
        if array[0] == row['name']:
          dfQTerm2[row['name']] = array[1]
      
    # Concat tabel term query dengan term dokumen
    idx = 0
    new_col = dfQTerm1['query']   
    dfQTerm2.insert(loc=idx, column='query', value=new_col)
    new_col = dfQTerm1['term'] 
    dfQTerm2.insert(loc=idx, column='term', value=new_col)
    
    self.dfTerm = dfQTerm2

    dfQout = dF_sort
    return dfQout

  # Mengembalikan vektor term
  def getTerm(self):
    return self.dfTerm

  def getVektor(self):
    self.termQuery()
    return len(self.vektor_query)
