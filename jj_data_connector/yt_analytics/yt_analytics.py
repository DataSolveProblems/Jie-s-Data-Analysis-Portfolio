from typing import List
from .data_model import CoreDimensions, SubDimensions, CoreMetrics, SubMetrics
from ..google_apis import create_service


class YTAnalyticsException(Exception):
    """YT Analytics Exception Base"""

class YTAnalytics:
    SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly',
              'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
              'https://www.googleapis.com/auth/youtubepartner',
              'https://www.googleapis.com/auth/youtube']
    API_NAME = 'youtubeAnalytics'
    API_VERSION = 'v2'

    def __init__(self, client_secret_file):
        self.client_secret_file = client_secret_file
        self.service = None
       
    def initService(self, prefix=None):
        try:
            self.service = create_service(self.client_secret_file, self.API_NAME, self.API_VERSION, self.SCOPES, prefix=prefix)
        except Exception as e:
            print(e)

    def query(self, start_date: str, end_date: str, metrics_list: List[str], 
        dimensions_list: List[str]=None, max_results: int=1000, start_index: int=1, filters: str=None):

        if self.service is None:
            raise YTAnalyticsException('YouTube service is not available')

        try:
            if not isinstance(metrics_list, list):
                raise YTAnalyticsException('metrics_list must be a list')
            else:
                metrics = ','.join(metrics_list)

            if dimensions_list is not None:
                if not isinstance(dimensions_list, list):
                    raise YTAnalyticsException('dimensions_list must be a list')
                else:    
                    dimensions = ','.join(dimensions_list)
            else:
                dimensions = None

            response = yt.service.reports().query(
                ids='channel==Mine',
                startDate=start_date,
                endDate=end_date,
                metrics=metrics,
                dimensions=dimensions,
                maxResults=max_results,
                startIndex=start_index,
                filters=filters
                # access_token: saved for API Playground to access brand account
            ).execute()
            
            columns = [column['name'] for column in response['columnHeaders']]
            rows = response['rows']
            return (columns, rows)
        except Exception as e:
            raise YTAnalyticsException(e)