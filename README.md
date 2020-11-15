# Algeo02-19099
# ABCDE SEARCH-ENGINE
> Search engine berbasis web memanfaatkan aplikasi dot product

## Setup

### Pastikan sudah terinstall python dan pip
Cek versi dari python dan pip
```bash
python --version
pip --version
```
Apabila belum terinstall maka install terlebih dahulu python dan pip \
Visit https://www.python.org/downloads/ \
Visit https://pip.pypa.io/en/stable/installing/ 

### Install virtual environment
```bash
pip install virtualenv
```

### Clone repository
```bash
git clone https://github.com/thomas-fm/Algeo02-19099.git
```

### Buat virtual environment baru
Masuk ke folder src
```bash
cd src
```
Pastikan sudah di /src/ lalu buat env
```bash
virtualenv env
```

### Aktifkan virtual environment
* MacOS / Linux
```bash
source env/bin/activate
```
* Windows
```bash
env\Scripts\activate
```
Lalu command line akan terlihat seperti ini
```bash
(env) path/to/repo/Algeo02-19099/src
```

## Install library
Install library-library yang dibutuhkan
```bash
pip install -r requirement.txt
```

### Jalankan web
Menjalankan web secara lokal
```bash
flask run
```
