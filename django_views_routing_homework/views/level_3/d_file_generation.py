"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""
from faker import Faker
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotAllowed


def create_text_content(length: int):
    text = Faker().text(max_nb_chars=length)
    return text


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    length = int(request.GET.get('length', 0))
    if length < 5 or length > 256:
        return HttpResponseForbidden()
    content = create_text_content(length)

    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="content_length_{length}.txt"'

    return response
