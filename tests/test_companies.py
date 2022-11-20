import requests

from configaration import SERVICE_URL

from src.baseclasses.response import ResponseTest
from src.pydantic_models.company import Company
from src.enums.company import CompanySatus
from src.enums.global_enums import GlobalEnums


def test_get_list_of_companies():
    response = requests.get(SERVICE_URL + 'companies/')
    test_response = ResponseTest(response)
    test_response.assert_status_code([200]).validate(Company)


def test_get_company():
    response = requests.get(SERVICE_URL + 'companies/1')
    test_response = ResponseTest(response)
    test_response.assert_status_code([200]).validate(Company)


def test_get_filtering_list_of_companies_status():
    for status in CompanySatus:
        response = requests.get(SERVICE_URL + f'companies/?status={status.value}')
        test_response = ResponseTest(response)
        test_response.assert_status_code([200]).validate_field('company_status', status.value)


def test_get_filtering_list_of_companies_limit_offset():
    response = requests.get(SERVICE_URL + f'companies/?limit=3&offset=0')
    test_response = ResponseTest(response)
    test_response.assert_status_code([200])
    assert len(test_response.response_data) == 3, GlobalEnums.WRONG_LEN_OF_LIST.value

    for i in range(1, 5):
        response = requests.get(SERVICE_URL + f'companies/?limit={i}&offset={5 - i}')
        test_response = ResponseTest(response)
        test_response.assert_status_code([200])
        assert len(test_response.response_data) <= i, GlobalEnums.WRONG_LEN_OF_LIST.value
