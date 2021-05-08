from selenium import webdriver
from time import sleep
from collections import defaultdict
import re

def main():
    try:
        driver = webdriver.Chrome()
        driver.get("https://kuku-kube.com/")
        sleep(1)

        play_btn = driver.find_element_by_xpath("//*[@id='index']/div[3]/button")
        play_btn.click()
        sleep(1)

        while True:
            time = int(driver.find_element_by_xpath("//*[@id='room']/header/span[2]").text)

            if time <= 1:
                break

            game = driver.find_element_by_xpath("//*[@id='box']")
            btns = re.findall('\(([^)]+)', game.get_attribute("innerHTML"))
            colors = defaultdict(list)
            
            for i, rgb in enumerate(btns, start=1):
                colors[rgb].append(i)                        

            for v in colors.values():
                if len(v) == 1:
                    driver.find_element_by_xpath(f"//*[@id='box']/span[{v[0]}]").click()

    finally:
        try:
            sleep(10000)
        except:
            driver.close()
            driver.quit()

if __name__ == '__main__':
    main()