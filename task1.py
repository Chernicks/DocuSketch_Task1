import psutil
import requests
import time
import asyncio
import msvcrt
from random import random
import sys
import logging

# Сформируем файл логов
logging.basicConfig(level="DEBUG", filename="mylog.log", datefmt="%d/%m/%Y %I:%M:%S", encoding="utf-8", 
        filemode="w", format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]")

try:
    # Пороговое значение потребления памяти в процентах
    Threshold = int(sys.argv[1])
    # URL используемого API
    Url = sys.argv[2]
except Exception as e:
    logging.exception(e)
    Threshold = 90
    Url = 'https://example.com/api/v1/alert'

# Функция генерации alarm путем отправки http запроса
def send_alarm(value, Url):
    payload = {
        'value': value,
        'time': int(time.time()),
    }
    response = requests.post(Url, json=payload)
    print(f"Alarm sent: {response.status_code}")

# Функция контроля потребления памяти
async def check_memory(Threshold, Url):
    total_mem = psutil.virtual_memory()
    used_mem = total_mem.percent
    if used_mem > Threshold:
        send_alarm(used_mem, Url)        
    else:
        print(f"{used_mem:.2f}% memory used")

# Функция выполнения других задач
async def other_tasks():
    print("Here we do something else")
    value = random()
    await asyncio.sleep(value)

# Функция асинхронного запуска функций
async def main():
    tasks = [asyncio.create_task(check_memory(Threshold=Threshold, Url=Url)), asyncio.create_task(other_tasks())]
    try:
        await asyncio.wait(tasks)
    except Exception as e:
        logging.exception(e)
    finally:
        for task in tasks:
            task.cancel()

# Запускаем цикл на выполнение задач, прервать можем нажатием Esc
if __name__ == "__main__":
    while True:
        asyncio.run(main())
        if msvcrt.kbhit():
            if ord(msvcrt.getche()) == 27:
                break