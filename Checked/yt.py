from types import BuiltinMethodType
from selenium import webdriver
from pytube import YouTube
import time, os, mysql.connector, urllib.request
from datetime import date, datetime
from ocr import detect_document
from vid import framecap, screenS
from webdriver_manager.chrome import ChromeDriverManager

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123ManugaD",
  database="capitalstreet"
)

mycursor = mydb.cursor()



op = webdriver.ChromeOptions()
op.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
driver.get('https://youtube.com/playlist?list=PLUfKAimIKI9W_kkXSEZ7Sii5kLjWYjxTM')
link = driver.find_element_by_xpath("//*[@id='img']")
link.click()
time.sleep(4)
titles = []
while True:
    today_date = datetime.now().strftime("%b %#d, %Y")
    video_date = driver.find_element_by_xpath("//*[@id='date']/yt-formatted-string").text
    button = driver.find_element_by_class_name("ytp-play-button.ytp-button")
    button.click()
    print(today_date, video_date)
    if today_date == video_date:
        print("yes")
        time.sleep(2)
        title = driver.find_element_by_xpath("//*[@id='container']/h1/yt-formatted-string").text
        if not title in titles:
            titles.append(title)
            print(f"Downloading : {title}")
            YouTube(driver.current_url).streams.filter(res="720p").first().download(f"videos")
            print("Download Finished")
            next_button = driver.find_element_by_class_name("ytp-next-button.ytp-button")
            next_button.click()
            time.sleep(8)
            button = driver.find_element_by_class_name("ytp-play-button.ytp-button")
            button.click()
            title = title.replace(',', '')
            title = title.replace('|', '')
            title = title.replace('/', '')
            f = framecap(title=title)
            if f == False:
                print("Video doesn't have a signal")
                continue
            else:
                print("good")
                str_list = detect_document(f"Screenshots/{title}.jpg")
                signal = screenS(str_list=str_list)
                os.remove(f"Screenshots/{title}.jpg")
                print(signal)
                if signal == False:
                    print("signal Fail")
                    continue
                else:
                    for i in signal:
                        print(signal[i])
                    sql = f"INSERT INTO trades (currency, BS, BS_type, TP, SL, Dates, duration) VALUES ('{signal['TC']}', '{signal['BS']}', '{signal['BS_type']}', '{signal['TP']}', '{signal['SL']}', '{datetime.now().strftime('%d-%m-%Y')}', '60')"
                    msg = f"{signal['BS_type']} {signal['TC']} {signal['BS']} SL {signal['SL']} TP {signal['TP']}"
                    msg = msg.replace('&', '%26')
                    urllib.request.urlopen(f"https://api.telegram.org/bot1447605485:AAHdSqT49TKsuRg6Jg9lRToeKDqH9BFEjUQ/sendMessage?chat_id=804493713&text={msg.replace(' ', '+')}")
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
        else:
            time.sleep(4)
            driver.get('https://youtube.com/playlist?list=PLUfKAimIKI9W_kkXSEZ7Sii5kLjWYjxTM')
            time.sleep(4)
            link = driver.find_element_by_xpath("//*[@id='img']")
            link.click()
            time.sleep(4)
            
    else:
        time.sleep(4)
        driver.get('https://youtube.com/playlist?list=PLUfKAimIKI9W_kkXSEZ7Sii5kLjWYjxTM')
        time.sleep(4)
        link = driver.find_element_by_xpath("//*[@id='img']")
        link.click()
        time.sleep(4)
        

# Opens the Video file
    
    # img = cv2.imread(f"Screenshots/{title.replace(',', '')}.jpg")
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # gray = cv2.bitwise_not(img_bin)
    # kernel = np.ones((2, 1), np.uint8)
    # img = cv2.erode(gray, kernel, iterations=1)
    # img = cv2.dilate(img, kernel, iterations=1)
    # str_list = detect_document(f"Screenshots/{title.replace(',', '')}.jpg")
    # for i in str_list:
    #     print(str_list[i])
    # for i in str_list:
    #     if ("Technical" in i):
    #         print(i)
    #     elif ("BUY :" in i):
    #         print(i)
    #     elif "SL" in i:
    #         print(i)
    #     elif ("Trading" in i):
    #         print(i)
    #     elif ("TP" in i):
    #         print(i)
    #     elif ("SELL :" in i):
    #         print(i)
    # print(str_list)