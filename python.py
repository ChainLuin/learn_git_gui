import paho.mqtt.client as mqtt
import time
import json

# MQTT 配置
MQTT_BROKER = "broker.emqx.io"  # MQTT 代理服务器地址
MQTT_PORT = 1883                # MQTT 代理服务器端口，默认为 1883
MQTT_TOPIC_PUB = "testtopic/"   # 发布主题
MQTT_CLIENT_ID = "python-mqtt-client"  # 客户端 ID

# 模拟的温湿度数据
def generate_sensor_data():
    import random
    temperature = round(random.uniform(20, 30), 2)  # 随机生成温度值
    humidity = round(random.uniform(40, 60), 2)     # 随机生成湿度值
    return {"temperature": temperature, "humidity": humidity}

# MQTT 发布消息
def publish_message(client, topic, payload):
    try:
        client.publish(topic, payload)
        print(f"Published message: {payload}")
    except Exception as e:
        print(f"Failed to publish message: {e}")

# 主程序
def main():
    # 创建 MQTT 客户端
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)  # 连接到 MQTT 代理服务器

    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")

    try:
        while True:
            # 生成模拟的温湿度数据
            sensor_data = generate_sensor_data()
            payload = json.dumps(sensor_data)  # 将数据转换为 JSON 格式

            # 发布消息
            publish_message(client, MQTT_TOPIC_PUB, payload)

            # 每隔 10 秒发送一次消息
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.disconnect()  # 断开与 MQTT 代理服务器的连接

if __name__ == "__main__":
    main()