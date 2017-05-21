'''
Created on May 21, 2017

@author: vbera
'''
import sys
import os
import hashlib
import requests

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def request_sub(md5):
    url = "http://api.thesubdb.com/?action=download&hash=" + md5 + "&language=en"
    header = {'user-agent': 'SubDB/1.0 (DownloadSubtitle/0.1)'}
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        return r.content

def save_sub(data, filename):
    s_filename = filename[:-4] + ".srt"
    with open(s_filename, "wb") as s_f:
        s_f.write(data)
    print("Subtitle saved as:" + s_filename)
    
def downloadSubtitle(file):
    md5 = get_hash(file)
    print("Downloading subtitle for:" + file)
    data = request_sub(md5)
    if data != None:
        save_sub(data, file)
    else:
        print("Error while downloading subtitle for movie: " + file)

def listFiles(directory):
    file_paths = []
    for folder, _, files in os.walk(directory):
        for filename in files:
            file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    
    for file in file_paths:
        if os.path.isdir(file):
            listFiles(file)
        elif file.endswith('.mkv') or file.endswith('.avi') or file.endswith('.mp4'):
            downloadSubtitle(file) 
            
if len(sys.argv) > 1:
    print("Downloading subtitle for files in folder: " + sys.argv[1])
    listFiles(sys.argv[1])     
