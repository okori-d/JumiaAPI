#!/home/okori/pythonproject/unicart_env/bin/python

from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to the MongoDB cluster
client = MongoClient("mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority")

# Access the first MongoDB database
db1 = client["database1"]

# Access the second MongoDB database
db2 = client["scraped_data"]

# Collection names
collection1_name = "jijiProducts"  # Collection for jiji products
collection2_name = "products"  # Collection for jumia products


# Routes

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/all", methods=["GET"])
def get_all_items():
    # Get all items from both collections
    collection1 = db1[collection1_name]
    collection2 = db2[collection2_name]

    #Projection documents to show what is included and what isn't
    collection1_data = [document for document in collection1.find({}, {"_id": 0, "image": 1, "name": 1, "price": 1})]
    collection2_data = [document for document in collection2.find({}, {"_id": 0, "image": 1, "name": 1, "price": 1})]

    result = {
        "collection1": collection1_data,
        "collection2": collection2_data
    }

    return jsonify(result)


@app.route("/item/<collection>/<item_id>", methods=["GET"])
def get_item(collection, item_id):
    # Retrieve item details from the specified collection and item_id
    if collection == "collection1":
        collection_name = collection1_name
        database = db1
    elif collection == "collection2":
        collection_name = collection2_name
        database = db2
    else:
        return jsonify({"error": "Invalid collection"})

    collection = database[collection_name] #Here. What's this meant to do. Since now I have db1 and db2.
    item = collection.find_one({"_id": item_id})

    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"})


if __name__ == "__main__":
    app.run(debug=True)
