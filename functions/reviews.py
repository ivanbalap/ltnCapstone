from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.error import CloudantException
from flask import Flask, jsonify, request, abort
import atexit
import json
#Add your Cloudant service credentials here
# cloudant_username = ''
# cloudant_password = ''
# cloudant_url = ''

# client = Cloudant(cloudant_username, cloudant_password, url=cloudant_url, connect=True)

with open("./.creds.json") as creds:
    param_dict=json.load(creds)

client = Cloudant.iam(
    account_name=param_dict["COUCH_USERNAME"],
    api_key=param_dict["IAM_API_KEY"],
    connect=True,
)
print(f"Databases: {client.all_dbs()}")

session = client.session()
# print('Username: {0}'.format(session['userCtx']['name']))
print('Username: {0}'.format(session))
print('Databases: {0}'.format(client.all_dbs()))

db = client['reviews']

app = Flask(__name__)

@app.route('/api/review', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('id')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    if len(data_list) == 0:
        return jsonify({"404": f"dealerId {dealership_id} does not exist"}), 404
    
    return jsonify(data_list)


@app.route('/api/review', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')
    
    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
