import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
#Инициализация
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4
comparatorvalue = 1
list1 = []
value = 0

#Настройка

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

#Объявление функций

def dec2bin(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def bin2led(value):
    signal = dec2bin(value)
    GPIO.output(leds, signal)
    return signal

def adc():
    value = 2**(bits - 1)
    for i in range(1, 8):
        signal = bin2dac(value)
        time.sleep(0.001)
        comparatorvalue = GPIO.input(comparator)
        if comparatorvalue == 1:
            value += (2**(bits - i - 1))
        else:
            value -= (2**(bits - i - 1))
    value -= (value % 2)
    signal = bin2dac(value)
    return value
try:

    #Зарядка конденсатора

    GPIO.output(troykaModule, 1)
    time1 = time.time()
    print("Зарядка конденсатора")
    while value <= 240:
        value = adc()
        list1.append(value)
        bin2led(value)

    #Разрядка конденсатора

    GPIO.output(troykaModule, 0)
    print("Разрядка конденсатора")
    while value >= 10:
        value = adc()
        list1.append(value)
        bin2led(value)

    #Анализ данных

    print("Эксперимент завершён. Обработка данных.")
    time1 = time.time() - time1
    freq = 1/(time1/len(list1))

    #Построение графика

    plt.plot(list1)
    plt.show()

    #Запись результатов в file.txt

    list1 = [str(i) for i in list1]
    with open("data.txt", "w") as file:
        file.write("\n".join(list1))

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleanup completed")
