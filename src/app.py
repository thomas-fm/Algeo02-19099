""" IMPORT LIBRARY """
import os
import json
import calculation
import pandas as pd 
import numpy as np 
import obj

from flask import Flask, render_template, url_for, request, redirect, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename

""" PATH DAN EKSTENSI FILE UPLOAD """
UPLOAD_FOLDER = "./static/docs/"
CSV_PATH = "./db/data.csv"
TERM_PATH = "./db/term.csv"
QTERM_PATH = "./db/qterm.csv"
ALLOWED_EXTENSIONS = {'txt', 'html'}

""" GLOBAL VARIABLE AS DATABASE """
global Filenames
global AllFiles
Filenames = []

""" FLASK THING """
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

""" FUNGSI MENGGENERATE NAMA FILE YANG AMAN """
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

""" INDEX ROUTE """
@app.route('/')
def index():
    return render_template('index.html')

""" UPLOADER ROUTE """
@app.route('/uploader')
def uploader():
    return render_template('upload.html')

""" UPLOAD FORM """
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Filenames = akan berisi array yang menampung nama-nama dokumen yang berhasil di upload
    global Filenames
    
    # Penyimpanan file
    if request.method == 'POST':
    
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('file')
        
        # Menyimpan file satu persatu, nama file diubag menjadi nama file yang aman
        for file in files:

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                """ MENGISI NAMA FILE YANG BERHASIL DISIMPAN """
                ada = False
                for name in Filenames:
                    if (name == filename):
                        ada = True
                        break
                if not ada:
                    Filenames.append(filename)

        return redirect(request.url)

    return render_template('upload.html')

""" QUERY ROUTE """
@app.route('/query')
def query():
    
    global Filenames

    # Mempersiapkan dataframe
    empty_df = pd.DataFrame()
    empty_dfDatabase = pd.DataFrame()
    
    df = obj.CustomDf(empty_df)
    dfDatabase = obj.CustomDf(empty_dfDatabase)

    df.createDf(['name', 'title','vektor', 'cos_sim','first_sentence','count_words'])
    df.createDf(['term'])

    # Membaca dokumen-dokkumen dan diisi ke dataframe
    for k in range (0, len(Filenames)):
        uploadDoc = obj.Dokumen(Filenames[k])
        data_term = dfDatabase.getDf()
        updateDatabase = uploadDoc.ProsesFile(data_term)
        
        df.insertfRowDf(uploadDoc.dokumenInfo())
        dfDatabase.updateDf(updateDatabase)

        # print(uploadDoc.dokumenInfo())

    # Save dataframe ke csv untuk kembali dibaca ketika web menerima sebuah query
    df.save(CSV_PATH)
    dfDatabase.save(TERM_PATH)
    return render_template('search.html')

""" SEARCH ROUTE """
@app.route('/search', methods=['GET', 'POST'])
def proses_file():

    global Filenames

    if request.method == 'POST':
        text = request.form['text']

        if text == '':
            flash("No text")
            return redirect(request.url)

        
        """ MASUKKAN QUERY KE DATABASE """
        empty_df = pd.DataFrame()
        
        dfDataTerm = obj.CustomDf(empty_df)
        dfDataTerm.openDf(TERM_PATH)
        
        dfQ = obj.CustomDf(empty_df)
        dfQ.openDf(CSV_PATH)
        
        query = obj.Query(text)
        if (query.getVektor()==0):
            return render_template('search.html')
        dfQout = query.cosSim(dfQ.getDf(), dfDataTerm.getDf())
        
        dict_dfQ = dfQout.to_dict('records')
        dfQTerm = query.getTerm()

        """ SAVE DATA """
        dfDataTerm.save(TERM_PATH)
        dfQ.save(CSV_PATH)
        dfQTermS = obj.CustomDf(dfQTerm)
        dfQTermS.save(QTERM_PATH)
        # Apabila term kosong
        print(dfQTerm)
        print(len(dfQTerm.index))

        # Apabila cos_sim kosong
        if (len(dict_dfQ)==0):
            return render_template('search.html')
        return render_template('result.html', data = dict_dfQ, column_names=dfQTerm.columns.values, row_data=list(dfQTerm.values.tolist()), zip=zip)

@app.route('/perihal')
def perihal():
    return render_template('perihal.html')

@app.route('/tentang-kami')
def tentang_kami():
    return render_template('tentang-kami.html')

@app.route('/cara-penggunaan')
def cara():
    return render_template('cara-penggunaan.html')

@app.route('/konsep-singkat')
def konsep():
    return render_template('konsep-singkat.html')

if __name__ == '__main__':
    app.run()