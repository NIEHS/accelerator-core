import json
import os
import shutil

import logging
import uuid

from airflow.sdk import Variable


# from airflow.models import Variable


logger = logging.getLogger(__name__)


class XcomProperties:
    """
    Properties around xcom, particularly whether and how passing via reference to temp files is done
    """

    def __init__(self):
        self.temp_files_supported = False
        self.temp_files_location = None


class XcomPropsResolver:
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

    def __init__(self, temp_files_supported: bool, temp_files_location: str):

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
        self.temp_files_supported = Variable.get(
            "accelerator.xcom.tempfiles.supported", default_var=False
        )
        self.temp_files_location = Variable.get(
            "accelerator.xcom.tempfile.path", default_var=None
        )

    def get_xcom_props(self) -> XcomProperties:
        props = XcomProperties()
        props.temp_files_supported = self.temp_files_supported
        props.temp_files_location = self.temp_files_location
        return props


class XcomUtils:
    """
    Utility class for handling XCOM data, allowing storage of xcom values to temporary file storage. Also provides
    storage of ephemeral files for general usage
    """

    def __init__(self, resolver: XcomPropsResolver = None):
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

    def delete_temp_data(self, file_name):
        """
        Deletes a temporary file from the system to free up storage or maintain
        system cleanliness. Specifically removes the file identified by its name
        from the temporary storage directory.

        This is just a wrapper around the remove but allows later abstraction of temp file storage

        Args:
            file_name (str): The name of the temporary file to be deleted. It
                should include the file extension if applicable.


        """

        os.remove(file_name)

    def store_temp_data(self, file_contents_buf) -> str:
        """
        Stores temporary data and generates a unique file name for it.
        This method creates a UUID to uniquely identify a temporary file and then
        delegates the storage to another method, ensuring that the data is stored
        with the generated unique name.

        Args:
            file_contents_buf: The contents of the temporary file to be stored.

        Returns:
            str: The name of the temporary file in which the data is stored.
        """
        myuuid = uuid.uuid4()
        file_name = str(myuuid)
        return self.store_temp_data_by_name(file_name, file_contents_buf)

    def store_temp_data_by_name(self, filename, file_contents_buf) -> str:
        """
        Stores temporary data in the specified directory. This method ensures the
        provided directory exists, creates it if necessary, and writes file
        contents into a temporary file. Additionally, it handles cases where the
        file already exists by deleting it before writing.

        Parameters:
            filename: str
                The name of the file to be created or overwritten in the
                temporary files directory.
            file_contents_buf: bytes
                The binary data to be written to the file.

        Returns:
            str: The full file path where the data has been stored.

        Raises:
            Exception: If temporary files are not supported by the system.
            Exception: If the temporary files directory is not provided or empty.
        """

        if not self.is_tempfiles_supported():
            raise Exception("temp files not supported")

        if not self.get_tempfiles_location():
            raise Exception("temp files dir not provided")

        temp_files_location = self.get_tempfiles_location()
        if temp_files_location.endswith("/"):
            temp_files_location = temp_files_location[:-1]

        dirpath = f"{self.xcom_properties.temp_files_location}/cache"
        if not os.path.exists(dirpath):
            # if the demo_folder directory is not present
            # then create it.
            os.makedirs(dirpath)

        file_path = os.path.join(dirpath, filename)

        if os.path.exists(file_path):
            "File already exists, delete it"
            logger.debug(f"File already exists, deleting it: {file_path}")
            os.remove(file_path)

        with open(file_path, "wb") as binary_file:
            binary_file.write(file_contents_buf)

        return file_path

    def resolve_task_dir(self, runid: str) -> str:
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

    def store_dict_in_temp_file(self, key: str, json_value: dict, runid: str) -> str:
        """
        Store a dictionary into the temp file (as json)
        @param key: the key to store in a file (leave off the file extension)
        @param json_value: the value to store as a dict
        @return: the path of the temp file to pass in xcom_properties
        """

        filename = f"{runid}-{key}.json"
        filedir = self.resolve_task_dir(runid)

        temp_file_path = os.path.join(filedir, filename)

        with open(temp_file_path, "w") as fp:
            json.dump(json_value, fp)

        return temp_file_path

    def retrieve_dict_from_temp_file(self, temp_file_path: str) -> dict:
        """
        Retrieve the dictionary of xcom values from a temp file
        """

        json_dict = json.load(open(temp_file_path))
        return json_dict

    def clear_temp_data_for_run(self, runid: str):
        """
        Clear the temp directory for this run
        """
        temp_files_location = self.get_tempfiles_location()
        if temp_files_location.endswith("/"):
            temp_files_location = temp_files_location[:-1]

        dirpath = f"{self.xcom_properties.temp_files_location}/{runid}"
        shutil.rmtree(dirpath)
