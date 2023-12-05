import paho.mqtt.client as mqtt , os
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

# water level sensor
pin_num_1 = 4
pin_num_2 = 14
pin_num_3 = 15
GPIO.setup(pin_num_1, GPIO.IN)
GPIO.setup(pin_num_2, GPIO.IN)
GPIO.setup(pin_num_3, GPIO.IN)

# led
# green
led_pin_1 = 17
# yellow
led_pin_2 = 22
# red
led_pin_3 = 23
GPIO.setup(led_pin_1, GPIO.OUT)
GPIO.setup(led_pin_2, GPIO.OUT)
GPIO.setup(led_pin_3, GPIO.OUT)

level_state = [0,0,0]

def update_leds(LED):
	if LED == "water_level_11" :
		level_state[0] = 1
	elif LED == "water_level_10" :
		level_state[0] = 0	

	elif LED == "water_level_21" :
		level_state[1] = 1

	elif LED == "water_level_20" :
		level_state[1] = 0

	elif LED == "water_level_31" :
		level_state[2] = 1

	elif LED == "water_level_30" :
		level_state[2] = 0
	led_on_off()		
	
def led_on_off():
	if level_state == [0, 0, 0]:
		print("수위 낮음, all led off" )
		GPIO.output(led_pin_1, GPIO.LOW)
		GPIO.output(led_pin_2, GPIO.LOW)
		GPIO.output(led_pin_3, GPIO.LOW)
	elif level_state == [1, 0, 0]:
		print("수위 적정, green led on")
		GPIO.output(led_pin_1, GPIO.HIGH)
		GPIO.output(led_pin_2, GPIO.LOW)
		GPIO.output(led_pin_3, GPIO.LOW)
	elif level_state == [1, 1, 0]:
		print("수위 주의, yellow led on")
		GPIO.output(led_pin_1, GPIO.HIGH)
		GPIO.output(led_pin_2, GPIO.HIGH)
		GPIO.output(led_pin_3, GPIO.LOW)		
	elif level_state == [1, 1, 1]:
		print("수위 위험, red led on")
		GPIO.output(led_pin_1, GPIO.HIGH)
		GPIO.output(led_pin_2, GPIO.HIGH)
		GPIO.output(led_pin_3, GPIO.HIGH)
	elif level_state == [1, 0, 1]:
		GPIO.output(led_pin_1, GPIO.LOW)
		GPIO.output(led_pin_2, GPIO.LOW)
		GPIO.output(led_pin_3, GPIO.LOW)
		print("수위 감지 오류 1,0,1")
	elif level_state == [0, 1, 1]:
		GPIO.output(led_pin_1, GPIO.LOW)
		GPIO.output(led_pin_2, GPIO.LOW)
		GPIO.output(led_pin_3, GPIO.LOW)
		print("수위 감지 오류 0,1,1")
	elif level_state == [0, 0, 1]:
		GPIO.output(led_pin_1, GPIO.LOW)
		GPIO.output(led_pin_2, GPIO.LOW)
		GPIO.output(led_pin_3, GPIO.LOW)
		print("수위 감지 오류 0,0,1")

# Define event callbacks  
def on_connect(client, mosq, obj, rc):
	print ("on_connect:: Connected with result code "+ str ( rc ) )
	print("rc: " + str(rc))

def on_message(mosq, obj, msg):
	topic = msg.topic
	payload = msg.payload.decode("utf-8")
	a = topic + payload
	update_leds(a)

def on_publish(mosq, obj, mid):
	print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
	print("This means broker has acknowledged my subscribe request")
	print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
	print(string)


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

client = mqtt.Client()
# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# Uncomment to enable debug messages
client.on_log = on_log

# user name has to be called before connect - my notes.
client.connect('localhost', 1883, 60)

client.loop_start()
client.subscribe ("water_level_1" ,0 )
client.subscribe ("water_level_2" ,0 )
client.subscribe ("water_level_3" ,0 )
 
run = True
	
while run:
	water_level_1, water_level_2, water_level_3 = \
	 GPIO.input(pin_num_1), GPIO.input(pin_num_2), GPIO.input(pin_num_3)
	
	if water_level_1 is not None and water_level_2 is not None and water_level_3 is not None:
		client.publish ( "water_level_1", water_level_1)
		client.publish ( "water_level_2", water_level_2)
		client.publish ( "water_level_3", water_level_3)
		print("water level 1:", water_level_1)  
		print("water level 2:", water_level_2)
		print("water level 3:", water_level_3)
		time.sleep(3)
	else:
		print('Failed to get reading. Try again!')	
		sleep(10)