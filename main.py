import requests
import json
import cfscrape


def define(fiat, type, amount, main_asset, paytype,rows):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    data = {
        "asset": main_asset,
        "fiat": 'RUB',
        "merchantCheck": True,
        "page": 1,
        "payTypes": paytype,
        "publisherType": None,
        "rows": rows,
        "tradeType": type,
        "transAmount": amount
    }
    r = requests.post(url, headers=headers, json=data)
    r = json.loads(r.text)
    return r


def payment_method_def(method):
    all_method = ""
    for i in method:
        all_method += i + ' '
    return all_method


def process_request(r, fiat, order_type, main_asset):
    seller_list = []

    order_var = order_type
    entity = "Request"
    if order_var == "BUY":
        entity = "Buyer"
    else:
        entity = "Seller"

    for i in r['data']:
        seller = []
        method = []
        seller.append(i['adv']['price'])
        seller.append(i['adv']['surplusAmount'])
        seller.append(i['adv']['minSingleTransAmount'])
        for k in i['adv']['tradeMethods']:
            method.append(k['payType'])
        seller.append(method)
        seller.append(i['advertiser']['nickName'])
        seller.append(i['advertiser']['userNo'])
        seller.append(i['adv']['dynamicMaxSingleTransAmount'])
        seller_list.append(seller)

    for i in range(len(seller_list)):
        print(
            f"{i + 1}. {main_asset}/{fiat} {seller_list[i][0]}.   {entity}: {seller_list[i][4]}.   Payment method: {payment_method_def(seller_list[i][3])}.   Available: {seller_list[i][1]} {main_asset}.   Limits:  {seller_list[i][2]} - {seller_list[i][6]} {fiat}")
    #print(seller_list)
    # try:
    #   eleccion = int(input("Enter number (ENTER payers) : "))-1
    #  webbrowser.open("https://p2p.binance.com/es/advertiserDetail?advertiserNo="+seller_list[eleccion][3], new=2, autoraise=True)
    # except:
    #   return


def main():
    assets =["USDT","BTC"]
    main_asset = "USDT"
    fiat = "RUB"
    type = "SELL"
    paytype_all = None
    paytype_bank = ["Tinkoff"]
    amount = "0"
    usdrub = 61.5
    rows =2

    '''all_sellers = []
    for i in range(len(assets)):
        all_sellers.append(define(fiat, type, amount, assets[i], paytype_all,rows))'''

    all_sellers = define(fiat, type, amount, main_asset, paytype_all,rows)
    print(all_sellers)

    process_request(all_sellers, fiat, type, main_asset)
#'surplusAmount': '548.60 'minSingleTransAmount': '500.00' 'dynamicMaxSingleTransAmount': '33856.31'

if __name__ == "__main__":
    main()
