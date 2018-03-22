from pymodm import fields, MongoModel


class User(MongoModel):
    # bc primary_key is True, need to query this field using label _id
    email = fields.EmailField(primary_key=True)
    age = fields.IntegerField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    heart_rate_times = fields.ListField(field=fields.DateTimeField())
