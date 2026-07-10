from flask import Flask, request, jsonify

from app.database import collection


app = Flask(__name__)


@app.route("/")
def home():

    return {
        "message":"Python Mongo Application Running"
    }


@app.post("/users")
def save_user():

    data=request.json

    collection.insert_one(data)

    return jsonify(
        {
            "message":"User saved successfully"
        }
    )


@app.get("/users")
def get_users():

    users=list(collection.find({},{"_id":0}))

    return jsonify(users)


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )