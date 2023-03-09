import logging
from time import sleep
from paho.mqtt import client as mqtt


def initialise_mqtt_connection(
        host: str,
        port: int,
        timeout: int,
        protocol: int = mqtt.MQTTv5

):
    client = mqtt.Client(protocol=protocol)
    client.on_connect = on_connect_callback
    client.on_connect_fail = on_connect_fail_callback
    client.on_disconnect = on_disconnect_callback

    logging.debug(f'{client.__dict__}')

    result = client.connect(
        host=host,
        port=port,
        keepalive=timeout
    )

    logging.info(f'{result=}')
    logging.info(f'{client.is_connected()=}')
    return client


def on_connect_callback(client: mqtt.Client, userdata: dict, flags: dict, reason_code: mqtt.ReasonCodes,
                        properties) -> None:
    logging.info(f"Connected to MQTT broker with result code: {reason_code}, flags: {flags}")


def on_connect_fail_callback(client: mqtt.Client, userdata: dict) -> None:
    logging.warning("Connection failed! Reconnecting...")
    sleep(1)
    client.reconnect()


def on_disconnect_callback(client: mqtt.Client, userdata: dict, reason_code: mqtt.ReasonCodes, properties) -> None:
    logging.warning(f"Disconnected. Reason: {reason_code}")
    if reason_code != 0:
        logging.error("Unexpected: True. Reconnecting...")
        sleep(1)
        client.reconnect()
