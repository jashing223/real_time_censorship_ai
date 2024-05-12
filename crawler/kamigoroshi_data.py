import requests
from bs4 import BeautifulSoup

def cup_transform(height, b, w):
    #http://negifukyu.x.fc2.com/bustcheck/cupchecker.html
    #バスト：身長の0.54倍と比較して、2.5cm大きい毎に、カップ数＋１。
    #ウエスト：身長の0.38倍と比較して、3.42cm細い毎に、カップ数＋１。
    #身長：158.8と比較して、23cm(身長補正が『３べーだ！』だと、7.67cm)大きい毎に、カップ数＋１。
    cup_temp = 4 #D
    cup_temp += (b - height*0.54)/2.5
    cup_temp += (height*0.38 - w)/3.42
    cup_temp += (height - 158.8)/23
    if cup_temp <=1:
        return "A"
    return chr(64+round(cup_temp))

def get_img(name: str):
    img_r = requests.get(f"https://kamigoroshi-aria.wikiru.jp/index.php?plugin=attach&refer={name}&openfile={name}.jpg")
    with open(f"./kamigoroshi_dataset/{name}.png", "wb") as fwb:
        fwb.write(img_r.content) 

r = requests.get("https://kamigoroshi-aria.wikiru.jp/index.php?%E3%82%B9%E3%83%AA%E3%83%BC%E3%82%B5%E3%82%A4%E3%82%BA%E4%B8%80%E8%A6%A7")
soup = BeautifulSoup(r.text, "html.parser")
row_list = soup.find("table",id="sortabletable1").find("tbody").find_all("tr")
for row in row_list:
    row = row.find_all("td")
            #name                   #height  #b     #w
    get_img(row[2].text)
    print(f"{row[2].text} done")
    
