from bs4 import BeautifulSoup
import codecs

""" Membaca isi dokumen html """
def htmlParser(filename):
  html_doc = codecs.open("./static/docs/" + filename, "r", "utf-8")
  soup = BeautifulSoup(html_doc, 'html.parser')

  parse_string = []

  for i in range (0, len(soup.find_all('p'))):
    text = soup.find_all('p')[i].get_text()
  
    if (len(text.split(' ')) > 3 and '.' in text):
      parse_string.append(text)
  parse_string = ' '.join(parse_string)
  
  return parse_string

def htmlFirst(filename):
  html_doc = codecs.open("./static/docs/" + filename, "r")
  soup = BeautifulSoup(html_doc, 'html.parser')

  for i in range (0, len(soup.find_all('p'))):
    text = soup.find_all('p')[i].get_text()
  
    if (len(text.split('.')) > 2 and '.' in text):
      sentence = text.split('.')
      for j in range(0, len(sentence)):
        if (len(sentence[j].split(' ')) > 3):
          # print(sentence[j].split(' '))
          return text.split('.')[j].replace('com', '').replace(',', '')
  return None