from bs4 import BeautifulSoup
import codecs

""" Membaca isi dokumen html """
def htmlParser(filename):
  html_doc = codecs.open("./static/docs/" + filename, "r", "utf-8")
  soup = BeautifulSoup(html_doc, 'html.parser')

  parse_string = []

  for i in range (0, len(soup.find_all('p'))):
    text = soup.find_all('p')[i].get_text()
  
    if (len(text.split(' ')) > 6 and '.' in text):
      parse_string.append(text)
  parse_string = ' '.join(parse_string)
  
  return parse_string

def htmlFirst(filename):
  html_doc = codecs.open("./static/docs/" + filename, "r")
  soup = BeautifulSoup(html_doc, 'html.parser')

  for i in range (0, len(soup.find_all('p'))):
    text = soup.find_all('p')[i].get_text()
  
    if (len(text.split('.')) > 3 and '.' in text):
      return text.split('.')[0]
  return None
