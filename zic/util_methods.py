from typing import List, Dict

from requests import Session

from zic.util_types import ArrivalSplashData, ZICInsuranceStages


def get_mapping_by_row_id(options: List[Dict], key: str):
    return {row[key].lower(): row['row_id'] for row in options}


def handle_arrivals_splash(session: Session):
    response = session.get(ZICInsuranceStages.ArrivalsSplash.value)
    print(response.json())
    data = response.json()['response']['data']
    return ArrivalSplashData(
        insurance_types=data["insurance_type"]["en"],
        nationalities=get_mapping_by_row_id(data['nationality'], 'nationality'),
        countries=get_mapping_by_row_id(data['countries'], 'country'),
        relationship_types=get_mapping_by_row_id(data['relationship_types'], 'relationship_type'),
        travel_purpose=get_mapping_by_row_id(data['travel_purpose']['en'], 'name'),
        genders=get_mapping_by_row_id(data['gender']['en'], 'gender'),
    )


def get_insurance_type(beneficiaries_num: int, insurance_types: List[Dict]):
    for option in insurance_types:
        if int(option['min_people']) <= beneficiaries_num <= int(option['max_people']):
            return option['insurance_type']
