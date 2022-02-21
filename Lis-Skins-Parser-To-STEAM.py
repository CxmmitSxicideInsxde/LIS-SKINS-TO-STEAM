from bs4 import BeautifulSoup
import requests
import json
from alive_progress import alive_bar
import time
import re
from fake_useragent import UserAgent
from steam_community_market import Market, AppID

market = Market("RUB")
ua = UserAgent()


def test():
    print('hello')
    url1 = 'https://steamcommunity.com/market/listings/730/'
    header = {'User-Agent': str(ua.random)}
    a = input('Nazvanie csgo skina')
    url2 = url1+a
    response = requests.get(url2, headers=header)
    print(re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(response.content)))
    #print(url2)
    print(response.status_code)

def lis_skins_parse():
    url = input('Вставьте ссылку для парса!\n')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    qoutes = soup.find_all('img', class_='image')
    prices = soup.find_all('div', class_='price')
    pricelis = []
    namelis = []
    for qoute in qoutes:
        qoute = qoute.get('alt', '')
        namelis.append(qoute)

    for price in prices:
        pricelis.append(float(price.text.replace(' ', '')))
    print('Перешли на 2 шаг | Получаем цену стима\n')
    test1(namelis, pricelis)
    
def test1(namelis, pricelis):
    a = []
    a = namelis
    steamprice = []
    volume = []
    with alive_bar(len(namelis), force_tty=True) as bar:
        for i in range(0, len(namelis)):
            req = market.get_lowest_price(a[i], 730)
            vol = market.get_volume(a[i], 730)
            if (vol is not None):
                print(vol)
                volume.append(vol)
            else: 
                vol = 0.0
                volume.append(vol)
            if (req is not None):
                req = ''.join(filter(lambda i: i.isdigit() or i == ',', req)).replace(',', '.')
                print(req)
                steamprice.append(req)
                time.sleep(4)
            else:
                req = 0.0
                steamprice.append(req)
                time.sleep(4)
            bar()
        print("Отправили на проверку!\n")
        check_this(namelis, steamprice, pricelis, volume)

def check_this(namelis, steamprice, pricelis, volume):
    print("\n")
    percentproffit = []
    minusfees = []
    for i in range(0, len(namelis)):
        minusFee = float(float(steamprice[i]) * 0.8696)
        minusfees.append(str(minusFee))
        percentage = float((minusFee / float(pricelis[i]) * 100 - 100))
        percentproffit.append(str(percentage))
        if (percentage >= 40 and percentage <= 80):
            print(f"High[{i}] {namelis[i]} : LPrice = {pricelis[i]} | SPrice = {steamprice[i]} | SPriceFee = {minusfees[i]} | Proffit[{percentproffit[i]}] | Volume[{volume[i]}]")
        elif (percentage >30 and percentage <= 39):
            print(f"Medium[{i}] {namelis[i]} : LPrice = {pricelis[i]} | SPrice = {steamprice[i]} | SPriceFee = {minusfees[i]} | Proffit[{percentproffit[i]}] | Volume[{volume[i]}]")
        else:
            print(f"Low[{i}] {namelis[i]} : LPrice = {pricelis[i]} | SPrice = {steamprice[i]} | SPriceFee = {minusfees[i]} | Proffit[{percentproffit[i]}] | Volume[{volume[i]}]")
    e = input('Press any key for close program!')

def main():
    lis_skins_parse()

if __name__ == '__main__':
    main()