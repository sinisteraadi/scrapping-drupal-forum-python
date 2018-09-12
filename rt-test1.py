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

final_download_list = []


def getThemeTopics(session):
    baseThemeUrl = r"/forums/theme-spotlights"
    fetchUrl = baseUrl + baseThemeUrl
    page = session.get(fetchUrl)
    
    html_page = page.text
    soup = BeautifulSoup(html_page,'lxml')
    pages = [ a['href'] for a in soup.find_all('a', href=True) if 'page='in a['href']]

    results = int("".join(filter(str.isdigit, pages[-1])))
    allPages = [fetchUrl+"?page="+str(x) for x in range(0,results+1)]
    final_download_list.extend(allPages)
    allTopics = []
    for p in allPages:
        pp = session.get(p)
        html_pp = pp.text
        sp = BeautifulSoup(html_pp, 'lxml')
        pageTopics = [a['href'] for a in sp.find_all('a', href=True) if 'forum-topic' in a['href'] and 'page=' not in a['href']]
        allTopics.extend(set(pageTopics))
        

    final_download_list.extend(allTopics)
    print("--- %s seconds ---" % (time.clock() - start_time))
    return allTopics

     
def fetchTopics(allTopics, session):
    for topic in allTopics:
        topicUrl = baseUrl + topic
        page = session.get(topicUrl)
    
        html_page = page.text
        soup = BeautifulSoup(html_page,'lxml')
        topicPages = []
        pages = [ a['href'] for a in soup.find_all('a', href=True) if 'page='in a['href']]
        if pages:
            results = int("".join(filter(str.isdigit, pages[-1])))
            topicPages = [topicUrl +"?page="+ str(x) for x in range(0,results+1)]
            final_download_list.extend(topicPages)
        else:
            final_download_list.append(topicUrl)

        
        print("--- %s seconds ---" % (time.clock() - start_time))
 
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
    'name': 'xxxxxxxxxx',
    'pass': 'xxxxxxxxxx',
    'form_id': 'user_login',
    'op': 'Log in'
    }
    
    loginUrl = 'https://www.rtbookreviews.com/user/login'

    session = requests.Session()
    response = session.post(loginUrl, data=postData)

    allTopics = getThemeTopics(session)
    fetchTopics(allTopics, session)
    
    print (len(final_download_list))
    with open(basePath + "dumpfile1.txt","w")as f:
        json.dump(final_download_list,f)
    
    with Pool(3) as p:
     results = p.map(partial(download,session = session), final_download_list)

    print("--- %s seconds ---" % (time.clock() - start_time))

if __name__ == '__main__': main()
