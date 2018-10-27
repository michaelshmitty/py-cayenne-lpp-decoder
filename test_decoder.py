# -*- coding: utf-8 -*-
import unittest
import cayennelpp


class DecoderTestCase(unittest.TestCase):
    """Unit tests for Cayenne LPP decoder."""

    def test_two_temperature_sensors(self):
        result = cayennelpp.lppdecode('A2cBEAVnAP8=')
        self.assertEqual(result,
                         [{'channel': 3,
                           'type': 'Temperature Sensor',
                           'value': 27.2},
                          {'channel': 5,
                           'type': 'Temperature Sensor',
                           'value': 25.5}])

    def test_temperature_and_acceleration_sensors(self):
        result = cayennelpp.lppdecode('AWf/1wZxBNL7LgAA')
        self.assertEqual(result,
                         [{'channel': 1,
                           'type': 'Temperature Sensor',
                           'value': -4.1},
                          {'channel': 6,
                           'type': 'Accelerometer',
                           'value': {'x': 1.234, 'y': -1.234, 'z': 0.0}}])

    def test_decode_gps(self):
        result = cayennelpp.lppdecode('AYgGdl/ylgoAA+g=')
        self.assertEqual(result,
                         [{'channel': 1,
                           'type': 'GPS Location',
                           'value': {'lat': 42.3519,
                                     'lon': -87.9094,
                                     'alt': 10.0}}])

    def test_decode_all_previous_tests_combined(self):
        result = cayennelpp.lppdecode(
            'AWcBEAVnAP8CZ//XA3EE0vsuAAAEiAZ2X/KWCgAD6A==')
        self.assertEqual(result,
                         [{'channel': 1,
                           'type': 'Temperature Sensor',
                           'value': 27.2},
                          {'channel': 5,
                           'type': 'Temperature Sensor',
                           'value': 25.5},
                          {'channel': 2,
                           'type': 'Temperature Sensor',
                           'value': -4.1},
                          {'channel': 3,
                           'type': 'Accelerometer',
                           'value': {'x': 1.234, 'y': -1.234, 'z': 0.0}},
                          {'channel': 4,
                           'type': 'GPS Location',
                           'value': {'lat': 42.3519,
                                     'lon': -87.9094,
                                     'alt': 10.0}}])

    def test_decode_unknown_lpp_data_type(self):
        result = cayennelpp.lppdecode('AQQBEA==')
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
