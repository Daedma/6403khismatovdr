import time
import threading
import logging
import numpy as np
from time_series_analysis import TimeSeries

class Service:
    def __init__(self, data_source):
        self.__is_running = false
        self.__data_source = data_source
        self.__thread = None
        self.__logger = logging.getLogger(__name__)
        self.__data = list()

    def run(self):
        self.__prerun()
        if self.__thread is not None:
            error = RuntimeError("Попытка повторного запуска сервиса")
            self.__logger.warning(error)
            raise error
        self.__thread = threading.Thread(target=self.__run_Impl, args=())
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

    def __run_Impl(self):
        while (self.__is_running):
            value = self.__data_source.get_current()
            self.__data.append(value)
            time_series = TimeSeries(self.__data)
            print("Текущий ряд : ", list(time_series.data))
            print("Автокорреляция : ", list(time_series.autocorrelation(2)))
            print("Скользящее среднее : ", list(time_series.smoothed(3)))
            print("Дифференциал : ", list(time_series.difference()))
            print("Экстремумы : ", list(time_series.find_extrema()))
            time.sleep(60)
        
    def __prerun(self):
        self.__logger.info("Начало загрузки данных за последние 15 минут")
        try:
            self.__data = self.__data_source.get_period(period='15m', interval='1m')
            self.__logger.info("Загрузка прошла успешно")
        except:
            error = RuntimeError("Ошибка при загрузке данных")
            self.__logger.warning(error)
            raise error


    