from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

error_html = 'error.html'


def csrf_failure(request: HttpRequest, reason='') -> HttpResponse:
    return render(request, error_html, status=HTTPStatus.FORBIDDEN)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, error_html, status=HTTPStatus.NOT_FOUND)


def server_error(request: HttpRequest) -> HttpResponse:
    return render(request, error_html, status=HTTPStatus.INTERNAL_SERVER_ERROR)
