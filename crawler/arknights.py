import requests
from bs4 import BeautifulSoup
import shutil

#取得角色網址
def get_charac_url(size: str, name: str):
    r = requests.get(f"https://gamepress.gg/arknights/operator/{name}")
    soup = BeautifulSoup(r.text, "html.parser")
    img_tags = soup.find_all("div", class_="operator-image")[1::]
    count = 0
    for img_tag in img_tags:
        img_url = f'https://gamepress.gg{img_tag.find("a").find("img")["src"]}'
        with open(f"./arknights_dataset/{name}_{count}.png", "wb") as fwb:
            fwb.write(requests.get(img_url).content)
            print(f"{name}_{count} done")
        try:
            shutil.copyfile(f"./arknights_dataset/{name}_{count}.png", f"./breast_size/{size}/{name}_{count}.png")
            print(f"{name}_{count} successfully copied")
        except Exception as e:
            print(e)
        count += 1

#取得網站所有角色的網址
def get_all_charac_url():
    size_map = {}
    with open("arknights.txt", "r") as fr:
        for characs in fr.readlines():
            size_map[characs.split()[0]] = characs.split()[1::]
    for size, names in size_map.items():
        for name in names:
            get_charac_url(size, name)
        

#檢測資料角色資料
def check_data():
    r = requests.get("https://gamepress.gg/arknights/tools/interactive-operator-list")
    soup = BeautifulSoup(r.text, "html.parser")
    charac_row = soup.find_all("tr", class_="operators-row")
    charac_set = set()
    for row in charac_row:
        charac_set.add(row['data-name'])
    with open("arknights.txt", "r") as fr:
        for characs in fr.readlines():
            for charac in characs.split()[1::]:
                if charac not in charac_set:
                    print(f"{charac} fail")
# pass
# check_data()

get_all_charac_url()