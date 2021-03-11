from selenium import webdriver
from datetime import datetime
import time, urllib,requests
import re
from webdriver_manager.chrome import ChromeDriverManager

def process_str(in_str):
  return re.sub('^.*?: ', '', in_str)


op = webdriver.ChromeOptions()
op.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
links = []
lst = []
while True:
    driver.get("https://www.capitalstreetfx.com/en/trade-idea/")
    print("yes")
    posts = driver.find_elements_by_class_name("column.dt-sc-one-third")
    for post in posts:
        p_date = post.find_element_by_class_name("date").text
        p_date = p_date.replace("Posted on ", '')
        t_date = datetime.utcnow().strftime("%d %b %Y")
        if p_date == t_date and not post.text in lst:
            try:
                link = post.find_element_by_css_selector('.entry-thumb a').get_attribute('href')
            except:
                link = post.find_element_by_css_selector('.entry-details a').get_attribute('href')
            links.append(link)
    if len(links) != 0:
        for link in links:
            if not link in lst: 
                lst.append(link)
                if len(lst) > 20:
                    lst.pop()
                driver.get(link)
                time.sleep(2)
        
                signal = driver.find_elements_by_class_name("has-text-align-center")
                for i in signal:
                    if "TRADE SIGNAL" in i.text:
                        m = i.text.replace('-', '–')
                        x = m.split('–')
                        print(x)
                        currency = process_str(x[1])
                        bs = x[2].split(':')[1]
                        if 'BUY' in x[2].split(':')[0]:
                            bs_type = 'Buy'
                        elif 'SELL' in x[2].split(':')[0]:
                            bs_type = 'Sell'
                        bs = "".join(i for i in bs if i in "0123456789.")
                        tp = "".join(i for i in x[2].split(':')[2] if i in "0123456789.")
                        sl = "".join(i for i in x[2].split(':')[3] if i in "0123456789.")
                        msg = f"{bs_type} {currency} {bs} SL {sl} TP {tp}"
                        urllib.request.urlopen(f"https://api.telegram.org/bot1447605485:AAHdSqT49TKsuRg6Jg9lRToeKDqH9BFEjUQ/sendMessage?chat_id=804493713&text={msg.replace(' ', '+')}")
            