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
    assert(c2 == input3["heart_rate_average_since"])
