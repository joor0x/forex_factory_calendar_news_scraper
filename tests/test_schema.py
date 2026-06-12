import json
import unittest
from pathlib import Path
from jsonschema import validate, ValidationError


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.schema_path = self.repo_root / "calendar.schema.json"
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_schema_with_valid_records(self):
        # Test 24h time format
        record_1 = {
            "time": "14:30",
            "timezone": "Asia/Karachi",
            "currency": "USD",
            "impact": "red",
            "impact_level": "high",
            "event": "Core CPI m/m",
            "detail": "https://www.forexfactory.com/calendar?month=June#detail=148363",
            "actual": "0.2%",
            "forecast": None,
            "previous": None,
            "day": "Wed",
            "date": "10/06/2026",
            "datetime_utc": "2026-06-10T09:30:00Z",
            "scraped_at": "2026-06-12T08:12:37.721712+00:00"
        }
        # Test "All Day" time format
        record_2 = record_1.copy()
        record_2["time"] = "All Day"
        record_2["datetime_utc"] = None
        
        # Test "all day" lowercase format
        record_3 = record_1.copy()
        record_3["time"] = "all day"
        record_3["datetime_utc"] = None

        # Test "Tentative" time format
        record_4 = record_1.copy()
        record_4["time"] = "Tentative"
        record_4["datetime_utc"] = None

        # Test "tentative" lowercase format
        record_5 = record_1.copy()
        record_5["time"] = "tentative"
        record_5["datetime_utc"] = None

        validate(instance=[record_1, record_2, record_3, record_4, record_5], schema=self.schema)

    def test_schema_invalid_time(self):
        record = {
            "time": "invalid_time",
            "timezone": "Asia/Karachi",
            "currency": "USD",
            "impact": "red",
            "impact_level": "high",
            "event": "Core CPI m/m",
            "detail": "https://www.forexfactory.com/calendar?month=June#detail=148363",
            "actual": "0.2%",
            "forecast": None,
            "previous": None,
            "day": "Wed",
            "date": "10/06/2026",
            "datetime_utc": "2026-06-10T09:30:00Z",
            "scraped_at": "2026-06-12T08:12:37.721712+00:00"
        }
        with self.assertRaises(ValidationError):
            validate(instance=[record], schema=self.schema)

    def test_schema_invalid_impact(self):
        record = {
            "time": "14:30",
            "timezone": "Asia/Karachi",
            "currency": "USD",
            "impact": "purple",  # Invalid impact color
            "impact_level": "high",
            "event": "Core CPI m/m",
            "detail": "https://www.forexfactory.com/calendar?month=June#detail=148363",
            "actual": "0.2%",
            "forecast": None,
            "previous": None,
            "day": "Wed",
            "date": "10/06/2026",
            "datetime_utc": "2026-06-10T09:30:00Z",
            "scraped_at": "2026-06-12T08:12:37.721712+00:00"
        }
        with self.assertRaises(ValidationError):
            validate(instance=[record], schema=self.schema)

    def test_schema_invalid_date(self):
        record = {
            "time": "14:30",
            "timezone": "Asia/Karachi",
            "currency": "USD",
            "impact": "red",
            "impact_level": "high",
            "event": "Core CPI m/m",
            "detail": "https://www.forexfactory.com/calendar?month=June#detail=148363",
            "actual": "0.2%",
            "forecast": None,
            "previous": None,
            "day": "Wed",
            "date": "2026-06-12",  # Invalid format (ISO-8601 instead of dd/mm/yyyy)
            "datetime_utc": "2026-06-10T09:30:00Z",
            "scraped_at": "2026-06-12T08:12:37.721712+00:00"
        }
        with self.assertRaises(ValidationError):
            validate(instance=[record], schema=self.schema)

    def test_news_calendar_matches_schema(self):
        calendar_path = self.repo_root / "news" / "calendar.json"
        if calendar_path.exists():
            with open(calendar_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            validate(instance=data, schema=self.schema)


if __name__ == "__main__":
    unittest.main()
