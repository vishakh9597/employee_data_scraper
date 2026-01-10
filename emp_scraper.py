import requests
import pandas as pd
import logging
import re
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL ="https://api.slingacademy.com/v1/sample-data/files/employees.json"

REQUIRED_FIELDS={
    "id",
    "first_name",
    "last_name",
    "email",
    "job_title",
    "phone",
    "gender",
    "age",
    "years_of_experience",
    "salary",
    "department"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def fetch_employee_data():
    session =requests.Session()
    retry_strategy =Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter=HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    response = session.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def validate_structure(data):
    if not isinstance(data, list):
        raise ValueError("response is not in list formet")

    for index,record in enumerate(data):
        missing_fields = REQUIRED_FIELDS-record.keys()
        if missing_fields:
            raise ValueError(
                f"Missing fields {missing_fields} in index {index}"
            )

def get_designation(experience):
    if experience< 3:
        return"System Engineer"
    elif 3 <=experience<= 5:
        return "Data Engineer"
    elif 6 <=experience<= 10:
        return "Senior Data Engineer"
    else:
        return"Lead"


def normalize_phone(phone):
    phone_str = str(phone).lower()
    if "x" in phone_str:
        return "Invalid Number"
    digits = re.sub(r"\D", "", phone_str)
    return int(digits)


def normalize_data(data):
    df = pd.DataFrame(data)
    df["Full Name"] =df["first_name"] + " " + df["last_name"]
    df["designation"] =df["years_of_experience"].apply(get_designation)
    df["phone"] =df["phone"].apply(normalize_phone)
    df["hire_date"] = "" #not specified therefore krpt empty

    df = df.astype({
        "Full Name": "string",
        "email": "string",
        "gender": "string",
        "age": "int",
        "job_title": "string",
        "years_of_experience": "int",
        "salary": "int",
        "department": "string"
    })

    return df

def main():
    
    logging.info("Starting employee data pipeline")

    data = fetch_employee_data()
    logging.info("Employee data fetched successfully")

    validate_structure(data)
    logging.info("Data validation successful")

    df =normalize_data(data)
    logging.info("Data normalization completed")

    output_path=os.path.join(os.getcwd(),"employees_cleaned.csv")
    df.to_csv(output_path,index=False)
    print(f"File location:{output_path}")


if __name__ =="__main__":
    main()
