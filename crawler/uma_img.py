import requests
import random

def main():
    for i in range(1,9):
        r = requests.get(f"https://umamusume.jp/app/wp-json/wp/v2/character?per_page=12&page={i}")
        r.encoding = "utf-8"
        all_chrac = r.json()
        for row in all_chrac:
            print(row['acf']['en'])
            print(row["title"]["rendered"], end=" ")
            img_r = requests.get(row["acf"]["chara_img"][random.randint(0,len(row["acf"]["chara_img"])-1)]["image"])
            with open(f'./uma_dataset/{row["title"]["rendered"]}.png', "wb") as fwb:
                fwb.write(img_r.content)
            print("done")

main()