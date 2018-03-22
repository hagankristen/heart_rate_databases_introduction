from pymodm import connect, errors
import models
import datetime
import numpy as np


def add_heart_rate(email, heart_rate, time):
    # Get the first user where _id=email
    user = models.User.objects.raw({"_id": email}).first()
    # Append the heart_rate to the user's list of heart rates
    user.heart_rate.append(heart_rate)
    # append the current time to the user's list of heart rate times
    user.heart_rate_times.append(time)
    user.save()  # save the user to the database


def create_user(email, age, heart_rate):
    u = models.User(email, age, [], [])  # create a new User instance
    u.heart_rate.append(heart_rate)  # add initial heart rate
    # add initial heart rate time
    u.heart_rate_times.append(datetime.datetime.now())
    u.save()  # save the user to the database


def print_user(email):
    # Get the first user where _id=email
    user = models.User.objects.raw({"_id": email}).first()
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)


def validate_user(input_json):
    try:
        email_key = input_json["user_email"]
        age_key = input_json["user_age"]
        heart_rate_key = input_json["heart_rate"]
        email_flag = isinstance(email_key, str)
        age_flag = isinstance(age_key, int)
        heart_rate_flag = isinstance(heart_rate_key, int)
        if not email_flag or not age_flag or not heart_rate_flag:
            raise TypeError
        print('Input data verified.')
        return email_key, age_key, heart_rate_key
    except KeyError:
        print('Input fails validation. Include email, age, and HR.')
        raise KeyError
    except TypeError:
        print('Input fails validation. Check data types.')
        raise TypeError


def validate_interval(input_json):
    try:
        email_key = input_json["user_email"]
        since_key = input_json["heart_rate_average_since"]
        email_flag = isinstance(email_key, str)
        since_flag = isinstance(since_key, str)
        since_key = datetime.datetime.strptime(
            since_key, "%Y-%m-%d %H:%M:%S.%f")
        if not email_flag or not since_flag:
            raise TypeError
        print('Input data verified.')
        return email_key, since_key
    except KeyError:
        print('Input fails validation. Include email and interval.')
        raise KeyError
    except TypeError:
        print('Input fails validation. Check data types.')
        raise TypeError
    except:
        print('Check format of inputs.')
        raise UnknownError

def calculate_interval_avg(user, t):
    hrs = user.heart_rate
    times = user.heart_rate_times
    hrs_np = np.array(hrs)
    times_np = np.array(times)
    mask = (times_np >= datetime.datetime(t))
    hrs_count = hrs_np[mask]
    if hrs_count.size is 0:
        raise ValueError
    return np.mean(hrs_count)


def check_tachycardia(hr, age):
    tachy_flag = False
    if ((age <= 2) & (hr > 151)):
        tachy_flag = True
    if ((age is 3 or age is 4) & (hr > 137)):
        tachy_flag = True
    if ((age >= 5 and age <= 7) & (hr > 133)):
        tachy_flag = True
    if ((age >= 8 and age <= 11) & (hr > 130)):
        tachy_flag = True
    if ((age >= 12 and age <= 15) & (hr > 119)):
        tachy_flag = True
    if ((age > 15) & (hr > 100)):
        tachy_flag = True
    return tachy_flag

# if __name__ == "__main__":
#    connect("mongodb://vcm-3580.vm.duke.edu:27017/heart_rate_app")
#    create_user(email="kristen.hagan@duke.edu", age=23, heart_rate=60)
#    add_heart_rate("kristen.hagan@duke.edu", 100, datetime.datetime.now())
#    print_user("kristen.hagan@duke.edu")
