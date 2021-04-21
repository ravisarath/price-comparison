from flask import Flask,request, url_for, redirect, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import pprint
import smtplib
from email.message import EmailMessage
import csv
import schedule
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("distribution/index.html")
x = 1
y=1

prdct ={
    "samsung-198-l-direct-cool-single-door-5-star-refrigerator-base-drawer":{
        "flipcart":"itm1f53955cd314c",
        "amazon":"B08445PP98"
    },
    "hp-hpud032-1u1-c-32-gb-microsd-card-class-10-100-mb-s-memory":{
        "flipcart":"itmff84zjzfkxph3",
        "amazon":"B07DJLFMPS"
    },
    "sandisk-ultra-128-gb-microsdxc-uhs-class-1-120-mb-s-memory-card":{
        "flipcart":"itm4f68e47181a34",
        "amazon":"B08L5DBMMS"
    },
    "sandisk-ultra-dual-drive-3-0-otg-64-gb-pen":{
        "flipcart":"itmfgg2vfawxcdjd",
        "amazon":"B01N6LU1VF"
    }
}


@app.route('/price',methods=['POST','GET'])
def input():

    url = request.form['productid']
    flipid = prdct[url]["flipcart"]
    amazonid = prdct[url]["amazon"]
    amazon = f"https://www.amazon.in/dp/{amazonid}"
    print(amazon)
    flipcart = f"https://www.flipkart.com/{url}/p/{flipid}"
    print(flipcart)
    global x
    if "flipkart" in flipcart.lower() :
        print("Flipkart:\n")
        res = requests.get(f'{flipcart}')
        
        soup = BeautifulSoup(res.text,'html.parser')
        try:
            flipkartname = soup.select('.B_NuCI')[0].getText()
            flipkartprice = soup.select('._30jeq3')[0].getText()
            #flipkartprice = int(flipkartprice[1:].replace(",",""))
        except Exception as e:
            print(e)
            flipkartname = "not available"
            flipkartprice = "not available"
        print(flipkartname,flipkartprice)
    if "amazon" in amazon.lower():
        print("Amazon:\n")
        res = requests.get(amazon,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        try:
            amazonname = soup.select("#title")[0].getText().strip()
            try:
                amazonprice = soup.select("#priceblock_dealprice")[0].getText().strip()
            except:
                amazonprice = soup.select("#priceblock_ourprice")[0].getText().strip()
            #amazonprice_num = amazonprice.replace("₹","")
            #amazonprice_num = amazonprice_num.replace(",","")
            #amazonprice = int(float(amazonprice_num))
        except Exception as e:
            print(e)
            amazonname = "not available"
            amazonprice = "not available"
        print(amazonname,amazonprice)
    return jsonify({"flipkart": {"flipkartname":flipkartname,"flipkartprice":flipkartprice}, "amazon": {"amazonname":amazonname, "amazonprice":amazonprice}})
    
    

  
if __name__ == '__main__':
    app.run(debug=True, port=3000)


