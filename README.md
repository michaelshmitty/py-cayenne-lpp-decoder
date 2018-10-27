# py-cayenne-lpp-decoder
Cayenne Low Power Payload decoder written in Python.
See [Cayenne Low Power Payload Documentation](https://mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload) for more information.

The decoder expects a base64 encoded payload string, commonly used in LoRaWAN implementations.

## Usage

```python
>>> import cayennelpp
>>> print(cayennelpp.lppdecode('A2cBEAVnAP8='))
[{'channel': 3, 'type': 'Temperature Sensor', 'value': 27.2}, {'channel': 5, 'type': 'Temperature Sensor',
'value': 25.5}]

```
