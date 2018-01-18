from unittest.mock import patch, MagicMock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..datadog_custom_metrics_block import DatadogCustomMetrics

# A test to send data to datadog

class TestDatadog(NIOBlockTestCase):

    def test_default_config(self):
        """API is called with default property values."""
        blk = DatadogCustomMetrics()
        with patch(blk.__module__ + ".api") as api:
            with patch(blk.__module__ + ".initialize") as initialize:
                self.configure_block(blk, {})
                blk.start()
                blk.process_signals([Signal({"value": 3.14})])
                blk.stop()
                self.assert_num_signals_notified(0)
                api.Metric.send.assert_called_once_with(
                    metric="my.value", points=3.14)

    def test_blk_configure(self):
        """Datadog initialize is called with correct api and app keys."""
        blk = DatadogCustomMetrics()
        with patch(blk.__module__ + ".initialize") as initialize:
            self.configure_block(blk, {
                "api_key": "abc123def456",
                "app_key": "123abc456def890",
            })
            initialize.assert_called_once_with(
                api_key='abc123def456', app_key='123abc456def890')

    def test_configurable_value(self):
        """Correct signal sent with dynamic value."""
        blk = DatadogCustomMetrics()
        with patch(blk.__module__ + ".api") as api:
            with patch(blk.__module__ + ".initialize") as initialize:
                self.configure_block(blk, {
                    "metric": "nio.value",
                    "value": "{{ $nio }}",
                })
                blk.start()
                blk.process_signals([Signal({"nio": 5.5})])
                blk.stop()
                self.assert_num_signals_notified(0)
                api.Metric.send.assert_called_once_with(
                    metric="nio.value", points=5.5)

    def test_multiple_signals(self):
        """API is called for each signal processed."""
        blk = DatadogCustomMetrics()
        with patch(blk.__module__ + ".api") as api:
            with patch(blk.__module__ + ".initialize") as initialize:
                self.configure_block(blk, {})
                blk.start()
                signals = [
                    Signal({"value": 3.14}),
                    Signal({"value": 4.15}),
                ]
                blk.process_signals(signals)
                blk.stop()
                self.assert_num_signals_notified(0)
                self.assertEqual(api.Metric.send.call_count, 2)
                api.Metric.send.assert_any_call(
                    metric="my.value", points=3.14)
                api.Metric.send.assert_any_call(
                    metric="my.value", points=4.15)
