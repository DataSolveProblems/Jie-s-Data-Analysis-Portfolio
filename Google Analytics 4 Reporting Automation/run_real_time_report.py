import os
import datetime
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (Dimension, Metric, Metric)
from google.analytics.data_v1beta.types import RunRealtimeReportRequest

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4_service_acct.json'
client = BetaAnalyticsDataClient()

property_id = '307310528'

# https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-api-schema
request = RunRealtimeReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name='country'), Dimension(name='city'), Dimension(name='deviceCategory'), Dimension(name='platform')],
    metrics=[Metric(name="activeUsers")]
)

response = client.run_realtime_report(request)

headers = [header.name for header in response.dimension_headers] + [header.name for header in response.metric_headers]
rows = []
for row in response.rows:
    rows.append(
        [dimension_value.value for dimension_value in row.dimension_values] + \
        [metric_value.value for metric_value in row.metric_values])

df = pd.DataFrame(rows, columns=headers)

