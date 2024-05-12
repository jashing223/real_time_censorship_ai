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

def main():
    with open("uma.txt", "r", encoding="utf-8") as fr:
        with open("edited_uma.txt","w",encoding="utf-8") as fw:
            for line in fr.readlines():
                line = line.split("\t") #name #height #b #w
                name = line[0]
                height = int(line[1].strip('㎝'))
                b = int(line[2])
                w = int(line[3])
                fw.write(f"{name} {height} {b} {w} {cup_transform(height,b,w)}\n")
            
main()