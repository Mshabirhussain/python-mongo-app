from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from app.database import collection


app = Flask(__name__)


@app.route("/")
def home():

    employees = list(
        collection.find(
            {},
            {"_id": 0}
        )
    )

    return render_template(
        "index.html",
        employees=employees,
        count=len(employees)
    )


@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form.get("name")
    department = request.form.get("department")


    if name and department:

        collection.insert_one(
            {
                "name": name,
                "department": department
            }
        )


    return redirect(
        url_for("home")
    )



@app.route("/delete/<name>")
def delete_employee(name):

    collection.delete_one(
        {
            "name": name
        }
    )


    return redirect(
        url_for("home")
    )



@app.route("/api/employees")
def api_employees():

    employees = list(
        collection.find(
            {},
            {"_id":0}
        )
    )


    return jsonify(employees)



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )