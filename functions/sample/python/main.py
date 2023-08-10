"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
# from ibmcloudant import Cloudant
# from ibmcloudant import CloudantException
import requests


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
    param_dict={
        "COUCH_USERNAME":"e19297ca-16b6-4c74-9771-d060d1f7629f-bluemix",
        "IAM_API_KEY":"qXP_0jljqbBazUCO2WDwktLMMwyksDOLy1Gm2i1ZLqUM"
    }
    print(main(param_dict))
