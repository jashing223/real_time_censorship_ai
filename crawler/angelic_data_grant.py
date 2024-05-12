import requests
from bs4 import BeautifulSoup

#不直接爬圖是因為網站的圖不來自遊戲卡面angelic

def get_img(name: str):
    img_r = requests.get(f"https://angelic.wikiru.jp/?plugin=attach&refer={name}&openfile={name}.png")
    with open(f"./angelic_dataset/{name}.png", "wb") as fwb:
        fwb.write(img_r.content) 


size_map = {}
r = requests.get("https://angelic.wikiru.jp/?%E3%83%90%E3%82%B9%E3%83%88%E3%82%B5%E3%82%A4%E3%82%BA%E9%A0%86%E4%B8%80%E8%A6%A7")
soup = BeautifulSoup(r.text, "html.parser")
full_table = soup.find_all("table",class_="style_table")[-1]
chuck_data = full_table.find("tbody").find_all("tr")
for chuck in [chuck_data[x] for x in range(0, len(chuck_data)-1, 2)]:
    # size, charac_list
    size_map[chuck.find("th",class_="style_th").text] = []
    chracs = chuck.find("td",class_="style_td").find_all("a")
    for chrac in chracs:
        name = chrac['title']
        size_map[chuck.find("th",class_="style_th").text].append(name)

for size, charac_list in size_map.items():
    for charac in charac_list:
        get_img(charac)
        print(f"{charac} done")