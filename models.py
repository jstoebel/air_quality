from datetime import date, datetime
from enum import IntEnum
from typing import Dict, List

from pydantic import BaseModel, Field, validator


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class Category(BaseModel):
    number: int
    name: str

    class Config:
        alias_generator = to_camel

    @property
    def is_healthy(self):
        return self.number < 3


class AirQualityResult(BaseModel):
    date_observed: str
    hour_observed: int
    local_time_zone: str
    reporting_area: str
    state_code: str
    latitude: float
    longitude: float
    parameter_name: str
    aqi: float = Field(alias="AQI")
    category: Category

    class Config:
        alias_generator = to_camel

    @validator("date_observed")
    def parse_date(cls, date_str: str) -> date:
        date_args = (int(piece) for piece in date_str.split("-"))
        return date(*date_args)

    @property
    def category_name(self):
        return self.category.name

    @property
    def category_number(self):
        return self.category.number

    @property
    def is_healthy(self):
        return self.category.is_healthy

    @property
    def observation_date_time(self):
        dt = datetime.combine(self.date_observed, datetime.min.time()).replace(
            hour=self.hour_observed
        )
        return dt.strftime("%c")

    @property
    def report(self):
        return f"{self.parameter_name}: {self.aqi} ({self.category_name}) at {self.observation_date_time}"


class AirQualityResultsList(BaseModel):
    results: List[AirQualityResult]

    @property
    def report(self):
        analysis = (
            "Everything looks good!"
            if self.is_healthy
            else "Air quality doesn't look great!"
        )
        result_reports = [result.report for result in self.results]

        return "\n".join([analysis, *result_reports])

    @property
    def is_healthy(self):
        return all(result.is_healthy for result in self.results)
