from typing import List
from ..google_apis import create_service

class GoogleSearchConsoleException(Exception):
    """Google Search Console Exception base class"""

class GoogleSearchConsole:
    API_VERSION = 'v1'
    API_NAME = 'searchconsole'
    SCOPES = ['https://www.googleapis.com/auth/webmasters']

    def __init__(self, client_file, site_url):
        self.client_file = client_file
        self.service = None
        self.site_url = site_url
       
    def initService(self, prefix=None):
        try:
            self.service = create_service(self.client_file, self.API_NAME, self.API_VERSION, self.SCOPES, prefix=prefix)
        except Exception as e:
            print(e)

    def query(self, start_date: str, end_date: str, 
        dimensions: List[str]=None, search_type: str='web', row_limit: int=3000,
        start_row: int=0, data_state: str='all'):
        """
        :param start_date: Start date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00).
        :param end_date: End date of the requested date range, in YYYY-MM-DD format, in PT time.
        :param dimensions: Zero or more dimensions to group results by: country, device, page, query, date, searchAppearance.
        :param search_type: filter result type: discover, googleNews, news, image, video, web
        :param row_limit: Valid range is 1–25,000; Default is 1,000] The maximum number of rows to return. 
        :param start_row: Optional; Default is 0] Zero-based index of the first row in the response. Must be a non-negative number. 
            If startRow exceeds the number of results for the query, the response will be a successful response with zero rows.
        :param date_state: [Optional] If "all" (case-insensitive), data will include fresh data. If "final" (case-insensitive) or 
            if this parameter is omitted, the returned data will include only finalized data.
        """
        if self.service is None:
            raise GoogleSearchConsoleException('Google Search Console service is not available')

        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'type': search_type,
            'rowLimit': row_limit,
            'startRow': start_row,
            'dataState': data_state
        }
        try:
            response = self.service.searchanalytics().query(
                siteUrl=self.site_url,
                body=request_body
            ).execute()
            return (dimensions, response['rows'])

        except Exception as e:
            raise GoogleSearchConsoleException(e)

    # def removeService(self)        
    #     token_searchconsole_v1None.pickle