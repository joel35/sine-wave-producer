# Publish sine wave data via MQTT.
# Version 1.1 GC - Added peaks finder over a threshold to data, listed as xPOI (point of interest).
import itertools
import json
import logging
import os
from functools import partial
from time import sleep, time
from typing import Callable, Iterator, Any
import numpy as np
from paho.mqtt import client
from scipy.signal import find_peaks

from mqtt_publisher import initialise_mqtt_connection

LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TIMEOUT = int(os.getenv("MQTT_TIMEOUT", 60))

ROOT_MQTT_TOPIC = os.getenv('ROOT_MQTT_TOPIC', 'testing')
DATA_MQTT_TOPIC = os.getenv('DATA_MQTT_TOPIC', 'sine_wave')

FPS = int(os.getenv('FPS', 5))
X_LEN = int(os.getenv('X_LEN', 100))

#added V1.1
USE_POI = bool(os.getenv('USE_POI', False))
POI_THRESHOLD = float(os.getenv('POI_THRESHOLD', 10.0)) # set the threshold out of range so it doesnt get triggered.

logging.basicConfig(level=LOGLEVEL)

RUN = True


def main():
    loop(
        get_x=partial(get_x_func, X_LEN),
        get_y=get_y_func,
        get_poi=partial(get_xpoi_func, np.array),
        publish=partial(publish_func, get_mqtt()),
        run=get_run,
        counter=itertools.count(0),
        delay=delay_func
    )


def loop(
        get_x: Callable[[], np.ndarray],
        get_y: Callable[[int, np.ndarray], np.ndarray],
        get_poi: Callable[[int, np.ndarray], np.ndarray],
        publish: Callable[[Any, Any], bool],
        run: Callable[[], bool],
        counter: Iterator,
        delay: Callable[[], None]
):
    x = get_x()

    while run():
        y = get_y(next(counter), x)
        xpoi = get_poi(y)
        publish(x, y, xpoi)
        delay()


def get_x_func(x_len: int = 100) -> np.ndarray:
    return np.linspace(0, 2 * np.pi, x_len)


def get_y_func(i: int, x: np.ndarray) -> np.ndarray:
    return sine_wave(x + i / 10)

def get_xpoi_func(i: int, y: np.ndarray) -> np.ndarray:
    if (USE_POI == True):
        peaks = find_peaks(abs(y), height=POI_THRESHOLD)
    else:
        peaks = []   
    return peaks

def publish_func(mqtt_client: client.Client, x: np.ndarray, y: np.ndarray, xpoi: np.ndarray) -> bool:
    if (USE_POI == True):
        peakPnt = list(xpoi[0].astype(float))
        peakLabel = []
    #    TODO: Add some code to find moving or static items and change the labels accordingly.
    #          If range was available at this point it could also be added, or calculated at received end.
        for hi in range(len(peakPnt)):
            peakLabel.append('Something')
        outputPeak = peakPnt + peakLabel
        data_json = json.dumps({
        'ts': time(),
        'x': list(x),
        'y': list(y),
        'xpoi': outputPeak,
        })
    else:
        data_json = json.dumps({
        'ts': time(),
        'x': list(x),
        'y': list(y),
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
