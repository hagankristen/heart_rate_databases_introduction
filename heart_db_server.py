from flask import Flask, request, jsonify
from pymodm import connect, errors
import models
import datetime
from main import add_heart_rate, create_user, print_user
from main import validate_user, validate_interval
from main import check_tachycardia, calculate_interval_avg


app = Flask(__name__)

connect("mongodb://vcm-3580.vm.duke.edu:27017/heart_rate_app")


@app.route("/api/heart_rate", methods=["POST"])
def post_user():
    input = request.get_json()
    try:
        email_v, age_v, hr_v = validate_user(input)
        user = models.User.objects.raw({"_id": email_v}).first()
        print('New heart rate added to existing user.')
        add_heart_rate(email_v, hr_v, datetime.datetime.now())
        done = {"user": email_v,
                "status": "verified and updated",
                "latest heart_rate": hr_v
                }
        return jsonify(done), 200
    except KeyError:
        print('POST to /api/heart_rate failed.')
    except ValidationError:
        print('POST to /api/heart_rate failed.')
    except errors.DoesNotExist:
        print('New user was created.')
        create_user(email=email_v, age=age_v, heart_rate=hr_v)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_interval_average():
    input = request.get_json()
    try:
        email_v, since_v = validate_interval(input)
        user = models.User.objects.raw({"_id": email_v}).first()
        interval_average = calculate_interval_avg(user.heart_rate,
                                                  user.heart_rate_times, since_v)
        tachy_flag = check_tachycardia(interval_average, user.age)
        done = {"user": email_v,
                "status": "verified and average calculated",
                "interval_average": interval_average,
                "tachycardia_check": tachy_flag
                }
        return jsonify(done), 200
    except KeyError:
        print('POST to /api/heart_rate/interval_average failed.')
    except TypeError:
        print('POST to /api/heart_rate/interval_average failed.')
    except errors.DoesNotExist:
        print('User does not exist.')
    except ValueError:
        print('No heart rates recorded since input time.')
    except UnknownError:
        print('UnknownError occured.')


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_heart_rates(user_email):
    user = models.User.objects.raw({"_id": user_email}).first()
    hi = {"user_email": user_email,
          "recorded heart rates": user.heart_rate
          }
    return jsonify(hi), 200


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_heart_rate_average(user_email):
    user = models.User.objects.raw({"_id": user_email}).first()
    hi = {"user_email": user_email,
          "average of recorded heart rates":
          sum(user.heart_rate)/len(user.heart_rate)
          }
    return jsonify(hi), 200
