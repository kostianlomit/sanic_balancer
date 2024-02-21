import pytest
from sanic import Sanic, response, json

from api.config import CDN_HOST


@pytest.fixture
def app():
    sanic_app = Sanic("TestSanic")
    return sanic_app

# проверка прямого запроса к origin server
def test_get_server(app):
    request, response = app.test_client.get(f"/origin/<pk:{int}>")

    assert request.method.lower() == "get"
    assert response.body == f"http://balancer-domain/?video=http://s{int}.origin-cluster/video/1488/xcg2djHckad.m3u8"
    assert response.status == 301

# проверка редиректа сервера CDN
def test_get_CDN(app):
    request, response = app.test_client.get(f'/CDN_HOST/<pk:{int}>')

    data = response.json()
    assert f"server_s{int}" in data
    assert request.method.lower() == "get"
    assert response.body == f'http://{CDN_HOST}/s{int}/video/1488/xcg2djHckad.m3u8'
    assert data[f"server_s{int}"] == f'http://{CDN_HOST}/s{int}/video/1488/xcg2djHckad.m3u8'
    assert response.status == 301

# проверка кеша при переходе на origin сервер