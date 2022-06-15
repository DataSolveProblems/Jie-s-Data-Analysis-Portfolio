# Data Analysis Projects

## 1. JJ Data Connector
A lightweight Python package to provide simple interface to query data and report from Google Analytics 4, YouTube Analytics, Google Search Console Analytics, and Salesforce.

### Basic Usage
1. Enable API services.

3. Start using the API.

#### Querying report from Google Search Console

```Python
from jj_data_connector.yt_analytics import YTAnalytics, CoreDimensions, SubDimensions, CoreMetrics, SubMetrics
from jj_data_connector.gsc import GoogleSearchConsole
from jj_data_connector.ga4 import GA4RealTimeReport, GA4Report, Metrics, Dimensions
from jj_data_connector.sfdc import generate_access_token
import pandas as pd
from salesforce_credential import USERNAME, PASSWORD, CONSUMER_KEY, CONSUMER_SECRET, DOMAIN_NAME

CLIENT_FILE = 'client-secret.json'
site_url = 'https://learndataanalysis.org/'

sconsole = GoogleSearchConsole(CLIENT_FILE, site_url)
sconsole.initService()

dimensions = ['date', 'page', 'query']
response = sconsole.query(
    '2022-05-01',
    '2022-05-31',
    dimensions=dimensions,
    row_limit=10,
    start_row=0
)
df = pd.DataFrame(response[1])
df = pd.concat([df['keys'].apply(pd.Series), df.iloc[:, 1:]], axis=1)
df.rename(columns={df.columns[i]: dimensions[i] for i in range(len(dimensions))}, inplace=True)
print(df)
```

#### Querying report from Salesforce

```python
import pandas as pd
from jj_data_connector.yt_analytics import YTAnalytics, CoreDimensions, SubDimensions, CoreMetrics, SubMetrics
from jj_data_connector.gsc import GoogleSearchConsole
from jj_data_connector.ga4 import GA4RealTimeReport, GA4Report, Metrics, Dimensions
from jj_data_connector.sfdc import SalesforceAPI

from salesforce_credential import USERNAME, PASSWORD, CONSUMER_KEY, CONSUMER_SECRET, DOMAIN_NAME

sfdc = SalesforceAPI(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD, DOMAIN_NAME)
access_token = sfdc.generate_access_token()

object_record_count = sfdc.record_count(['account', 'opportunity'])
records = sfdc.run_soql_query('SELECT FIELDS(ALL) FROM Account LIMIT 10')
df_soql = pd.DataFrame(records)
print(object_record_count)
print(df_soql)
```

#### Querying report from Google Analytics 4 (GA4)

```python
import os
import pandas as pd
from jj_data_connector.yt_analytics import YTAnalytics, CoreDimensions, SubDimensions, CoreMetrics, SubMetrics
from jj_data_connector.gsc import GoogleSearchConsole
from jj_data_connector.ga4 import GA4RealTimeReport, GA4Report, Metrics, Dimensions

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_acct.json'  
property_id = '<property id>'
lst_dimension = ['country', 'city', 'deviceCategory']
lst_metrics = ['activeUsers', 'sessions']

ga4_realtime = GA4RealTimeReport(property_id)
ga4 = GA4Report(property_id)
report = ga4.run_report(
    lst_dimension, lst_metrics, 
    date_ranges=[('2022-04-01', '2022-04-30'), ('2022-05-01', '2022-05-31')], 
    row_limit=100,
    offset_row=0
)
df = pd.DataFrame(data=report['rows'], columns=report['headers'])
print(df)

```
