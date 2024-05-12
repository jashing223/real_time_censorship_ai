import requests
import io
import os
import aiohttp
import asyncio
import time

# download message
# extract picture
# download picture
# async

HEADERS = {
        "Authorization": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }

# https://discord.com/api/v9/channels/1193561050008801410/messages?before=1196132591141666876&limit=50
def GetChatMessage(channelID: str, fileOpener: io.TextIOWrapper, lastMessageID = ""):

    requestArgument = "" if not lastMessageID else f"before={lastMessageID}&"

    response = requests.get(f"https://discord.com/api/v9/channels/{channelID}/messages?{requestArgument}limit=100", headers=HEADERS)
    messageData = response.json()
    if not messageData: return
    fileOpener.write(str(messageData)+"\n")
    if len(messageData) < 100: return
    newLastMessageID = messageData[-1]["id"]
    print(newLastMessageID)
    GetChatMessage(channelID=channelID, fileOpener=fileOpener, lastMessageID = newLastMessageID)

def isFileExist(filepath: str):
    if os.path.exists(filepath):
        print(f"{filepath} exist")
        return True
    return False

def BackupChatInFile(channelID: str, filepath: str):
    if isFileExist(filepath): return

    with open(filepath, "w"): pass
    with open(filepath, "a", encoding="utf-8") as fa:
        GetChatMessage(channelID=channelID, fileOpener=fa)

def ExtractImageUrlFromBackup(filepath: str):
    if not isFileExist(filepath): return

    urls = []
    with open(filepath, "r", encoding="utf-8") as fr:
        for chunkData in fr.readlines():
            messageDatas = eval(chunkData)
        
            urls += ExtractImageUrlFromMessage(messageDatas)

    return urls

def ExtractImageUrlFromMessage(messageDatas: list):
    urls = []
    for message in messageDatas:
        for attachment in message["attachments"]:
            if not "image" in attachment['content_type']: continue 
            urls.append(attachment["url"])
        for embed in message["embeds"]:
            if embed["type"] != "image": continue
            urls.append(embed["thumbnail"]["url"])

    return urls

def StoreImageUrlFromBackup(backupFilePath:str, storeFilePath: str):
    if isFileExist(storeFilePath): return

    with open(storeFilePath, "w") as fw:
        urls = ExtractImageUrlFromBackup(backupFilePath)
        for url in urls:
            fw.write(url+"\n")



progressCount = 0

def WriteProgressBar(url, now, total):
    progress = int(round(now/total, 2)*100//2)
    paddingSpace = "" if len(url) < 72 else f"{' '*(72-len(url))}"
    print(f"\r{url}{paddingSpace}", end="")
    print(f"\nDownloading |{'▓'*progress}{' '*(50-progress)}| ({now}/{total})", end="")

async def DownloadFile(url: str, session: aiohttp.ClientSession, outputPath: str, filename, urlsCount: int):
    global progressCount
    async with session.get(url) as response:
        with open(f"{outputPath}/{filename}.{url.split('.')[-1].split('?')[0]}", "wb") as fwb:
            async for chunk in response.content.iter_chunked(256*1024):
                fwb.write(chunk)
            progressCount += 1
            WriteProgressBar(url, progressCount, urlsCount)
        

async def DownloadStoredImageUrlsFile(outputPath: str, ImageUrlsFile: str):
    if not os.path.isfile(ImageUrlsFile):
        print("Image urls file is not exist")
        return
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    processingFileCount = 1
    with open(ImageUrlsFile, "r", encoding="utf-8") as fr:
        async with aiohttp.ClientSession() as session:
            tasks = []
            urls = fr.readlines()
            urlsCount = len(urls)
            for i in range(urlsCount):
                tasks.append(
                    DownloadFile(url = urls[i].strip('\n'),
                                 urlsCount = urlsCount,
                                 session = session,
                                 outputPath = outputPath,
                                 filename = i)
                    )

                processingFileCount += 1

                if len(tasks) >= 10:
                    await asyncio.gather(*tasks)
                    tasks.clear()
                    time.sleep(1)
            await asyncio.gather(*tasks)
            print("\r [Finished] ")
            global progressCount
            progressCount = 0

def TryBar():
    now = 1
    total = 100
    for i in range(total):
        time.sleep(0.1)
        WriteProgressBar("https://cdn.discordapp.com/attachments/933631098561372210/1109763368073572442/71894921_p5.jpg?ex=65b613ad&is=65a39ead&hm=4ad1c86fee55f613fc9290773754663d471c9a8ef0c38ffbacafa8ee9a879d2d&", now = now, total = total)
        now+=1

def main():
    # BackupChatInFile("858972515479977994", "./messageRecord_meme.txt")
    # ExtractImageUrlFromBackup("./messageRecord_meme.txt")
    # StoreImageUrlFromBackup("./messageRecord_meme.txt", storeFilePath="./image.txt")
    asyncio.run(DownloadStoredImageUrlsFile(outputPath="./output", ImageUrlsFile="image.txt"))
    # TryBar()
    ...

if __name__ == "__main__":
    main()
    