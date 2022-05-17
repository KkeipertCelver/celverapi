# AUTOGENERATED! DO NOT EDIT! File to edit: 21_boardstorage.ipynb (unless otherwise specified).

__all__ = ['ApiKey', 'ContentType', 'get_forecast', 'IDENTITY_PATH', 'QUERY_PATH', 'Client', 'query', 'cubes',
           'entities', 'entity', 'procedure_run', 'procedure_status', 'human_readable_size', 'Client',
           'list_directories_and_files', 'delete_file', 'download_file', 'upload_file', 'get_file_size']

# Cell

from nbdev.showdoc import *
import pandas as pd
import requests

# Cell
ApiKey='37QNHAHY6SEXQ4N3R8MMQYZ3T'
ContentType="json"

# Cell

"get_forecast returns a DataFrame from a given Forecast"

def get_forecast(city: str, start_date: str, end_date: str, UnitGroup: str):

    """
    The function takes 4 Parameters:

    - City(String) : The name of the city you want to Forecast
    - Start_date(String) : The starting date YYYY-MM-DD
    - End_date(String) : The ending date YYYY-MM-DD
    - UnitGroup = metric"

    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup={UnitGroup}&include=current&key={ApiKey}&contentType={ContentType}"
    response = requests.get(url).json()

    # ---- Converts the JSON response into a Pandas DataFrame
    # ---- Every Day is line in the Pandas DataFrame

    df = pd.json_normalize(response['days'])

    return df




# Cell

from datetime import datetime
import json
import logging
import requests

# Cell
IDENTITY_PATH = "/identity/connect/token"
QUERY_PATH = "/public/"

# Cell

logging.getLogger(__name__).addHandler(logging.NullHandler())

class Client():  # pylint: disable=too-few-public-methods
    """
    simple client to run queries and processes using the Board APIs.
    See related documentation when creating External Queries in a Board Datamodel

    """

    # initialize a new Client object - will retrieve and store bearer token
    def __init__(self, endpoint, client_id, client_secret, scope):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

        # generate and store access token in self.token
        try:
            auth_url = self.endpoint + IDENTITY_PATH
            result = requests.post(
                auth_url,
                data={
                    'grant_type': 'client_credentials',
                    'scope': self.scope,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                }
            )
            self.token = json.loads(result.text)['access_token']
            logging.debug("Board API - Host: {} - Client ID: {} - token generated".format(self.endpoint,self.client_id))

        except Exception as error:
            logging.error("Board API - Host: {} - Client ID: {} - error generating token: {}".format(self.endpoint,self.client_id,str(error)))
            raise

    # call board api - GET request
    def __api_call_get(self,query):
        """Run API Call - Get"""
        try:
            result = requests.get(
                self.endpoint + query,
                headers={
                    "Authorization":"Bearer " + self.token
                }
            )
            logging.debug("Board API - Host: {} - Client ID: {} - GET request: {} - executed succesfully".format(self.endpoint,self.client_id,query))
            return result.text

        except Exception as error:
            logging.error("Board API - Host: {} - Client ID: {} - GET request: {} - error: {}".format(self.endpoint,self.client_id,query,str(error)))
            raise
        pass

    # call board api - POST request
    def __api_call_post(self,query):
        """Run API Call"""
        try:
            result = requests.post(
                self.endpoint + query,
                headers={
                    "Authorization":"Bearer " + self.token,
                    "Accept":"application/json"
                }
            )
            logging.debug("Board API - Host: {} - Client ID: {} - POST request: {} - executed succesfully".format(self.endpoint,self.client_id,query))
            return result.text

        except Exception as error:
            logging.error(
                "Board API\tHost: %s\tQuery: %s\tStatus: Error\tMessage: %s",
                self.endpoint, query, str(error)
            )
            raise
        pass




# Cell

def query(self, datamodel: str, query_name: str, query_string= str):

        """
        Execute a datamodel external query and returns
        a python dictionary with the data from Board.

        The Function takes 3 Parameters:

        -       datamodel(String) : Name of the Board Database
        -       query_name(String) : Name of the Query
        -       query_string(String) : Query in String Format


        """

        query = QUERY_PATH + "/" + datamodel + "/query/" + query_name + query_string

        return self.__api_call_get(query)

# Cell

def cubes(self, datamodel: str):

    """
    Return list of cubes for specified datamodel.

    The Function takes 1 Parameter:

    -   datamodel(String) : Name of the Board Database

    """

    query = QUERY_PATH + "/" + datamodel + "/schema/Cubes"

    return self.__api_call_get(query)

# Cell

def entities(self,datamodel: str):

    """
    Return list of entities for specified datamodel.

    The Function takes 1 Parameter:

    -   datamodel(String) : Name of the Board Database

    """

    query = QUERY_PATH + "/" + datamodel + "/schema/Entities"

    return self.__api_call_get(query)

# Cell

def entity(self,datamodel: str,entity: str):

    """
    Return entity members for specified entity.

    The Function takes 2 Parameters:

    -   datamodel(String) : Name of the Board Database
    -   entity(String) : Name of the specified entity

    """

    query = QUERY_PATH + "/" + datamodel + "/schema/Entities/" + entity

    return self.__api_call_get(query)

# Cell

def procedure_run(self,datamodel: str,procedure: str):

    """
    Execute a Board Procedure and returns Session ID of the execution.

    The Function takes 2 Parameters:

    -   datamodel(String) : Name of the Board Database
    -   procedure(String) : Board Procedure

    """

    query = QUERY_PATH + "/" + datamodel + "/procedure/Execute/" + procedure

    return self.__api_call_post(query)

# Cell

def procedure_status(self,datamodel: str ,session: str):

    """
    Return status of the execution of a Board Procedure

    The Function takes 2 Parameters:

    -   datamodel(String) : Name of the Board Database
    -   session(String) : Session

    """

    query = QUERY_PATH + "/" + datamodel + "/procedure/Status/" + session

    return self.__api_call_get(query)

# Cell

import logging
from azure.storage.file import FileService
from datetime import datetime

# Cell

def human_readable_size(size, decimal_places=2):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"

class Client(): # pylint: disable=too-few-public-methods

    """simple client to access and execute basic operations on the Board Shared Storage"""

    def __init__(self, sas_uri):
        # split sas uri to get token and account
        self.azure_token = sas_uri[sas_uri.find("bss?")+4:]
        self.azure_account = sas_uri[8:sas_uri.find(".file")]
        self.azure_share = "bss"
        self.azfs = FileService(                     # create file service to access board extractions
            account_name=self.azure_account,
            sas_token=self.azure_token,
            socket_timeout=10
        )

# Cell

def list_directories_and_files(self,azure_dir=None):

    """List all files and directories in a Board Shared Storage path
    if no path specified, runs at root level"""

    return self.azfs.list_directories_and_files(self.azure_share,azure_dir)


# Cell

def delete_file(self,azure_file,azure_dir=None):

    """Delete a file from the Board Shared Storage"""

    self.azfs.delete_file(self.azure_share,azure_dir,azure_file)

# Cell

def download_file(self,azure_file,local_path,azure_dir=None,):

    """Download a file from the Board Shared Storage
    If content is set to true, return the full content and not just reference to the file"""

    self.azfs.get_file_to_path(self.azure_share,azure_dir,azure_file,local_path)

# Cell

def upload_file(self,azure_file,local_path,azure_dir=None):

    self.azfs.create_file_from_path(self.azure_share,azure_dir,azure_file,local_path)

# Cell

def get_file_size(self,azure_file,azure_dir,readable = True):

    """return size in bytes of a file on the Board Shared Storage
    if readable set to True, return in a human readable format (e.g. 10GiB)"""

    fileinfo = self.azfs.get_file_properties(self.azure_share,azure_dir,azure_file)

    if readable:

        return human_readable_size(fileinfo.properties.content_length)

    else:

        return fileinfo.properties.content_length