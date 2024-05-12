import cv2
import os
import time

# for roots, dirnames, filenames in os.walk(".\\breast_size"):
#     for filename in filenames:
#         try:
#             image = cv2.imread(f"{roots}\\{filename}")
#             image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)
#             cv2.imwrite(f"{roots}\\{filename}", image)
#             time.sleep(1)
#             print(f"{roots}\\{filename} done")
#         except:
#             print(f"{roots}\\{filename} failed")
image = cv2.imread(f"./75115124_p0_master1200.jpg")
image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)
cv2.imwrite(f"./75115124_p0_master1200.jpg", image)