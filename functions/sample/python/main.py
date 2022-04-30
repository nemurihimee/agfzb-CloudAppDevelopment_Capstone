#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("n7AkBVN2-5nan58pB6VwWmiY2EzxkkBqKoMc7GMdeWBF")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://77d8d6d4-4b5a-4aac-9899-bc42710a75c2-bluemix.cloudantnosqldb.appdomain.cloud")
    
    responce = service.post_find(
        db='reviews',
        selector={'dealership': {'$eq':int(dict['id'])}},
    ).get_result()
    

    try:
        result ={
           'headers':{'Content-Type': 'application/json'},
           'body':{'data':responce}
       }
        return result
    except:
        return {
            "statusCode": 404,
            'message': "Something went wrong"
            }
    
def main(dict):
    authenticator = IAMAuthenticator("n7AkBVN2-5nan58pB6VwWmiY2EzxkkBqKoMc7GMdeWBF")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://77d8d6d4-4b5a-4aac-9899-bc42710a75c2-bluemix.cloudantnosqldb.appdomain.cloud")  
    
    document: Document = Document()
    
    document.id = dict['review']['id']
    document.name = dict['review']['name']
    document.dealership = dict['review']['dealership']
    document.review = dict['review']['review']
    document.purchase = dict['review']['purchase']
    document.another = dict['review']['another']
    document.purchase_date = dict['review']['purchase_date']
    document.car_make = dict['review']['car_make']
    document.car_model = dict['review']['car_model']
    document.car_year = dict['review']['car_year']

    responce = service.post_document(db = 'reviews', document=dict).get_result()

    try:
        result ={
           'headers':{'Content-Type': 'application/json'},
           'body':{'data':responce}
       }
        return result
    except:
        return {
            "statusCode": 500,
            'message': "Something went wrong"
            }
