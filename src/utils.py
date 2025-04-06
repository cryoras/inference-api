import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
# import skimage
from PIL import Image
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import requests
import os
import time


def cleaningText(t):
  t = re.sub(r'[0-9]+', '', t)
  t = re.sub(r'[^\w\s]', '', t)
  t = t.replace('\n', ' ') 
  t = t.translate(str.maketrans('', '', string.punctuation)) 
  t = t.strip(' ')
  return t

def caseFold(t):
  t = t.lower()
  return t

def tokenizeText(t):
  t = word_tokenize(t)
  return t

def filteringText(text):
    listStopwords = set(stopwords.words('indonesian'))
    listStopwords1 = set(stopwords.words('english'))
    listStopwords.update(listStopwords1)
    listStopwords.update(['iya','yaa','gak','nya','na','sih','ku',"di","ga","ya","gaa","loh","kah","woi","woii","woy"])
    filtered = []
    for txt in text:
        if txt not in listStopwords:
            filtered.append(txt)
    text = filtered
    return text

def toSentence(list_words):
  sentence = ' '.join(word for word in list_words)
  return sentence

lang_dict = {
    # Istilah darurat tidak baku
    "gempa": "gempabumi",
    "gempa tektonik": "gempabumi",
    "gempa bumi": "gempabumi",
    "banjir bandang": "banjir",
    "longsor": "tanah longsor",
    "tsu": "tsunami",
    "angin puting": "angin puting beliung",
    "kebakaran hutan": "karhutla",

    # Singkatan darurat
    "bpbd": "Badan Penanggulangan Bencana Daerah",
    "posko": "posko bencana",
    "pengungsi": "korban terdampak",
    "mksd": "maksud",
    "jln": "jalan",

    # Ekspresi populer
    "wih": "waduh",
    "parah": "berat",
    "kacau": "rusak parah",
    "gede": "besar",
    "ampe": "sampai",
    "bnyk": "banyak",
    "krn": "karena",
    "yg": "yang"
}

def fix_slangwords(text):
    words = text.split()
    fixed_words = []

    for word in words:
        if word.lower() in lang_dict:
            fixed_words.append(lang_dict[word.lower()])
        else:
            fixed_words.append(word)

    fixed_text = ' '.join(fixed_words)
    return fixed_text


tfidf_vectorizer = joblib.load('./src/tfidf.joblib')
def tfid(text):
    return tfidf_vectorizer.transform([text]).toarray()

path = "bucket"
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(path, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        return filepath, True
    else:
        return None , False


def getImg(link:str):
    res = requests.get(link)
    if res.status_code == 200:  # Cek apakah request berhasil
      with open("downloaded_image.png", "wb") as file:
        file.write(res.content)
      print("Gambar berhasil didownload!")
      return True
    else:
      print("Gagal mendownload gambar.")
      return False



def clean_old_files():
    while True:
        current_time = time.time()
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # Dapatkan waktu modifikasi file
            file_time = os.path.getmtime(filepath)
            # Hapus jika lebih dari 10 menit (600 detik)
            if current_time - file_time > 600:
                try:
                    os.remove(filepath)
                    print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")
        # Tunggu 1 menit sebelum cek lagi
        time.sleep(60)

def preprocess_image(image_path, target_size=(150, 150,1)):
    img = load_img(image_path, color_mode='grayscale',target_size=target_size)
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array