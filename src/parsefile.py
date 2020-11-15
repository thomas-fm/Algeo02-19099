from bs4 import BeautifulSoup
import codecs

""" Membaca isi dokumen html """
def htmlParser(filename):
  html_doc = codecs.open("./static/docs/" + filename, "r", "utf-8")
  soup = BeautifulSoup(html_doc, 'html.parser')

  return soup.get_text()