from azure.cosmos import CosmosClient
from flask import Flask, jsonify, render_template, request ,redirect

COSMOS_URI = "https://cosmosdb-user123.documents.azure.com:443/"
COSMOS_KEY = "V620s0XxckARoXXbBD6BM9eBttdGmTUYkHWffivDxTmnzICNu0opkD8CHV36BkH7D7vHwdDgvJx8ACDbPQ1zBg=="

DATABASE_NAME = "cosmos-db"
CONTAINER_NAME = "cosmos-container"

PARTITION_KEY_FIELD = "/state"


client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

print("Connected to Cosmos DB successfully!")

app = Flask(__name__)

@app.route("/")
def Index():
    #lst = []
    query = "SELECT * FROM c"
    items = container.query_items(
    query=query,
    enable_cross_partition_query=True
    )

#   print(items)
    # for item in items:
    #     lst.append(item)
        

    return render_template('index.html', data=items)


@app.route('/create', methods=['POST'])
def create():
    id = request.form.get('id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    state = request.form.get('state')
    
    item = {
    "id": id,
    "firstname": firstname,
    "lastname": lastname,
    "state": state
    }
    container.upsert_item(item)

    return redirect('/')

# item = {
#     "id": "107",
#     "firstname": "Rahul",
#     "lastname": "Roy",
#     "city": "Ahmedabad",
#     "state": "Gujarat"
# }

# container.upsert_item(item)
# print("Item Inserted Successfully....!")

# query = "SELECT * FROM c"
# items = container.query_items(
#     query=query,
#     enable_cross_partition_query=True
# )

# # print(items)
# for item in items:
#     print(item)

# updated_item = {
#     "id": "202",
#     "firstname": "Prem",
#     "lastname": "Ramchandani",
#     "city": "Bengaluru",
#     "state": "Karnataka"
# }

# container.upsert_item(updated_item)
# print("Item updated!")


# container.delete_item(
#     item="202",
#     partition_key="Karnataka"
# )
# print("Deleted Successfully....")

if __name__ == "__main__":
    app.run(debug=True)
