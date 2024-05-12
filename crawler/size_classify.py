import os
import shutil
import requests
from bs4 import BeautifulSoup

size_map = {}

# size_map = {}
# r = requests.get("https://angelic.wikiru.jp/?%E3%83%90%E3%82%B9%E3%83%88%E3%82%B5%E3%82%A4%E3%82%BA%E9%A0%86%E4%B8%80%E8%A6%A7")
# soup = BeautifulSoup(r.text, "html.parser")
# full_table = soup.find_all("table",class_="style_table")[-1]
# chuck_data = full_table.find("tbody").find_all("tr")
# for chuck in [chuck_data[x] for x in range(0, len(chuck_data)-1, 2)]:
#     # size, charac_list
#     size_map[chuck.find("th",class_="style_th").text] = []
#     chracs = chuck.find_all("td",class_="style_td")[-1].find_all("a")
#     for chrac in chracs:
#         name = chrac['title']
#         size_map[chuck.find("th",class_="style_th").text].append(name)

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

def uma():
    with open("edited_uma.txt", "r", encoding="utf-8") as fr:
        for row in fr.readlines():
            row = row.split()
            size_map[row[0]] = row[4]
    for root, dirname, filenames in os.walk("./uma_dataset"):
        for filename in filenames:
            try:
                shutil.copyfile(f"./uma_dataset/{filename}", f"./breast_size/{size_map[filename.strip('.png')]}/{filename}")
                print(f"{filename} sucessfully replace")
            except Exception as e:
                print(e)

def angel():
    for size, charac_list in size_map.items():
        for charac in charac_list:
            try:
                shutil.copyfile(f"./angelic_dataset/{charac}.png", f"./breast_size/{size}/{charac}.png")
                print(f"{charac}.png sucessfully replace")
            except Exception as e:
                print(e)

def k():
    size_map = {}
    r = requests.get("https://kamigoroshi-aria.wikiru.jp/index.php?%E3%82%B9%E3%83%AA%E3%83%BC%E3%82%B5%E3%82%A4%E3%82%BA%E4%B8%80%E8%A6%A7")
    soup = BeautifulSoup(r.text, "html.parser")
    row_list = soup.find("table",id="sortabletable1").find("tbody").find_all("tr")
    for row in row_list:
        row = row.find_all("td")
                #name                               #height         #b                  #w
        size_map[row[2].text] = cup_transform(int(row[8].text), int(row[10].text), int(row[11].text))
    for root, dirname, filenames in os.walk("./kamigoroshi_dataset"):
        for filename in filenames:
            try:
                shutil.copyfile(f"./kamigoroshi_dataset/{filename}", f"./breast_size/{size_map[filename.strip('.png')]}/{filename}")
                print(f"{filename} sucessfully replace")
            except Exception as e:
                print(e)

def princess_connect_getimg(size, charac):
    r = requests.get(f"https://princess-connect.fandom.com/wiki/{charac}")
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        img_tag_set = soup.find("div", class_="pi-image-collection wds-tabber").find_all("div")[1::]
    except:
        img_tag_set = [soup.find("aside", role="region")]
    count = 0
    for img_tag in img_tag_set:
        img_url = img_tag.find("figure").find("a")['href']
        with open(f"./princess_connect_dataset/{charac}_{count}.png", "wb") as fwb:
            fwb.write(requests.get(img_url).content)
            print(f"{charac}_{count}.png done")
            try:
                shutil.copyfile(f"./princess_connect_dataset/{charac}_{count}.png", f"./breast_size/{size}/{charac}_{count}.png")
                print(f"{charac}_{count}.png successfully copy")
            except Exception as e:
                print(e)
        count+=1

def princess_connect():
    size_map = {}
    with open("princess_connect.txt", "r") as fr:
        for line in fr.readlines():
            characs = line.split()[1::]
            size = line.split()[0]
            size_map[size] = []
            for charac in characs:
                size_map[size].append(charac)
                princess_connect_getimg(size, charac)

princess_connect()