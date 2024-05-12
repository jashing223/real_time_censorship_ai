import requests
from bs4 import BeautifulSoup
import shutil

def check():
    characs_set = set()
    all_characs = set()
    with open("azur_lane.txt", "r", encoding="utf-8") as fr:
        for row in fr.readlines():
            charac_list = row.split("\t")[1].strip("\n")
            for name in charac_list.split("/"):
                characs_set.add(name)
    r = requests.get("https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Image")
    soup = BeautifulSoup(r.text, "html.parser")
    ship_cards = soup.find_all("div", class_="azl-shipcard")
    for ship_card in ship_cards:
        name = ship_card.find("div", class_="alc-top truncate").text
        all_characs.add(name)
    for charac in characs_set:
        if charac not in all_characs: print(f"{charac} failed")

def get_charac_img(size: str, name: str, wiki_url:str):
    r = requests.get(wiki_url)
    soup = BeautifulSoup(r.text, "html.parser")
    img_tags = soup.find_all("div",class_="shipskin-image res-h")
    count = 0
    for img_tag in img_tags:
        img_url = img_tag.find("a").find("img")['src']
        with open(f"./azur_lane_dataset/{name}_{count}.png", "wb") as fwb:
            fwb.write(requests.get(img_url).content)
        print(f"{name}_{count} done")
        try:
            shutil.copyfile(f"./azur_lane_dataset/{name}_{count}.png", f"./breast_size/{size}/{name}_{count}.png")
            print(f"{name} successfully copied")
        except Exception as e:
            print(e)
        count += 1


def get_all_charac_img():
    characs_dict = {}
    with open("azur_lane.txt", "r", encoding="utf-8") as fr:
        for row in fr.readlines():
            charac_list = row.split("\t")[1].strip("\n")
            size = row.split("\t")[0]
            for name in charac_list.split("/"):
                characs_dict[name] = size
    r = requests.get("https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Image")
    soup = BeautifulSoup(r.text, "html.parser")
    ship_cards = soup.find_all("div", class_="azl-shipcard")
    for ship_card in ship_cards:
        name = ship_card.find("div", class_="alc-top truncate").text
        ship_wiki_url = f"https://azurlane.koumakan.jp{ship_card.find('div', class_='alc-top truncate').find('a')['href']}/Gallery"
        if name in characs_dict:
            get_charac_img(characs_dict[name], name, ship_wiki_url)

get_all_charac_img()