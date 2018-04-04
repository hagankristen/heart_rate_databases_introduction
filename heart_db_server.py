from flask import Flask, request, jsonify
from flask_cors import CORS

from pymodm import connect, errors
import models
import datetime
from main import add_heart_rate, create_user, print_user
from main import validate_user, validate_interval
from main import check_tachycardia, calculate_interval_avg


app = Flask(__name__)
CORS(app)
comp_with_db = "mongodb://vcm-3580.vm.duke.edu:27017/heart_rate_app"
connect(comp_with_db)


@app.route("/api/heart_rate", methods=["POST"])
def post_user():
    input = request.get_json()
    try:
        email_v, age_v, hr_v = validate_user(input)
        user = models.User.objects.raw({"_id": email_v}).first()
        print('New heart rate added to existing user.')
        add_heart_rate(email_v, hr_v, datetime.datetime.now())
        print_user(email_v)
        done = {"user": email_v,
                "status": "verified and updated",
                "latest heart_rate": hr_v
                }
        return jsonify(done), 200
    except KeyError:
        data = {"message": 'POST to /api/heart_rate failed.'}
        return jsonify(data), 400
    except TypeError:
        data = {"message": 'POST to /api/heart_rate failed.'}
        return jsonify(data), 400
    except errors.DoesNotExist:
        data = {"message": 'New user was created.'}
        create_user(email=email_v, age=age_v, heart_rate=hr_v)
        print_user(email_v)
        return jsonify(data), 400


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_interval_average():
    input = request.get_json()
    try:
        email_v, since_v = validate_interval(input)
        user = models.User.objects.raw({"_id": email_v}).first()
        interval_average = calculate_interval_avg(user.heart_rate,
                                                  user.heart_rate_times,
                                                  since_v)
        tachy_flag = check_tachycardia(interval_average, user.age)
        done = {"user": email_v,
                "status": "verified and average calculated",
                "interval_average": interval_average,
                "tachycardia_check": tachy_flag
                }
        print(done)
        return jsonify(done), 200
    except KeyError:
        data = {"message": 'POST to /api/heart_rate/interval_average failed.'}
        return jsonify(data), 400
    except TypeError:
        data = {"message": 'POST to /api/heart_rate/interval_average failed.'}
        return jsonify(data), 400
    except errors.DoesNotExist:
        data = {"message": 'User does not exist.'}
        return jsonify(data), 400
    except ValueError:
        print('No heart rates recorded since input time.')
        data = {"message": 'No heart rates recorded since input time.'}
        return jsonify(data), 400
    except UnknownError:
        data = {"message": 'UnknownError occured.'}
        return jsonify(data), 400


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_heart_rates(user_email):
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        hi = {"user_email": user_email,
              "recorded_heart_rates": user.heart_rate,
              "hr_times": user.heart_rate_times
              }
        return jsonify(hi), 200
    except errors.DoesNotExist:
        data = {"message": 'User does not exist.'}
        return jsonify(data), 400


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_heart_rate_average(user_email):
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        hi = {"user_email": user_email,
              "average_recorded_heart_rates":
              sum(user.heart_rate)/len(user.heart_rate)
              }
        return jsonify(hi), 200
    except errors.DoesNotExist:
        data = {"message": 'User does not exist.'}
        return jsonify(data), 400

@app.route("/api/heart_rate/userlist", methods=["GET"])
def get_userlist():
    try:
        db.getUsers()
        hi = {"user_emails": 1,
        }
        return jsonify(hi), 200
    except UnknownError:
        data = {"message": 'Problem getting list.'}
        return jsonify(data), 400
