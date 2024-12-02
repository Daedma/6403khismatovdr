import time
import threading
import logging
import numpy as np
from time_series_analysis import TimeSeries


class CancellationToken:
    """
    Класс токена отмены выполнения задачи.
    """

    def __init__(self):
        self.__is_canceled = False

    def is_canceled(self) -> bool:
        """
        Метод проверки отмены задачи.
        Returns:
            True, если задача была отменена.
        """
        return self.__is_canceled

    def cancel(self) -> None:
        """
        Метод установки статуса отмены выполнения задачи.
        """
        self.__is_canceled = True


class DataMonitor:

    def __init__(self, data_source):
        self.__cancellation_token = None
        self.__data_source = data_source
        self.__thread = None
        self.__logger = logging.getLogger(__name__)
        self.__data = np.array([])

    def run(self, output_file="out.txt"):
        self.__prerun()
        if self.__thread is not None:
            error = RuntimeError("Попытка повторного запуска сервиса")
            self.__logger.warning(error)
            raise error
        self.__cancellation_token = CancellationToken()
        self.__thread = threading.Thread(
            target=self.__run_Impl, args=(output_file, self.__cancellation_token)
        )
        try:
            self.__thread.start()
            self.__logger.info("Сервис запустился")
        except:
            error = RuntimeError("Не удалось запустить сервис")
            self.__logger.error(error)
            raise error

    def stop(self):
        """
        Метод остановки сервиса.
        """
        if self.__thread is None:
            error = RuntimeError("Попытка остановить незапущенный сервис")
            self.__logger.warning(error)
            raise error
        self.__cancellation_token.cancel()
        self.__thread.join()
        self.__thread = None
        self.__logger.info("Сервис завершил работу")

    def __run_Impl(self, output_file, cancellation_token):
        while not cancellation_token.is_canceled():
            value = self.__data_source.get_current()
            self.__data = np.append(self.__data, value)
            time_series = TimeSeries(self.__data)
            with open(output_file, "a") as file:
                file.write(f"Текущий ряд : {list(time_series.data)}\n")
                file.write(f"Автокорреляция : {list(time_series.autocorrelation(2))}\n")
                file.write(f"Скользящее среднее : {list(time_series.smoothed(3))}\n")
                file.write(f"Дифференциал : {list(time_series.difference())}\n")
                file.write(f"Экстремумы : {list(time_series.find_extrema())}\n")
                file.write("\n")
            self.__logger.info(f"Данные записаны в файл: {output_file}")
            time.sleep(5)

    def __prerun(self):
        self.__logger.info("Начало загрузки данных за последний день")
        try:
            self.__data = self.__data_source.get_period(period="1d", interval="1m")
            self.__logger.info("Загрузка прошла успешно")
        except:
            error = RuntimeError("Ошибка при загрузке данных")
            self.__logger.warning(error)
            raise error
