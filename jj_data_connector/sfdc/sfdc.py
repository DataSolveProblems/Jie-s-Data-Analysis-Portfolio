from typing import List, Dict
from rich.console import Console
import requests
# from credential import USERNAME, PASSWORD, CONSUMER_KEY, CONSUMER_SECRET, DOMAIN_NAME

__version__ = 'v1.1'
__author__ = 'Jie Jenn'

def generate_access_token(consumer_key, consumer_secret, username, password, domain_name):
    json_data = {
        'grant_type': 'password',
        'client_id': consumer_key,
        'client_secret': consumer_secret,
        'username': username,
        'password': password
    }
    response = requests.post(domain_name + '/services/oauth2/token', data=json_data)
    if response.status_code == 200:
        access_token_id = response.json()['access_token']
        print('Access token created')
        return access_token_id
    else:
        print('Error: {0}'.format(response.reason))

class SalesforceAPI:
    SERVICE_URL = '/services/data/v53.0'

    def __init__(self, consumer_key, consumer_secret, username, password, domain_name):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.username = username
        self.password = password
        self.domain = domain_name
        self.access_token = None

    def generate_access_token(self):
        json_data = {
            'grant_type': 'password',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
            'username': self.username,
            'password': self.password
        }
        response = requests.post(self.domain + '/services/oauth2/token', data=json_data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            print('Access token created')
            self.access_token = access_token 
            return access_token
        else:
            print('Error: {0}'.format(response.reason))

    @property
    def headers(self):
        if self.access_token is None:
            print('token is not generated')
            return            
        return {'Authorization': 'Bearer ' + self.access_token}   


    def record_count(self, object_list=[str]):
        params = {
            'sObjects': ','.join(object_list)
        }
        response = requests.get(self.domain + self.SERVICE_URL + '/limits/recordCount', headers=self.headers, params=params)
        return response.json()

    # def api_usage_summary(self):
    #     response = requests.get(self.domain + self.SERVICE_URL + '/limits', headers=self.headers, params=params)
    #     return response.json()        

    def describe_object(self, object_api_name='all'):
        """
        param object_name: if 'all' returns all.
        """
        if object_api_name == 'all':
            response = requests.get(self.domain + self.SERVICE_URL + '/sobjects', headers=self.headers)
        else:
            response = requests.get(self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(response.reason)
            return

    def sObject_get_delete(self, object_api_name, operation, start_date_time, end_date_time):
        """
        Retrieves records that have been deleted within the given timespan for the specified object. 
        :param object_api_name:
        :param operation: {deleted; updated}
        :param start_date_time
        :param end_date_time

        Starting/Ending date/time (Coordinated Universal Time (UTC))
        Use the yyyy-MM-ddTHH:mm:ss.SSS+/-HH:mm or yyyy-MM-ddTHH:mm:ss.SSSZ formats to specify dateTime fields.
        More information: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_valid_date_formats.htm
        """
        params = {
            'start': start_date_time,
            'end': end_date_time
        }
        response = requests.get(self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/' + operation, 
                                headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.reason)
            return
    
    def insert_record(self, object_api_name, field_data: Dict):
        """insert new record
        :param object_api_name:
        :param field_data: Dict object containing field api name and field value
        """
        response = requests.post(self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name, headers=self.headers, json=field_data)
        if response.status_code == 201:
            return response.json()
        else:
            print('Message: {0}'.format(response.json()[0]['message']))
            print('Error Code: {0}'.format(response.json()[0]['errorCode']))
    
    def update_record(self, object_api_name, record_id, field_data: Dict):
        response = requests.patch(self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/' + record_id, headers=self.headers, json=field_data)
        if response.status_code == 204:
            print('Record "{0}" updated.'.format(record_id))
        else:
            print('Message: {0}'.format(response.json()[0]['message']))
            print('Error Code: {0}'.format(response.json()[0]['errorCode']))

    def delete_record(self, object_api_name, record_id):
        """insert new record
        :param object_api_name:
        :param field_data: Dict object containing field api name and field value
        """
        response = requests.delete(self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/' + record_id, headers=self.headers)
        if response.status_code == 204:
            print('Record "{0}" deleted.'.format(record_id))
        else:
            print(response.reason)

    def run_soql_query(self, soql_statement):
        """Run SOQL query query"""
        params = {
            'q': soql_statement
        }
        response_query = requests.get(self.domain + '/services/data/v53.0/query', headers=self.headers, params=params)
        if response_query.status_code != 200:
            console.print('Call failed: {0}'.format(response_query.json()[0]['message']))
            return
        records = []
        records.extend(response_query.json()['records'])
        is_done = response_query.json()['done']
        nextRecordsUrl = response_query.json().get('nextRecordsUrl')
        while not is_done:
            response_query = requests.get(self.domain + '/services/data/v53.0/query/' + nextRecordsUrl, headers=self.headers)
            records.extend(response_query.json()['records'])
            is_done = response_query.json()['done']
            nextRecordsUrl = response_query.json().get('nextRecordsUrl')
        return records

    def batch_delete(self, ids: List[str], roll_back_on_error: bool=False):
        """
        Use a DELETE request with sObject Collections to delete up to 200 records, returning a list of DeleteResult objects. 
        You can choose to roll back the entire request when an error occurs.
        :param ids (Required)
        :param roll_back_on_error (optional): Indicates whether to roll back the entire request when the deletion of any object 
            fails (true) or to continue with the independent deletion of other objects in the request.
        """
        log =[]
        for i in range(0, len(ids), 200):
            params = {
                'ids': ','.join(ids[i: i+200]),
                'allOrNone': roll_back_on_error
            }
            response = requests.delete(self.domain + sf.SERVICE_URL + '/composite/sobjects', headers=sf.headers, params=params)
            log.extend(response.json())
        return log  

    def batch_update(self, records_json: List, roll_back_on_error: bool=False):
        """
        Use a PATCH request with sObject Collections to update up to 200 records, returning a list of UpdateResult objects. 
        You can choose to roll back the entire request when an error occurs.
        :param ids (Required)
        :param roll_back_on_error (optional): Indicates whether to roll back the entire request when the updating of any object 
            fails (true) or to continue with the independent updating of other objects in the request.
        """
        log =[]
        for i in range(0, len(records_json), 200):
            json_data = {
                'allOrNone': roll_back_on_error,
                'records': records_json,
            }
            response = requests.patch(self.domain + sf.SERVICE_URL + '/composite/sobjects', headers=sf.headers, json=json_data)
            log.extend(response.json())
        return log  

    def batch_create(self, records_json: List):
        """
        TODO
        https://developer.salesforce.com/docs/atlas.en-us.218.0.api_rest.meta/api_rest/resources_composite_sobjects_collections_create.htm
        """
        ...

    def batch_upsert(self, records_json: List):
        """
        TODO
        Use a PATCH request with sObject Collections to either create or update (upsert) up to 200 records based on an external ID field. 
        """
        ...

    def objec_relationships(self, object_api_name):
        """
        TODO
        https://developer.salesforce.com/docs/atlas.en-us.218.0.api_rest.meta/api_rest/resources_sobject_relationships.htm
        """
        ...

    def retrieve_listview_list(self, object_api_name):
        """
        Returns the list of list views for the specified sObject, including the ID and other basic 
        information about each list view. You can also get basic information for a specific list view by ID.
        """
        endpoint = self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/listviews'
        response = requests.get(endpoint, headers=sf.headers)
        if response.status_code != 200:
            print(response.reason)
            return
        return response.json()

    def describe_listview(self, object_api_name, listview_id):
        """
        Returns detailed information about a list view, including the ID, the columns, 
        and the SOQL query.
        """
        endpoint = self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/listviews/' + listview_id + '/describe'
        if response.status_code != 200:
            print(response.reason)
            return
        return response.json()

    def retrieve_listview_result(self, object_api_name, listview_id):
        """
        Executes the SOQL query for the list view and returns the resulting data 
        and presentation information.
        """
        endpoint = self.domain + self.SERVICE_URL + '/sobjects/' + object_api_name + '/listviews/' + listview_id + '/results'
        if response.status_code != 200:
            print(response.reason)
            return
        return response.json()

if __name__ == '__main__':
    console = Console()
    # get the latest available API version
    # console.print(requests.get(DOMAIN_NAME + '/services/data').json())

    token_id = generate_access_token()
    # example retrieve object metadata
    headers = {
        'Authorization': 'Bearer ' + token_id
    }    
    sf = SalesforceConnector(headers)
    
    sf.retrieve_listviews('project__c')


    records = []

    endpoint = DOMAIN_NAME + sf.SERVICE_URL + '/composite/tree/opportunity'
    response = requests.get(endpoint, headers=headers)
    response.reason
    console.print(response.json())


