#setting

from grab_ticket.citycode import init_station_code

# station cookie

FROM_STATION = 'NCG'

TO_STATION = 'NJH'

TRAIN_DATE = '2025-05-16'

#passenger
#form:['name1(student)if is_student', 'name2',...]
PASSENGER_NAME = [' ']
#form: 3
TRAIN_ORDER = 5
#form: [bool, bool,...]
IS_STUDENT = [True]
#form:['O', 'M', ...]
#'O' is 2nd class, 'M' is 1st class, '' is hard seat
SEAT_TYPE = ['O']

#'A','B','C','D','F','G' only support one passenger to choose seat position
#if don't choose let it equals to None
SEAT_POSITION = 'A'

#chromedriver path
EXECUTABLE_PATH = 'D:\Python\Grab_Train_tickets\chrome_driver\chromedriver.exe'

#buy ticket date
#form:'2025-05-03 01:04:01'
BUY_DATE = '2025-05-03 15:55:00'

#whether to spare time to pay for ticket:
PAY_TIME_LEFT = True

if __name__ == '__main__':
    city_code_dic = init_station_code('D:\Python\Python_Crawler\Ticket_help\grab_ticket_12306\station_code.xlsx')
    from_station = input("input from_station, then output a code of it:")
    print(city_code_dic[from_station])
    to_station = input("input to_station, then output a code of it:")
    print(city_code_dic[to_station])
