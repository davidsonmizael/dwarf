from io import BytesIO
import base64
import requests
import pyautogui

image = pyautogui.screenshot()
buffered = BytesIO()
image.save(buffered, format="JPEG")
image.close()
b64image = base64.b64encode(buffered.getvalue()).decode('utf-8')

#do something with the image, like for example, upload it to a ftp server