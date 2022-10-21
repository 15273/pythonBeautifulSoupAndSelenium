from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

from selenium.webdriver.common.by import By

"https://docs.google.com/forms/d/e/1FAIpQLSe9I_VeykYUUL4jmGHW6vqCiyhI-xQSyE1u2lCWmsobBZ3mGw/viewform?usp=sf_link"
"https://forms.gle/hKm4XKF7PHMxSewKA"

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/106.0.0.0 Mobile Safari/537.36"
}

response = requests.get(
    "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3"
    "A%7B%22west%22%3A-123.27516331015882%2C%22east%22%3A-122.28502048789319%2C%22south%22%3A37.31005546199283%2"
    "C%22north%22%3A37.65659426441187%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22ma"
    "x%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%2"
    "2max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A"
    "%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%"
    "22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D",
    headers=header)


web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

list_links = []

cl = soup.select("div", {"class": "property-card-data"})
print(len(cl))
for a in cl:

    if a.select_one("a", {"data-text": "property-card-link"}) is not None and \
            a.find("span", {"data-test": "property-card-price"}) is not None:

        print(a.find("span", {"data-test": "property-card-price"}).text)
        print(a.select_one("a", {"data-text": "property-card-link"})["href"])
        print(a.select_one("a address").text)
        address = a.select_one("a address").text
        href = a.select_one("a", {"data-text": "property-card-link"})["href"]
        span = a.find("span", {"data-test": "property-card-price"}).text
        if "http" not in a.select_one("a", href=True)["href"]:
            list_links.append({
                "a": f"https://www.zillow.com{href}",
                "address": address,
                "span": span,
            })
        else:
            # print(a.find("a", href=True)["href"])
            list_links.append({"a": href,
                               "address": address,
                               "span": span})

print(list_links)
print(len(list_links))

chrome_driver_path = "/Users/admit/Desktop/קוד החלמה jetbrauns/chromedriver"

from selenium.webdriver.chrome.service import Service

s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

for n in range(len(list_links)):
    driver.get("https://docs.google.com/forms/d/1qk4ovkWgBQBHHj3qZE9aq9etswfhH0AO6oRzXfx3Zqs/edit")
    time.sleep(2)
    print(driver.find_element(By.XPATH,
                              "/html/body/div/div[3]/form/div[2]/div/div[2]/div[1]/div/"
                              "div/div[2]/div/div[1]/div/div[1]/input"))

    address = driver.find_element(By.XPATH,
                                  "/html/body/div/div[3]/form/div[2]/div/div[2]/div["
                                  "1]/div/div/div[2]/div/div[1]/div/div[1]/input")

    price2 = driver.find_element(By.XPATH,
                                 "/html/body/div/div[3]/form/div[2]/div/div[2]/div[2]/div/div/div[2]"
                                 "/div/div[1]/div/div[1]/input")

    link = driver.find_element(By.XPATH,
                               "/html/body/div/div[3]/form/div[2]/div/div[2]/div[3]/div/div"
                               "/div[2]/div/div[1]/div/div[1]/input")

    submit = driver.find_element(By.XPATH, "/html/body/div/div[3]/form/div[2]/div/div[3]/div[1]/div[1]/div")
    link.send_keys(list_links[n]["a"])
    address.send_keys(list_links[n]["address"])
    price2.send_keys(list_links[n]["span"])
    submit.click()

"property-card-price"
