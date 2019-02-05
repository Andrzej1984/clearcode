from bs4 import BeautifulSoup
import requests

def crawler(url):

    title = []
    links = []
    try:
        seurce_code = requests.get(url)
        plain_text = seurce_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        for x in soup.find('title'):
            b = x.string
            title.append(b)
    except:

        return
    try:
        for link in soup.findAll('a'):
            href = link.get('href')
            links.append(href)
    except:
        links.append("No links here")
        return title, links

    return title, links

def site_map(url):

    readylinks=[]
    alllinks=[]
    alllinks.append(url)
    alldata={}
    onelink={}

    while True:
        print("Pętla...")
        if not alllinks:
            print("Wynik", alldata)
            break
        buf = []

        for i in alllinks:
            test = i in readylinks

            #instrukcja zapobiegająca ponownemu mapowaniu linków, oraz wychodzenia poza obszar zadanego url
            if test==False and alllinks[alllinks.index(i)][:len(url)]== url:

                print("Trying crawl", i)
                next=crawler(i)
                if next:
                    # pełne linki dla podkatalogów
                    for item in next[1]:
                        if item != "":
                            if item[0] == '/':
                               next[1][next[1].index(item)] = url + item

                    onelink['title']=set(next[0])
                    onelink['links']=set(next[1])
                    alldata[i]=onelink
                    print(alldata)

                    #przygtowanie linków do następnej iteracji
                    for k in next[1]:
                        buf.append(k)


                #oznaczenie linków które już były
                readylinks.append(i)
        alllinks.extend(buf)

        for z in buf:
            if z in readylinks:
                buf.remove(z)

        alllinks=buf

    return alldata


site_map('http://localhost:8000')

