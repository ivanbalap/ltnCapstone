"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
# from ibmcloudant import Cloudant
# from ibmcloudant import CloudantException
# from ibmcloudant.cloudant_v1 import CloudantV1
# from ibm_cloud_sdk_core import ApiException
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import json


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

if __name__=='__main__':
    with open("../../.creds.json") as creds:
        # param_dict={
        #     "COUCH_USERNAME":"",
        #     "IAM_API_KEY":""
        # }
        param_dict=json.load(creds)
    print(main(param_dict))
