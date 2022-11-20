from pydantic import BaseModel, ValidationError
from requests import Response

from src.enums.global_enums import GlobalEnums


class ResponseTest:
    """
    Тестирование Response на:
    * статус код
    * соответствие заданной модели
    * значение возвращаемого поля
    """

    def __init__(self, response: Response):
        self.response: Response = response
        self.response_status: int = response.status_code
        try:
            self.response_data: list | dict = response.json()['data']
        except KeyError:
            self.response_data: list | dict = response.json()

    def assert_status_code(self, status_code: list | int):
        if isinstance(status_code, list):
            assert self.response_status in status_code, self
        else:
            assert self.response_status == status_code, self

        return self

    def validate(self, model: BaseModel):
        if isinstance(self.response_data, list):
            for item in self.response_data:
                try:
                    model.parse_obj(item)
                except ValidationError:
                    print(item)
                    raise
        else:
            try:
                model.parse_obj(self.response_data)
            except ValidationError:
                print(self.response_data)
                raise

    def validate_field(self, field, value):
        if isinstance(self.response_data, list):
            for item in self.response_data:
                assert item[field] == value, f'{GlobalEnums.WRONG_FIELD}\n{self}'
        else:
            assert self.response_data[field] == value, f'{GlobalEnums.WRONG_FIELD}\n{self}'

    def __str__(self):
        return f'\nResponse status code: {self.response_status}\n' \
               f'Response date: {self.response_data}'
