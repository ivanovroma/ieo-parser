import time
import datetime
from Logger import Logger

logger = Logger()

class Timer:
    def sleep(self, result):
        
        success = result.get('success')
        if success:
            timer = self.__get_next_check_time()
            
            time.sleep(timer)
        else:
            minuts = 2
            logger.info(f'Что-то пошло не так, следущая попытка через {minuts}м.')
            
            time.sleep(minuts * 60)

    def __get_next_check_time(self):
        now = datetime.datetime.now()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        wake_up_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)
        delta = wake_up_time - now

        timer = delta.seconds

        hours = timer // 3600
        minutes = (timer % 3600) // 60
        seconds = timer - (hours * 3600) - (minutes * 60)

        logger.info(f'Следующая проверка через {hours}ч. {minutes}м. {seconds}с.')

        return timer
