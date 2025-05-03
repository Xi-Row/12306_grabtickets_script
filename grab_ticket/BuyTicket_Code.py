import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as excon
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from config.setting import (FROM_STATION, TO_STATION,
                                                          TRAIN_DATE, PASSENGER_NAME,
                                                          IS_STUDENT, SEAT_POSITION,
                                                          SEAT_TYPE, TRAIN_ORDER,
                                                          PAY_TIME_LEFT)
class TicketBuyer:
    #Url
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
    profile_url = 'https://kyfw.12306.cn/otn/view/index.html'
    left_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
    confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

    #Infromation
    from_station = FROM_STATION
    to_station = TO_STATION
    train_date = TRAIN_DATE
    trains_order = TRAIN_ORDER
    passenger_list = PASSENGER_NAME

    #Options
    options = Options()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_experimental_option("detach", True)
    # options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")

    #browser driver
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 8)


    #log in
    def login(self):
        #navigate to a url
        self.driver.get(self.login_url)
        #wait until the web url to profile url
        WebDriverWait(self.driver,120).until(
            excon.url_to_be(self.profile_url)
        )
        self.driver.get(self.left_ticket_url)
        print("log in Successfully")
        #logging...

    #set cookies
    def set_cookies(self):
        # self.driver.add_cookie({'name':'_jc_save_showIns','value':True})
        self.driver.add_cookie({'name':'_jc_save_fromStation','value':self.from_station})
        self.driver.add_cookie({'name':'_jc_save_toStation','value':self.to_station})
        self.driver.add_cookie({'name':'_jc_save_fromDate','value':self.train_date})
        self.driver.refresh()


    #query and choose ticket
    def query_choose_ticket(self):
        from_to_station = self.driver.find_element(By.ID, 'fromStation')
        to_station = self.driver.find_element(By.ID, 'toStation')
        train_date = self.driver.find_element(By.ID, 'train_date')
        from_station_code = FROM_STATION
        to_station_code = TO_STATION
        # execute through js
        self.driver.execute_script('arguments[0].value="%s"' % from_station_code, from_to_station)
        self.driver.execute_script('arguments[0].value="%s"' % to_station_code, to_station)
        self.driver.execute_script('arguments[0].value="%s"' % self.train_date, train_date)

        times = 1
        while True:
            if times >= 20:
                break
            try:
                WebDriverWait(self.driver,0.5).until(
                    excon.element_to_be_clickable((By.XPATH, '//*[@id="query_ticket"]'))
                ).click()
                self.wait.until(
                    excon.presence_of_element_located((By.XPATH, '//tbody[@id="queryLeftTable"]/tr'))
                )
                trains = self.driver.find_elements(By.XPATH,
                                                   '//tbody[@id="queryLeftTable"]/tr[not(@datatran)]')
                order_btn = trains[self.trains_order - 1].find_element(By.XPATH, './/a[@class="btn72"]')
                order_btn.click()
                break

            except:
                #logging...
                continue

    #choose type of seat(optional)
    def choose_seat_type(self, seat_type=None,idx=0):

        if seat_type is not None:
            type_options = self.driver.find_element(By.ID, f'seatType_{idx+1}')
            Select(type_options).select_by_value(f"{seat_type}")

    #choose position of seat(optional)
    def choose_seat_position(self, seat_type=None, seat_position=None):
        type_dict = {'O':'erdeng1', 'M':'yideng1'}
        if seat_position is not None:
            try:
                seat_order = WebDriverWait(self.driver,0.1).until(
                    excon.element_to_be_clickable((By.XPATH,
                               f'//div[@id="{type_dict[seat_type]}"]//ul/li/a[@id="1{seat_position}"]'))
                )
                seat_order.click()
            except:
                #logging...
                pass

    #confirm passenger:
    def confirm_passenger(self):
        self.wait.until(
            excon.url_to_be(self.confirm_url)
        )
        self.wait.until(
            excon.presence_of_element_located((By.XPATH, '//ul[@id="normal_passenger_id"]/li/label'))
        )
        passenger_list = self.driver.find_elements(By.XPATH, '//ul[@id="normal_passenger_id"]/li/label')

        idx = -1
        for passenger in passenger_list:
            name = passenger.text
            if name in self.passenger_list:
                idx += 1
                passenger.click()
                try:
                        WebDriverWait(self.driver, 0.2).until(
                            excon.presence_of_element_located((By.XPATH, '//div[@class="lay-btn"]'))
                        )
                        is_student_options = self.driver.find_elements(By.XPATH,
                                           '//div[@id="dialog_xsertcj"]//a[@shape="rect"]')

                        if IS_STUDENT[idx]:
                            is_student_options[2].click()
                        else:
                            is_student_options[1].click()

                except:
                    pass
                self.choose_seat_type(SEAT_TYPE[idx],idx)

        self.wait.until(
            excon.presence_of_element_located((By.XPATH, '//a[@id="submitOrder_id"]'))
        ).click()

        self.choose_seat_position(SEAT_TYPE[0], SEAT_POSITION)

        stfm = time.time()
        while True:
            if  time.time() - stfm >= 10:
                break
            try:
                final_confirm = self.driver.find_element(By.XPATH, '//a[@id="qr_submit_id"]')
                final_confirm.click()
            except:
                pass
        print('break successfully!!')
        if PAY_TIME_LEFT:
            time.sleep(600)

    def start_buy(self):
        try:
            self.set_cookies()

            self.query_choose_ticket()

            self.confirm_passenger()
            return True

        except:
            return False



if __name__ == '__main__':
    ticket_buyer = TicketBuyer()
    ticket_buyer.login()
    st = time.time()
    ticket_buyer.start_buy()
    ed = time.time()
    print(ed - st)
