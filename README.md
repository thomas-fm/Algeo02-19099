# ABCDE SEARCH-ENGINE
> Search engine berbasis web memanfaatkan aplikasi dot product

## Anggota Kelompok
Thomas Ferdinand Martin - 13519099 \
Azmi Muhammad Syazwana - 13519151 \
Muhammad Rayhan Ravianda - 13519201 \

## Setup

### Pastikan sudah terinstall python dan pip
Cek versi dari python dan pip
```bash
python --version
pip --version
```
atau
```bash
python3 --version
pip3 --version
```
Apabila belum terinstall maka install terlebih dahulu python dan pip \
Visit https://www.python.org/downloads/ \
Visit https://pip.pypa.io/en/stable/installing/ 

### Install virtual environment
```bash
pip install virtualenv
```
atau
```bash
pip3 install virtualenv
```

### Clone repository
```bash
git clone https://github.com/thomas-fm/Algeo02-19099.git
```

### Buat virtual environment baru
Buka command line dan arahkan ke dalam folder src
```bash
cd /path/to/repo/Algeo02-19099/src
```
Pastikan sudah di /src/ lalu buat env
```bash
$ path/to/repo/Algeo02-19099/src> virtualenv env
```

### Aktifkan virtual environment
* MacOS / Linux
```bash
$ path/to/repo/Algeo02-19099/src> source env/bin/activate
```
* Windows
```bash
$ path/to/repo/Algeo02-19099/src>env\Scripts\activate
```
Lalu command line akan terlihat seperti ini
```bash
$ (env) path/to/repo/Algeo02-19099/src
```

## Install library
Install library-library yang dibutuhkan
```bash
$ (env) path/to/repo/Algeo02-19099/src> pip install -r requirement.txt
```

### Jalankan flask
Menjalankan web secara lokal
```bash
$ (env) path/to/repo/Algeo02-19099/src> flask run
```
### Buka web
Biasanya web akan terbuka pada port 5000, buka link berikut
```bash
http://127.0.0.1:5000/
```
Apabila tidak bisa dibuka, salin link dari yang muncul pada cli
```bash
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Begini tampilan cli yang terlihat
