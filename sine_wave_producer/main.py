import itertools
import json
import logging
import os
from functools import partial
from time import sleep, time
from typing import Callable, Iterator, Any
import numpy as np
from paho.mqtt import client

from mqtt_publisher import initialise_mqtt_connection

LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TIMEOUT = int(os.getenv("MQTT_TIMEOUT", 60))

ROOT_MQTT_TOPIC = os.getenv('ROOT_MQTT_TOPIC', 'testing')
DATA_MQTT_TOPIC = os.getenv('DATA_MQTT_TOPIC', 'sine_wave')

FPS = int(os.getenv('FPS', 1))
X_LEN = int(os.getenv('X_LEN', 100))

logging.basicConfig(level=LOGLEVEL)

RUN = True


def main():
    loop(
        get_x=partial(get_x_func, X_LEN),
        get_y=get_y_func,
        publish=partial(publish_func, get_mqtt()),
        run=get_run,
        counter=itertools.count(0),
        delay=delay_func
    )


def loop(
        get_x: Callable[[], np.ndarray],
        get_y: Callable[[int, np.ndarray], np.ndarray],
        publish: Callable[[Any, Any], bool],
        run: Callable[[], bool],
        counter: Iterator,
        delay: Callable[[], None]
):
    x = get_x()

    while run():
        y = get_y(next(counter), x)
        publish(x, y)
        delay()


def get_x_func(x_len: int = 100) -> np.ndarray:
    return np.linspace(0, 2 * np.pi, x_len)


def get_y_func(i: int, x: np.ndarray) -> np.ndarray:
    return sine_wave(x + i / 10)


def publish_func(mqtt_client: client.Client, x: np.ndarray, y: np.ndarray) -> bool:
    data_json = json.dumps({
        'ts': time(),
        'x': list(x),
        'y': list(y)
    })

    result = publish_many(
        to_publish={get_topic(): data_json},
        client=mqtt_client
    )

    logging.debug(f'{result=}')
    return True


def sine_wave(x):
    return np.sin(x)


def get_run() -> bool:
    return RUN


def get_topic(data_topic: str = None, root: str = None) -> str:
    root = root or ROOT_MQTT_TOPIC
    data_topic = data_topic or DATA_MQTT_TOPIC
    return f'{root}/{data_topic}'


def get_mqtt(host: str = None, port: int = None, timeout: int = None):
    kwargs = dict(
        host=host or MQTT_HOST,
        port=port or MQTT_PORT,
        timeout=timeout or MQTT_TIMEOUT,
    )

    return initialise_mqtt_connection(**kwargs)


def publish_many(to_publish: dict[str, Any], client: client.Client) -> list[int]:
    logging.debug(f'{to_publish=} {client=}')

    results = [
        client.publish(topic=topic, payload=payload)
        for topic, payload in to_publish.items()
    ]

    client.loop()
    return results


def delay_func(i: int = None):
    i = i or 1 / FPS
    sleep(i)


if __name__ == '__main__':
    main()
