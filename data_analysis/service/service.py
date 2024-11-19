import time
import threading
import logging

class Service:
    def __init__(self, data_source):
        self.__is_running = false
        self.__data_source = data_source
        self.__thread = None
        self.__logger = logging.getLogger(__name__)

    def run(self, period: int):
        if self.__thread is not None:
            error = RuntimeError("Попытка повторного запуска сервиса")
            self.__logger.warning(error)
            raise error
        self.__thread = threading.Thread(target=self.__run_Impl, args=(period))
        try:
            self.__thread.start()
            self.__is_running = True
            self.__logger.info("Сервис запустился")
        except:
            error = RuntimeError("Не удалось запустить сервис")
            self.__logger.error(error)
            raise error

    
    def stop(self):
        '''
        Метод остановки сервиса.
        '''
        if self.__thread is None:
            error = RuntimeError("Попытка остановить незапущенный сервис")
            self.__logger.warning(error)
            raise error
        self.__is_running = False
        self.__thread.join()
        self.__thread = None
        self.__logger.info("Сервис завершил работу")

    def __run_Impl(self, period):
        while (self.__is_running):
            value = self.__data_source.get_current()
            print(value)
            time.sleep(period)
        