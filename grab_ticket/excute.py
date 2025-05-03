import sys
from datetime import datetime
import os

#add project_root path into system path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from BuyTicket_Code import TicketBuyer
from config.setting import BUY_DATE
from apscheduler.schedulers.blocking import BlockingScheduler

Ticket_buyer = TicketBuyer()

def execute():
    Ticket_buyer.login()
    schedule = BlockingScheduler(timezone='Asia/Shanghai')
    schedule.add_job(
        Ticket_buyer.start_buy,
        'date',
        run_date=BUY_DATE,
    )
    schedule.start()

if __name__ == '__main__':
    execute()