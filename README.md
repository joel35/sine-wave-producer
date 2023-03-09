# Sine Wave Producer

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
