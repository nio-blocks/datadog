from nio import TerminatorBlock
from nio.properties import FloatProperty, StringProperty, VersionProperty
from datadog import initialize, api


class DatadogCustomMetrics(TerminatorBlock):

    version = VersionProperty('0.1.0')
    api_key = StringProperty(title="API Key", default="[[DATADOG_API_KEY]]")
    app_key = StringProperty(title="APP Key", default="[[DATADOG_APP_KEY]]")
    metric = StringProperty(title="Metric", default="my.value")
    value = FloatProperty(title="Value", default="{{ $value }}")

    def configure(self, context):
        super().configure(context)
        options = {
            'api_key': self.api_key(),
            'app_key': self.app_key(),
        }
        initialize(**options)

    def process_signals(self, signals):
        for signal in signals:
            # Submit a single point with a timestamp of `now`
            api.Metric.send(metric=self.metric(), points=self.value(signal))
