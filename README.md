# Sine Wave Producer

## Data
### Description
- ts: UNIX timestamp of when data was produced
- x: Float array for graph x-axis
- y: Float array for graph y-axis

### Format
``` json
{
  "ts": <float>,
  "x": <array>,
  "y": <array>
}
```
### Example with `X_LEN` of 10

```json
{
  "ts": 1678365923.8776073, 
  "x": [0.0, 0.6981317007977318, 1.3962634015954636, 2.0943951023931953, 2.792526803190927, 3.490658503988659, 4.1887902047863905, 4.886921905584122, 5.585053606381854, 6.283185307179586], 
  "y": [0.8545989080882804, 0.3208684319195699, -0.3629999495997086, -0.8770166204062203, -0.9806674675706343, -0.6254531077538699, 0.022417712317940538, 0.659799035651065, 0.9884530573535778, 0.8545989080882807]
}
```


## Available environment variables
### Logging
- `LOGLEVEL` - Sets logging level (default: `INFO`)

### MQTT client settings
- `MQTT_HOST` - MQTT broker address (default: `localhost`)
- `MQTT_PORT` - MQTT broker port (default: `1883`)
- `MQTT_TIMEOUT` - MQTT client keepalive duration (default: `60`)
- `ROOT_MQTT_TOPIC` - Root MQTT publish topic (default: `testing`)
- `DATA_MQTT_TOPIC` - MQTT topic for sine wave data (default: `sine_wave`)

### Application settings
- `FPS` - Data generation frequency (frames per second) (default: `1`)
- `X_LEN` - Length of generated data array (default: `100`)
