from peewee import CharField, DateTimeField, Model, SqliteDatabase

db = SqliteDatabase("results.db")


class AirQualityResult(Model):
    parameter_name = CharField()
    observation_date_time = DateTimeField()
    level = CharField()

    class Meta:
        database = db


db.create_tables([AirQualityResult])
