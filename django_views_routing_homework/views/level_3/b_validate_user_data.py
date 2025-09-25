"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
import json
import re
from typing import TypedDict, NotRequired

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse


class UserData(TypedDict):
    full_name: str
    email: str
    registered_from: str
    age: NotRequired[int]


def validate_user_data(user_data_json: UserData) -> bool:
    email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    required_keys = {"full_name", "email", "registered_from"}
    allowed_keys = {"full_name", "email", "registered_from", "age"}
    income_user_data_keys = set(user_data_json.keys())

    if income_user_data_keys - allowed_keys or not required_keys.issubset(income_user_data_keys):
        return False

    is_correct_full_name = 5 < len(user_data_json['full_name']) < 256
    is_correct_email =  bool(re.match(email_pattern, user_data_json['email']))
    is_correct_registered_from = user_data_json['registered_from'] in ['website', 'mobile_app']
    is_correct_age =  isinstance(user_data_json['age'], int) if 'age' in user_data_json.keys() else True

    return is_correct_full_name and is_correct_email and is_correct_registered_from and is_correct_age


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        user_data_json = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid json")
    else:
        is_valid = validate_user_data(user_data_json)
        return JsonResponse(data={'is_valid': is_valid}, status=200)
