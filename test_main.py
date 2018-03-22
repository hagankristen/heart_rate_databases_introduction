from pymodm import connect, errors
import models
import datetime
import numpy as np
import pytest
import datetime
from main import add_heart_rate, create_user, print_user
from main import validate_user, validate_interval
from main import check_tachycardia, calculate_interval_avg


def test_validate_user():
    input1 = {
        "user_email": "suyash@suyashkumar.com",
        "user_age": "adult",
        "heart_rate": 100
    }
    with pytest.raises(TypeError):
        a1, a2, a3 = validate_user(input1)
    input2 = {
        "user": "suyash@suyashkumar.com",
        "user_age": 23,
        "heart_rate": 100
    }
    with pytest.raises(KeyError):
        b1, b2, b3 = validate_user(input2)
    input3 = {
        "user_email": "suyash@suyashkumar.com",
        "user_age": 23,
        "heart_rate": 100
    }
    c1, c2, c3 = validate_user(input3)
    assert(c1 == input3["user_email"])
    assert(c2 == input3["user_age"])
    assert(c3 == input3["heart_rate"])


def test_validate_interval():
    input1 = {
        "user_email": "suyash@suyashkumar.com",
        "heart_rate_average_since": 2016
        }
    with pytest.raises(TypeError):
        a1, a2 = validate_interval(input1)
    input2 = {
        "user": "suyash@suyashkumar.com",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339"
        }
    with pytest.raises(KeyError):
        b1, b2 = validate_interval(input2)
    input3 = {
        "user_email": "suyash@suyashkumar.com",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339"
        }
    c1, c2 = validate_interval(input3)
    assert(c1 == input3["user_email"])
    assert(c2 == datetime.datetime.strptime(
        input3["heart_rate_average_since"], "%Y-%m-%d %H:%M:%S.%f"))


def test_calculate_interval_avg():
    hrs = [80, 60, 40]
    t1 = "2018-03-09 10:00:36.372339"
    t2 = "2018-03-09 11:00:36.372339"
    t3 = "2018-03-09 12:00:36.372339"
    s1 = "2018-03-09 10:10:36.372339"
    s2 = "2018-03-10 10:10:36.372339"
    times = [datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f"),
             datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S.%f"),
             datetime.datetime.strptime(t3, "%Y-%m-%d %H:%M:%S.%f")]
    since1 = datetime.datetime.strptime(s1, "%Y-%m-%d %H:%M:%S.%f")
    since2 = datetime.datetime.strptime(s2, "%Y-%m-%d %H:%M:%S.%f")
    interval_average1 = calculate_interval_avg(hrs, times, since1)
    assert(interval_average1 == 50)
    with pytest.raises(ValueError):
        interval_average2 = calculate_interval_avg(hrs, times, since2)


def test_check_tachycardia():
    hr1 = 150
    hr2 = 130
    hr3 = 90
    age1 = 1
    age2 = 3
    age3 = 10
    age4 = 20
    assert(check_tachycardia(hr1, age1) is False)
    assert(check_tachycardia(hr1, age2) is True)
    assert(check_tachycardia(hr2, age1) is False)
    assert(check_tachycardia(hr2, age3) is False)
    assert(check_tachycardia(hr2, age4) is True)
    assert(check_tachycardia(hr3, age1) is False)
    assert(check_tachycardia(hr3, age4) is False)
