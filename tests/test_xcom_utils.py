import os
import shutil
import unittest

from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver, XcomUtils


class TestXcomUtil(unittest.TestCase):
    def test_store_dict(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_store_dict"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=True, temp_files_location=temp_dirs_path)
        xcom_utils = XcomUtils(xcom_props_resolver)
        file = xcom_utils.store_dict_in_temp_file(key=file_key, json_value=my_vals,runid=runid )
        self.assertTrue(os.path.exists(file))
        os.remove(file)

    def test_clear_temp_data_for_run(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_clear_temp_data_for_run"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=True, temp_files_location=temp_dirs_path)
        xcom_utils = XcomUtils(xcom_props_resolver)
        file = xcom_utils.store_dict_in_temp_file(key=file_key, json_value=my_vals, runid=runid)
        xcom_utils.clear_temp_data_for_run(runid=runid)
        self.assertFalse(os.path.exists(file))

    def test_retrieve_dict_from_temp_file(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_retrieve_dict_from_temp_file"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=True, temp_files_location=temp_dirs_path)
        xcom_utils = XcomUtils(xcom_props_resolver)
        file = xcom_utils.store_dict_in_temp_file(key=file_key, json_value=my_vals, runid=runid)
        actual = xcom_utils.retrieve_dict_from_temp_file(file)
        self.assertEqual(my_vals, actual)


if __name__ == '__main__':
    unittest.main()
