import os
import pandas as pd
import win32com.client as win32
from ga4 import GA4RealTimeReport, Dimensions, Metrics

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4_service_acct.json'    
property_id = '307310528'

lst_dimension = [Dimensions['Country'], 'deviceModel']
lst_metrics = ['activeUsers']

ga4_realtime = GA4RealTimeReport(property_id)
response = ga4_realtime.query_report(
    dimensions=lst_dimension,
    metrics=lst_metrics
)

df = pd.DataFrame(data=response.get('rows'), columns=response.get('headers'))
df['activeUsers'].astype(int).sum()