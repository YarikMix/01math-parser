# -*- coding: utf-8 -*-
import time
from pathlib import Path
import pickle

from selenium import webdriver

from auth_data import login, password
from data import tests_dict


class _01MathParser():
    def __init__(self):
        self.URL = "https://www.01math.com/maths/class?class_id=1"
        self.LOGIN_URL = "https://www.01math.com/user/login"
        self.BASE_DIR = Path(__file__).resolve().parent
        self.PATH_ANSWERS = self.BASE_DIR.joinpath("answers")
        self.tests_dict = tests_dict

        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
        )
        # headless mode
        options.add_argument("--headless")
        options.add_argument("window-size=2560x1440")
        driver = webdriver.Chrome(
            executable_path=self.BASE_DIR.joinpath("chromedriver.exe"),
            options=options
        )

        self.driver = driver

    def authorization(self):
        """Authorization"""
        self.driver.get(self.LOGIN_URL)

        login_input = self.driver.find_element_by_name("login_or_email")
        login_input.send_keys(login)

        password_input = self.driver.find_element_by_name("pwd")
        password_input.send_keys(password)

        self.driver.find_element_by_class_name("btn-primary").click()
        time.sleep(1)

        #cookies
        pickle.dump(self.driver.get_cookies(), open("cookies", "wb"))

    def get_data(self):
        # Создаём папку с ответами на контрольную работу
        self.answers_to_test_path.mkdir()

        tasks = self.driver.find_elements_by_class_name("panel")
        tabs = self.driver.find_elements_by_css_selector(".green-tab.last-tab")
        for i in range(0, len(tasks)):
            tabs[i].click()
            self.driver.execute_script("arguments[0].scrollIntoView();", tasks[i])
            screenshot_path = self.answers_to_test_path.joinpath(f"{i}.png")
            self.driver.save_screenshot(str(screenshot_path))
            i += 1

        self.driver.close()
        self.driver.quit()

    def is_enabled(self):
        menus = self.driver.find_elements_by_css_selector("ul.dropdown-menu")
        for menu in menus:
            if menu.is_displayed():
                li = menu.find_elements_by_css_selector("li")[-1]
                self.link = li.find_element_by_css_selector("a")
                if "disabled" in self.link.get_attribute("class").split():
                    return False
                else:
                    return True

    def prepare(self):
        # Создаём папку с данными, если её ещё нет
        if not self.PATH_ANSWERS.exists():
            self.PATH_ANSWERS.mkdir()

        # Путь до папки с ответами на контрольную работу
        self.answers_to_test_path = self.PATH_ANSWERS.joinpath(self.test_name)
        if self.answers_to_test_path.exists():
            print(f"Папка с ответами на работу {self.test_name} уже существует")
            self.parse()
        else:
            cookies_path = self.BASE_DIR.joinpath("cookies")
            # Проверяем на наличие кукисов
            if cookies_path.exists():
                # Загружаем кукисы, если они есть
                self.driver.get(self.URL)

                for cookie in pickle.load(open("cookies", "rb")):
                    self.driver.add_cookie(cookie)

                self.driver.refresh()
            else:
                self.authorization()  # Авторизовываемся

            self.driver.get(self.URL)

            self.driver.find_element_by_xpath(f"//span[text()='{self.test_name[:-3]}']").click()
            time.sleep(1)

            title = f"\n{self.tests_dict[self.test_name]}            "
            self.driver.find_element_by_xpath(f"//a[text()='{title}']").click()
            time.sleep(3)

            if not self.is_enabled():
                print("Контрольная работа по этой теме недоступна")
                self.parse()
            else:
                self.link.click()
                time.sleep(2)

                window_after = self.driver.window_handles[1]
                self.driver.switch_to.window(window_after)

                self.driver.find_element_by_css_selector(".btn.btn-lg.btn-primary").click()
                time.sleep(2)

                self.driver.find_element_by_css_selector("div[style='width: 120px;']").click()
                time.sleep(2)

                print(f"Контрольная работа по теме '{self.tests_dict[self.test_name]}'")
                print("Собираю данные...")

                self.get_data()

                print(f"Данные собраны")

    def parse(self):
        self.test_name = input("> ")  # Пример: ЕГЭ.07.03
        # Проверяем, существует ли такая страница на сайте 01math
        if self.test_name not in self.tests_dict:
            print("Такой контрольной работы не существует")
            self.parse()
        else:
            self.prepare()


if __name__ == "__main__":
    Parser = _01MathParser()
    Parser.parse()