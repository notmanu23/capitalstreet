from selenium import webdriver
import time, urllib.request
from webdriver_manager.chrome import ChromeDriverManager

op = webdriver.ChromeOptions()
op.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)

links = []

while True:
    driver.get("https://www.capitalstreetfx.com/en/technical-analysis/")

    link = driver.find_element_by_xpath("//*[@id='main']/div/section/div/div/table[1]/tbody/tr[1]/td[1]/a").get_attribute("href")
    if not link in links:
        links.append(link)
        driver.get(link)
        time.sleep(2)
        trades = []

        for i in range(10, 50):
            try:
                data = driver.find_element_by_xpath(f"/html/body/div[3]/div/div[2]/div/section/article/div/div[3]/p[{i}]").text
                trades.append(data)
            except:
                continue
        removable = []
        for i in trades:
            removable.append(i)
            if i == "TECHNICAL SUMMARY":
                break

        for i in removable:
            trades.remove(i)

        signals = {}
        for i in range(0, len(trades), 2):
            signals[trades[i]] = trades[i+1]

        for i in signals.keys():
            if "buy" in signals[i].lower():
                bs = "Buy"
            elif "sell" in signals[i].lower():
                bs = "Sell"
            x = signals[i].replace('\n', '')
            x = signals[i].replace('TRADE SUGGESTION- ', '')
            x = x.split("AT")
            a = x[0].strip()   
            b = "".join(i for i in x[1] if i in "0123456789.")
            c = "".join(i for i in x[2] if i in "0123456789.")
            d = "".join(i for i in x[3] if i in "0123456789.")
            signals[i] = [a,b,c,d]
            msg = f"{bs} {i} {b} SL {d} TP {c}"
            urllib.request.urlopen(f"https://api.telegram.org/bot1447605485:AAHdSqT49TKsuRg6Jg9lRToeKDqH9BFEjUQ/sendMessage?chat_id=804493713&text={msg.replace(' ', '+')}")
    time.sleep(120)