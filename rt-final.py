import requests
import os
import subprocess
import json
import wget
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from os.path import basename
import time
from functools import partial

start_time = time.clock()

baseUrl = r"https://www.rtbookreviews.com"
basePath = r"E:\some books\studyyyy\New folder\RTbookreviews\\"



 
def download(link,session):
    try:
        response = session.get(link, stream=True)
        handle = open(basePath + str(basename(link)).replace('?','_')+".html", "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
    except Exception as e:
        print (e)
        print (link)
    return True



   
def main():
    postData = {
    'name': 'xxxxxxx',
    'pass': 'xxxxxxx',
    'form_id': 'user_login',
    'op': 'Log in'
    }
    
    loginUrl = 'https://www.rtbookreviews.com/user/login'

    session = requests.Session()
    response = session.post(loginUrl, data=postData)

    final_download_list = []
    with open(basePath + "dump1.txt","r")as f:
        final_download_list = json.load(f)
    x = input()
    
    with Pool(3) as p:
     results = p.map(partial(download,session = session), final_download_list)

    print("--- %s seconds ---" % (time.clock() - start_time))

if __name__ == '__main__': main()
