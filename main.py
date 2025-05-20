from machine import Pin, I2C
import ssd1306
import time
from dht import DHT11hel
import ujson
from umqtt.simple import MQTTClient
import network

# 配置文件
MQTT_CLIENT_ID = "micropython-weather-publisher"
MQTT_BROKER    = "broker.emqx.io"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC_PUB = "sc104/9032/get_temperature" # 发布主题: room/学号后4位/get_temperature
MQTT_TOPIC_SUB = "sc104/9032/set_temperature" # 订阅主题: room/学号后4位/set_temperature
WIFI_NAME  = "cafe1" # WiFi 名称
WIFI_PASSWORD  = "88888888" # WiFi 密码

# 初始化全局变量
target_temperature = None  # 上次接收到的目标温度

# MQTT的订阅回调函数
def sub_callback(topic, msg):
    global target_temperature
    try:
        data = ujson.loads(msg.decode())
        if "target_temperature" in data:
            target_temperature = data["target_temperature"]
            print("topic:", topic.decode())
            print("receive target：", target_temperature)
    except Exception as e:
        print("parse error：", e)

# 连接 WiFi
print(f"Connecting to WiFi {WIFI_NAME}", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# 初始化 MQTT 客户端
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(sub_callback)
client.connect()
client.subscribe(MQTT_TOPIC_SUB)
print("Connected and subscribed to:", MQTT_TOPIC_SUB)

# 初始化 I2C 和 OLED
i2c = I2C(0, scl=Pin(4), sda=Pin(5))
time.sleep(0.5)
devices = i2c.scan()
if devices:
    print('I2C devices found:', devices)
else:
    print('No I2C devices found')

oled_width = 128
oled_height = 64
addr = devices[0]
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=addr)

# 初始化 DHT11
dht = DHT11(Pin(6))

# 主循环
while True:
    # 处理 MQTT 消息（检查是否有订阅消息到达）
    client.check_msg()

    # 读取温湿度
    try:
        dht.measure()
        temp = dht.temperature()
        hum = dht.humidity()
    except Exception as e:
        print("读取传感器失败：", e)
        temp = hum = None

    # 更新 OLED 显示
    oled.fill(0)
    if temp is not None and hum is not None:
        msg1 = f"Temp: {temp} C"
        msg2 = f"Humid: {hum}%"
        oled.text(msg1, 0, 0)
        oled.text(msg2, 0, 15)

        # 发布数据
        payload = ujson.dumps({
            "temperature": temp,
            "humidity": hum,
        })
        # 获取发布结果
        try:
            client.publish(MQTT_TOPIC_PUB, payload)
            print("publish successed:", payload)
        except Exception as e:
            print("publish failed:", e)
    else:
        oled.text("Sensor Error", 0, 0)

    # 显示目标温度（如果之前收到过）
    if target_temperature is not None:
        oled.text(f"Set: {target_temperature} C", 0, 30)
    else:
        oled.text(f"Set: None", 0, 30)

    oled.show()

    # 每 10 秒执行一次
    time.sleep(10)


