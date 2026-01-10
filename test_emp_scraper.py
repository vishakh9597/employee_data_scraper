import unittest
from unittest.mock import patch, MagicMock
import emp_scraper
class TestEmployeeScraper(unittest.TestCase):

    @patch("emp_scraper.requests.Session.get")
    
    def test_json_download(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1}]
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        data = emp_scraper.fetch_employee_data()
        self.assertTrue(isinstance(data, list))

   
    def test_json_extraction(self):
        sample_data = [{
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "job_title": "Engineer",
            "phone": "1234567890",
            "gender": "Male",
            "age": 30,
            "years_of_experience": 2,
            "salary": 50000,
            "department": "IT"
        }]
        df = emp_scraper.normalize_data(sample_data)
        self.assertEqual(df["Full Name"][0], "John Doe")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            emp_scraper.validate_structure({"id": 1})

    def test_missing_fields(self):
        bad_data = [{"id": 1}]
        with self.assertRaises(ValueError):
            emp_scraper.validate_structure(bad_data)

    def test_invalid_phone_number(self):
        sample_data = [{
            "id": 1,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@test.com",
            "job_title": "Engineer",
            "phone": "123x456",
            "gender": "Female",
            "age": 25,
            "years_of_experience": 1,
            "salary": 40000,
            "department": "HR"
        }]
        df = emp_scraper.normalize_data(sample_data)
        self.assertEqual(df["phone"][0], "Invalid Number")

if __name__ == "__main__":
    unittest.main()
