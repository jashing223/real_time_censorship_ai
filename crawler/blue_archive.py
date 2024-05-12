import requests
from bs4 import BeautifulSoup
import shutil

def check():
    charac_list = []
    characs = set()
    with open("blue_archive_size.txt", "r") as fr:
        for row in fr.readlines():
            charac_list += row.split()[1::]
    r = requests.get("https://bluearchive.fandom.com/wiki/Category:Students")
    soup = BeautifulSoup(r.text, "html.parser")
    charac_table = soup.find_all("table")[2].find("tbody")
    charac_rows = charac_table.find_all("tr")[1::]
    for row in charac_rows:
        name = row.find("td").find("div").find("div").text
        characs.add(name)
    for charac in charac_list:
        if charac not in characs: print(f"{charac} failed")

def get_charac_img(size: str, name: str, url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    img_url = soup.find_all("figure", class_="pi-item pi-image")[1].find("a")['href']
    with open(f"./blue_archive_dataset/{name}.png", "wb") as fwb:
        fwb.write(requests.get(img_url).content)
        print(f"{name} done")
        try:
            shutil.copyfile(f"./blue_archive_dataset/{name}.png", f"./breast_size/{size}/{name}.png")
            print(f"{name} successfully copied")
        except Exception as e:
            print(e)


def get_all_charac_name():
    charac_map = {}
    with open("blue_archive_size.txt", "r") as fr:
        for row in fr.readlines():
            for name in row.split()[1::]:
                charac_map[name] = row.split()[0]
    r = requests.get("https://bluearchive.fandom.com/wiki/Category:Students")
    soup = BeautifulSoup(r.text, "html.parser")
    charac_table = soup.find_all("table")[2].find("tbody")
    charac_rows = charac_table.find_all("tr")[1::]
    for row in charac_rows:
        sur_name_tag = row.find("td").find("div").find("div")
        if sur_name_tag.text in charac_map:
            img_wiki_url = f"https://bluearchive.fandom.com{sur_name_tag.find_next_sibling('div').find('a')['href']}"
            get_charac_img(charac_map[sur_name_tag.text], sur_name_tag.find_next_sibling('div').find('a')['title'], img_wiki_url)

get_all_charac_name()