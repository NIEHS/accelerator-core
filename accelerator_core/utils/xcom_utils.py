import json
import os
import shutil

from airflow.models import Variable


class XcomProperties():
    """
    Properties around xcom, particularly whether and how passing via reference to temp files is done
    """

    def __init__(self):
        self.temp_files_supported = False
        self.temp_files_location = None


class XcomPropsResolver():
    """
    Injectable handler for resolving xcom properties, this is the base class
    """

    def get_xcom_props(self) -> XcomProperties:
        """
        Return the resolved xcom properties
        @return: the resolved XcomProperties
        """
        pass

class DirectXcomPropsResolver(XcomPropsResolver):
    """
        Resolver directly passes values (esp for testing)
        """
    def __init__(self, temp_files_supported:bool, temp_files_location:str):

        super().__init__()
        self.temp_files_supported = temp_files_supported
        self.temp_files_location = temp_files_location

    def get_xcom_props(self) -> XcomProperties:
        props = XcomProperties()
        props.temp_files_supported = self.temp_files_supported
        props.temp_files_location = self.temp_files_location
        return props


class AirflowXcomPropsResolver(XcomPropsResolver):
    """
    Resolver obtains values from airflow variables
    """

    def __init__(self):
        super().__init__()
        self.temp_files_supported = Variable.get("accelerator.xcom.tempfiles.supported", default_var=False)
        self.temp_files_location = Variable.get("accelerator.xcom.tempfile.path", default_var=None)

    def get_xcom_props(self) -> XcomProperties:
        props = XcomProperties()
        props.temp_files_supported = self.temp_files_supported
        props.temp_files_location = self.temp_files_location
        return props


class XcomUtils():
    """
    Utility class for handling XCOM data, allowing storage of xcom values to temporary file storage
    """

    def __init__(self, resolver:XcomPropsResolver=None):
         self.resolver = resolver
         self.xcom_properties = self.resolver.get_xcom_props()

    def is_tempfiles_supported(self) -> bool:
        """
        Ask whether passing temp files is supported
        @return: True if temp files are supported
        """
        return self.xcom_properties.temp_files_supported

    def get_tempfiles_location(self) -> str:
        """
        Return the location of the temp files, or None if no temp files supported
        @return: the location of the temp files, or None if no temp files supported
        """
        return self.xcom_properties.temp_files_location

    def resolve_task_dir(self, runid:str) -> str:
        """
        Get the directory path that corresponds to this task, creating it if necessary
        """

        if not self.is_tempfiles_supported():
            raise Exception("temp files not supported")

        if not self.get_tempfiles_location():
            raise Exception("temp files dir not provided")

        temp_files_location = self.get_tempfiles_location()
        if temp_files_location.endswith("/"):
            temp_files_location = temp_files_location[:-1]

        dirpath = f"{self.xcom_properties.temp_files_location}/{runid}"
        if not os.path.exists(dirpath):
            # if the demo_folder directory is not present
            # then create it.
            os.makedirs(dirpath)

        return dirpath

    def store_dict_in_temp_file(self, key:str, json_value:dict, runid:str) -> str:
        """
        Store a dictionary into the temp file (as json)
        @param key: the key to store in a file (leave off the file extension)
        @param json_value: the value to store as a dict
        @return: the path of the temp file to pass in xcom_properties
        """

        filename = f"{runid}-{key}.json"
        filedir = self.resolve_task_dir(runid)

        temp_file_path = os.path.join(filedir, filename)

        with open(temp_file_path, 'w') as fp:
            json.dump(json_value, fp)

        return temp_file_path

    def retrieve_dict_from_temp_file(self, temp_file_path:str) -> dict:
        """
        Retrieve the dictionary of xcom values from a temp file
        """

        json_dict = json.load(open(temp_file_path))
        return json_dict

    def clear_temp_data_for_run(self, runid:str):
        """
        Clear the temp directory for this run
        """
        temp_files_location = self.get_tempfiles_location()
        if temp_files_location.endswith("/"):
            temp_files_location = temp_files_location[:-1]

        dirpath = f"{self.xcom_properties.temp_files_location}/{runid}"
        shutil.rmtree(dirpath)


