import requests
import pandas as pd
import src.utils as utils
from unittest.mock import patch

# pytest --cov=src.utils
# coverage html

# A sample response XML string for testing
sample_xml_response = """<root>
    <data>
        <item1>Value1</item1>
        <item2>Value2</item2>
    </data>
</root>"""


def test_return_data_response_successful():
    url = "http://example.com/api/data"

    # Mock the 'requests.get' function to return a successful response
    with patch.object(requests, "get", return_value=MockResponse(200, sample_xml_response)):
        data_dict = utils.return_data_response(url)

    assert isinstance(data_dict, dict)
    assert "root" in data_dict


def test_return_data_response_failed():
    url = "http://example.com/api/data"

    # Mock the 'requests.get' function to return a failed response
    with patch.object(requests, "get", return_value=MockResponse(404, "Not Found")):
        data_dict = utils.return_data_response(url)

    assert data_dict is None


sample_json_response = {
    "MRData": {"RaceTable": {"Race": {"ResultsList": {"Result": [{"@position": "1", "Laps": 54}]}}}}
}


def test_get_number_of_laps_done():
    year_race = 2023
    round_race = 5
    base_url = "http://example.com/api/f1/"

    # Mock the 'return_data_response' function to return a sample response
    with patch.object(utils, "return_data_response", return_value=sample_json_response):
        number_of_laps = utils.get_number_of_laps_done(year_race, round_race, base_url)

    assert number_of_laps == 54  # Expecting 54 laps made by the driver in the first position


data = {
    "@time": ["01:30.500", "02:45.123", "00:59.999"],
}
sample_df = pd.DataFrame(data)


def test_laptimes_to_seconds():
    result_df = utils.laptimes_to_seconds(sample_df)

    expected_data = {
        "@time": [90.5, 165.123, 59.999],
    }
    expected_df = pd.DataFrame(expected_data)

    assert result_df.equals(expected_df)


# A helper class to mock HTTP responses
class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content
