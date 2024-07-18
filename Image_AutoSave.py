from bs4 import BeautifulSoup
from urllib import parse
import urllib.request
import re
import time
import datetime
import os

opener = urllib.request.build_opener() # Request Header 추가 (Bot 차단 방지)
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]
urllib.request.install_opener(opener)

slideURL = []

def main():
    print("----------------------------")
    print("- Article Image Downloader -")
    print("----------------------------\n")
    print("Enter the URL of the article:")
    articleURL = input()
    time.sleep(0.5)
    print("\n------------------------------\nTrying to get image URL from given article URL...\n")
    time.sleep(1)
    imageURL = []
    start = time.time()
    if (articleURL.find("wccftech", 0) != -1): # wccfTech 기사인 경우
        imageURL = WCCFTech(articleURL) 
    elif (articleURL.find("videocardz", 0) != -1): # videoCardz 기사인 경우
        imageURL = videoCardz(articleURL)
    else:
        print("!- Do not recognize article sources. Please check article URL -!\n")
        exit(-1)
    cnt = imageURL.pop() # 전체 이미지 개수
    print("  - Total number of Images: " + cnt)
    time.sleep(1)
    print("\nTrying to download article image...\n")
    if (len(slideURL) == 0): # 슬라이드 형태로 삽입된 이미지가 없을 경우 (에러 방지)
        slideURL.append("-1")
    failed = saveImage(imageURL, cnt) # 저장 실패 이미지 개수
    end = time.time()
    sec = end - start
    time.sleep(1)
    print("\n---------------------")
    print("- [Download Result] -")
    print("---------------------")
    print(" - Downloaded Successfully: " + str(int(cnt) - failed))
    print(" - Download Failed: " + str(failed))
    print(" - Time taken to download: " + str(datetime.timedelta(seconds=sec)).split(".")[0])
    time.sleep(1)
    print("\nCompleted!\n")
    os.system("pause")


def WCCFTech(articleURL): # for WCCFTech / article URL 을 받아서, content 에 포함된 이미지 개수와 원본 URL return
    try:
        imageURL = []
        req = urllib.request.Request(url = articleURL)
        html = urllib.request.urlopen(req)
        source = html.read()
        origin = BeautifulSoup(source, 'html.parser')
        soup = origin.find("div", "post-cover") # 커버이미지
        imgURL = soup.find_all("img")
        for url in imgURL:
            url = url.attrs['src']
            url = re.sub("-[0-9]{3,4}x[0-9]{3,4}", "", url) # 특정 크기로 Resize 된 이미지의 원본 URL 추출.
            imageURL.append(url)
        soup = origin.find("div", "post") # 본문이미지
        imgURL = soup.find_all("img")
        for url in imgURL: # URL로부터 HTML 구조 읽어와서, img 링크만 추출
            url = url.attrs['src']
            url = re.sub("-[0-9]{3,4}x[0-9]{3,4}", "", url) # 특정 크기로 Resize 된 이미지의 원본 URL 추출.
            imageURL.append(url)
        imageURL.append(str(len(imageURL))) # 페이지의 전체 이미지 개수를 저장.
        imgURL = origin.select("figure.story-gallery > div > div > div") # 슬라이드 형태로 삽입된 이미지 링크 추출
        for url in imgURL:
            url = url.find("img")
            if (url is not None):
                url = url.attrs['src']
                url = re.sub("-[0-9]{3,4}x[0-9]{3,4}", "", url)
                slideURL.append(url)
        print("Getting URL Successfully!\n  - Article Sources: WCCFTech")
        return imageURL
    except: # Image URL 추출 실패
        print("Failed to getting image URL. Please check your internet connection and article URL.")
        exit(-1)

def videoCardz(articleURL): # for videoCardz / article URL 을 받아서, content 에 포함된 이미지 개수와 원본 URL return
    try:
        imageURL = []
        req = urllib.request.Request(url = articleURL)
        html = urllib.request.urlopen(req)
        source = html.read()
        soup = BeautifulSoup(source, 'html.parser')
        soup = soup.find("article")
        imgURL = soup.find_all("img")
        for url in imgURL: # URL로부터 HTML 구조 읽어와서, img 링크만 추출
            url = url.attrs['src']
            url = re.sub("-[0-9]{3,4}x[0-9]{3,4}", "", url) # 특정 크기로 Resize 된 이미지의 원본 URL 추출.
            imageURL.append(url)
        imageURL.append(str(len(imageURL)))
        print("Getting URL Successfully!\n  - Article Sources: VideoCardz")
        return imageURL
    except: # Image URL 추출 실패
        print("Failed to getting image URL. Please check your internet connection and article URL.")
        exit(-1)


def saveImage(imageURL, totalCnt): # 원본 이미지 URL을 받아, Root 디렉토리에 이미지를 저장.
    totalSaved = 0 # 저장된 이미지의 개수
    cnt = 0
    failed = 0 # 저장 실패 이미지 개수
    slideCnt = 0 # 현재 슬라이드의 이미지 중 저장된 것의 개수
    slideSaved = 0 # 직전 슬라이드까지 저장된 이미지 개수
    slideIdx = 0 # slideURL 배열의 idx
    beforeStatus = 0 # 0 -> Non-Slide / 1 -> In Slide
    extension = ""
    for url in imageURL:
        cnt += 1
        extension = url.split(".")[-1]
        url = url[8:]
        try: 
            if (slideURL[slideIdx][8:] == url):
                beforeStatus = 1
                fileName = str(cnt - slideCnt - slideSaved) + "-" + str(slideCnt + 1) + "." + extension
                urllib.request.urlretrieve("https://" + parse.quote(url), "./" + fileName)
                totalSaved += 1
                slideCnt += 1
                slideIdx += 1
                print(fileName + " | Downloading... [" + str(totalSaved) + " / " + str(totalCnt) + "]")
            else:
                if (beforeStatus):
                    cnt += 1
                    beforeStatus = 0
                    slideSaved += slideCnt
                    slideCnt = 0
                fileName = str(cnt - slideSaved) + "." + extension
                urllib.request.urlretrieve("https://" + parse.quote(url), "./" + fileName)
                totalSaved += 1
                print(fileName + " | Downloading... [" + str(totalSaved) + " / " + str(totalCnt) + "]")
        except:
            print("!- Download Failed! [" + str(totalSaved) + " / " + str(totalCnt) + "] -!")
            failed += 1
    return failed

main()