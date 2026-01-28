from datetime import datetime

from processing.tazania.util_types import TanzaniaPayloadData, EmploymentStatus


def get_employment_type(data: TanzaniaPayloadData):
    age = (datetime.now() - data.passport.date_of_birth).days / 365
    if age < 3:
        return "Infant"
    elif age < 18:
        return "Minor "
    elif data.employment.employment_status == EmploymentStatus.Other.value:
        return "Unemployed" if age < 60 else "Retired "
    elif data.employment.employment_status == EmploymentStatus.Soldier.value:
        return "Employed"
    else:
        return EmploymentStatus[data.employment.employment_status].name


def get_employment_data(data: TanzaniaPayloadData):
    employment = {}
    if data.employment.employment_status == EmploymentStatus.Soldier.value:
        employment["Employer"] = "IDF"
        employment["Occupation"] = "Soldier"
    elif data.employment.employer_name:
        employment["Employer"] = data.employment.employer_name
        employment["Occupation"] = data.employment.occupation

    return employment
