from selenium import webdriver
from datetime import datetime
import time, urllib.request, re
from webdriver_manager.chrome import ChromeDriverManager

op = webdriver.ChromeOptions()
op.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)

list = []
while True:
    driver.get("https://www.capitalstreetfx.com/en/trade-signal/")
    posts = driver.find_elements_by_class_name("wpb_column.vc_column_container.vc_col-sm-3.td_res")
    for post in posts:
        text = post.text
        text = text.splitlines()
        p_date = text[1].split(" ")[-1]
        t_date = datetime.utcnow().strftime("%d/%m/%Y")
        if p_date == t_date:
            if not post.text in list:
                print("yes")
                print(list)
                list.append(post.text)
                text[0] = re.sub(' +', ' ', text[0])
                text[0] = text[0].replace(" / ", "/")
                bs = "".join(i for i in text[3] if i in "0123456789.")
                tp = "".join(i for i in text[4] if i in "0123456789.")
                sl = "".join(i for i in text[5] if i in "0123456789.")
                if "sell" in text[3].lower():
                    bs_type = "Sell"
                elif "buy" in text[3].lower():
                    bs_type = "Buy"
                msg = f"{bs_type} {text[0]} {bs} SL {sl} TP {tp}"
                urllib.request.urlopen(f"https://api.telegram.org/bot1447605485:AAHdSqT49TKsuRg6Jg9lRToeKDqH9BFEjUQ/sendMessage?chat_id=804493713&text={msg.replace(' ', '+')}")
                if not len(list) < 10:
                    list.pop() 
    time.sleep(120)