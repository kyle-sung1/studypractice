import requests
import random
from bs4 import BeautifulSoup
import html2text
import re

#studies = ["cohort studies", "cross-sectional studies", "case-control studies"]
#randomStudy = random.choice(studies)

headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Content-Type': 'text/plain;charset=UTF-8',
'Origin': 'https://www.google.com',
'Referer': 'https://www.google.com/',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

class Study:
    def __init__(self, type, link):
        self.type = type
        self.link = link

def randomStart():
    """
    Returns random integer between 0 and 40 as a string
    """
    start = str(random.randint(0,40))
    return start

def sendRequests(studyType):
    """
    Scrapes Google Scholar for links, sends request to link, scrape abstract, then print abstract, then asks users to guess
    """
    cohort = "https://scholar.google.com/scholar?start=" + randomStart() + "&q=cohort+study&hl=en&num=20&as_sdt=0,22"
    xSectional = "https://scholar.google.com/scholar?start=" + randomStart() + "&q=cohort+study&hl=en&num=20&as_sdt=0,22"
    caseControl = "https://scholar.google.com/scholar?start=" + randomStart() + "&q=cohort+study&hl=en&num=20&as_sdt=0,22"

    cohort = "https://pubmed.ncbi.nlm.nih.gov/?term=cohort+study&size=50"
    xSectional = "https://pubmed.ncbi.nlm.nih.gov/?term=a+cross+sectional+study&size=50"
    caseControl = "https://pubmed.ncbi.nlm.nih.gov/?term=a+case+control+study&size=50"

    if studyType == "cohort":
        response = requests.get(cohort, headers = headers)
    elif studyType == "cross-sectional":
        response = requests.get(xSectional, headers = headers)
    elif studyType == "case-control":
        response = requests.get(caseControl, headers = headers)


    """for item in soup.select('[data-lid]'):
        try:
            item = str(item)
            index = item.index("href")
            item = item[index+6:]
            index = item.index('"')
            item = item[:index]
            linkList.append(item)
        except Exception as e:
    		#raise e
            print('error no link')
    for study in linkList:
        if "pdf" in study:
            linkList.remove(study)"""

    cohort = "https://pubmed.ncbi.nlm.nih.gov/?term=cohort+study&size=10"
    response = requests.get(cohort, headers = headers)
    soup = BeautifulSoup(response.content,'lxml')
    #myarticles = soup.find_all("article", {"class": "full-docsum"})
    myarticles = soup.select('article[class=full-docsum]')
    linkList = []
    for item in myarticles:
        item = str(item)
        index = item.index("href")
        item = item[index+6:]
        index = item.index('"')
        item = item[:index]
        linkList.append("https://pubmed.ncbi.nlm.nih.gov" + item)



    return Study(studyType, linkList)


def getHTML(study):
    """
    sends request to study, returns html but with study type censored
    """
    response = requests.get(study, headers=headers)
    soup = BeautifulSoup(response.content,'lxml')
    abstract = str(soup.find("div", {"id": "enc-abstract"}))
    cleanr = re.compile('<.*?>')
    cleanAbstract = re.sub(cleanr, '', abstract)
    return str(cleanAbstract)

def main(n):
    """
    Main function that asks users for inputs then compares it to right answer
    """
    study1 = sendRequests("cohort")
    study2 = sendRequests("case-control")
    study3 = sendRequests("cross-sectional")
    studyList = (study1, study2, study3)
    for i in range(n):
        randomStudy = random.choice(studyList) # Study object
        rand = random.choice(randomStudy.link)
        abstract = getHTML(rand)
        # display the html
        #text = html2text.html2text(html)
        print(abstract.replace(randomStudy.type, "_________"))
        guess = input("What study is this? (cohort, CC or XS)")
        if guess == randomStudy.type:
            print("Correct")
            print("------------------------------------------------")
        else:
            print("oops")
            print(randomStudy.type)
            print("------------------------------------------------")
#scrape should not include pdfs
#and should not include ones without abstract


if __name__ == '__main__':
    #sendRequests()
    """c1 = Study("cohort", ["www.google.com", "www.bing.com"])
    c2 = Study("XS", ["www.yahoo.com", "www.gmail.com"])
    c3 = Study("CC", ["www.spotify.com", "www.apple.com"])
    print(c1.type, c1.link)
    studyList = (c1, c2, c3)
    print(studyList)
    randomStudy = random.choice(studyList)
    print(randomStudy)"""
    #print(getHTML("https://pubmed.ncbi.nlm.nih.gov/19690438/"))
    main(3)
    #print(myarticles)
