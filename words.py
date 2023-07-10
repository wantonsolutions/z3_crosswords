import bz2
import pickle
from nltk.corpus import words

def download_and_save_english_dict():
    #check if the files exists
    import os
    if os.path.isfile("english_words.pickle"):
        return
    
    # print("Downloading english words")
    import urllib.request
    url = "https://downloads.skullsecurity.org/passwords/english.txt.bz2"
    urllib.request.urlretrieve(url, "english.txt.bz2")

    # print("Decompressing english words")
    with bz2.open("english.txt.bz2", "rb") as f:
        content = f.read()
    content = content.decode("utf-8")

    lines = clean_english_words_list(content.splitlines())


    words_of_length = get_words_of_length_dict(lines)
    with open("english_words.pickle", "wb") as f:
        pickle.dump(words_of_length, f)

    #remove bz2 file
    os.remove("english.txt.bz2")
    print("Done")


def clean_english_words_list(lines):
    output_lines=[]
    for line in lines:
        line = line.rstrip()
        if "'" in line:
            continue
        if "&" in line:
            continue
        if "." in line:
            continue
        if "-" in line:
            continue
        line = line.lower()
        output_lines.append(line)
    return output_lines

def get_english_word_of_length_list():
    download_and_save_english_dict()
    import pickle
    with open("english_words.pickle", "rb") as f:
        words_of_length = pickle.load(f)
    return words_of_length

def get_word_word_list():
    return words.words()

def get_words_of_length_dict(word_list):
    words_of_length = dict()
    for word in word_list:
        size = len(word)
        if size in words_of_length:
            row = words_of_length[size]
            row.append(word)
            words_of_length[size]=row
        else:
            new_line = []
            new_line.append(word)
            words_of_length[size] = new_line
    return words_of_length

def get_english_words_dict_of_length(n):
    english_words = get_english_word_of_length_list()
    return english_words[n]
