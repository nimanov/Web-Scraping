from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request
from time import sleep

turbo = 'https://turbo.az' #bizim esas saytimiz
filename = 'turbo_az.csv' #scrap elediyimiz data ni yazacagimiz filr
f = open(filename , "w+") #file create olunur
#headerlerimiz
headers = "Şəhər, Marka, Model, Buraxılış ili, Ban növü, Rəng, Mühərrikin həcmi, Mühərrikin gücü, Yanacaq növü, Yürüş, Sürətlər qutusu, Ötürücü, Yeni, Qiymət, Seller name, Seller contact, Shop name, Shop contact, Sayta qoyulma tarixi\n"
f.write(headers) #headerlerimizi file a yazirq

#Birinci for'da nece page scrap elemek isdediyimizi yaziriq
for i in range(1121):
    boolean = False #Boolean bir deyer gotuturem asagda isdifade eliyecem
    url = 'https://turbo.az/autos' #Bu butun elanlariin yerlesditildiyi seyfedir
    
    #Birinci seyfede page yazmaga ehtiyac yoxdur (saytin qurulusu beledir)
    if(i!=0):
        num_page = i + 1 #Ikinci seyfe page = 2 den baslayir bunu biz range(1,5) lede yaza bilerdik
        url = url + '?page=' + str(num_page) #Saytin qurulusuna uygun page i deyisdirmek
    
    #Burda sadece BeautifulSoup ile site a request gonderirik
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = uReq(req).read()
    page_soup = soup(webpage , 'html.parser')
    
    
    all_products = page_soup.findAll("div",{"class":"products"}) #bu mene butun prodoductlari verir
    only_thrid_one = all_products[2] #Mene ise 3 cu hisse lazim idi ki hamsi orda var
    elanlar= only_thrid_one.findAll("div",{"class":"products-i"})#Indi ise o elanlar hissedeki masinlari gotururem
    sayta_qoyulma_tarixi_class = only_thrid_one.findAll("div",{"class":"products-bottom"})#Sayita qoyulma tarixini gotururrem
  
    for j in range(len(elanlar)):
        #Her bir masina tek tek girmek
        sayta_qoyulma_tarixi = sayta_qoyulma_tarixi_class[0].text
        sayta_qoyulma_tarixi = sayta_qoyulma_tarixi.split(',')
        sayta_qoyulma_tarixi = sayta_qoyulma_tarixi[1]
        #Yalniz qoyulma tarixini goturerem 
        sayta_qoyulma_tarixi =str(sayta_qoyulma_tarixi)
    
        #linkin basi yox idi yerlesdirdim
        elan_url=elanlar[j].a['href']
        full_url = turbo + elan_url
        
        #Hemen linklere girirem
        req_for_each_elan = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        newWebpage = uReq(req_for_each_elan ).read()
        page_soup2 = soup(newWebpage , 'html.parser')
     
        
        
        
        seller_phone_class = page_soup2.findAll("div",{"class":"seller-phone"})
        seller_name_class = page_soup2.findAll("div",{"class":"seller-name"})
        if(seller_phone_class != [] and seller_name_class != []):
            boolean = True
            seller_phone = seller_phone_class[0].text
            seller_name = seller_name_class[0].text
            
            
        shop_phone_class =  page_soup2.findAll("a",{"class":"shop-contact--phones-number"})   
        shop_name_class = page_soup2.findAll("a",{"class":"shop-contact--shop-name"})
        if(shop_name_class != [] and shop_phone_class != []):
            shop_name = shop_name_class[0].text
            if(len(shop_phone_class)==1):
                shop_phone = shop_phone_class[0].text
            else:    
                for z in range(len(shop_phone_class)):
                    number = shop_phone_class[z].text
                    if(z == 0):
                        shop_phone = number + ","
                        continue
                        
                    if(z==(len(shop_phone_class)-1)):
                        shop_phone += number
                        continue
                    shop_phone += number + ","
                    
        
        
        products_properties = page_soup2.findAll("li",{"class":"product-properties-i"})
        
        for k in range(14):
            name= products_properties[k].div.text
            if(k==0):
                one_row = name + ","
                continue
            one_row += name + ","
        if(boolean):   
            one_row += seller_name + "," 
            one_row += seller_phone + ","
            one_row += "    Not Salon" + ","
            one_row += "    Not Salon" + ","
        else:
            one_row += "Not Owner" + "," 
            one_row += "Not Owner" + ","
            one_row += shop_name + ","
            one_row += shop_phone + ","
        one_row += sayta_qoyulma_tarixi + "\n"
            
        f.write(one_row)
    sleep(1)
            
f.close()