import RPi.GPIO as GPIO

from time import sleep

# https://robototehnika.ru/content/article/upravlenie-neskolkimi-servoprivodami-na-raspberry-pi-dlya-mekhanizma-povorota-naklona-pi-kamery/

"""
Различие между GPIO.setmode(GPIO.BOARD) и GPIO.setmode(GPIO.BCM) заключается в системе нумерации выводов.
В первом случае используется нумерация разъема P1 на борту Raspberry Pi,
а во втором случае нумерация выводов системы-на-кристалле Broadcom, являющейся ядром Raspberry Pi. 
Следует знать, что в случае с BCM нумерация выводов между первой и второй ревизиями немного отличается,
а при использовании BOARD ревизия не имеет никакого значения, все остается тем же самым.
"""

GPIO.setmode(GPIO.BCM)
tiltPin = 17
GPIO.setup(tiltPin, GPIO.OUT)
# частота
tilt = GPIO.PWM(tiltPin, 50)
# Включаем генерацию сигнала ШИМ на выводе и задаём начальный коэффициент заполнения равный нулю:
tilt = start(0)

# 0 градусов ==> заполнение 3%
# 90 градусов ==> заполнение 8%
# 180 градусов ==> заполнение 13%
tilt.ChangeDutyCycle(5)

tilt = stop()
GPIO.cleanup()


def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()

# подключене светодиодов или динамика

# Disable warnings (optional)
GPIO.setwarnings(False)
# Select GPIO mode
GPIO.setmode(GPIO.BCM)
# Set buzzer - pin 23 as output
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)
# Run forever loop
while True:
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(0.5)  # Delay in seconds
    GPIO.output(buzzer, GPIO.LOW)
    print("No Beep")
    sleep(0.5)
