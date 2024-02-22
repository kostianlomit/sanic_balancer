from sanic import Sanic, json, redirect
from sanic.response import text
from sanic_redis import SanicRedis
from sqlalchemy import select

from api.balanser.balanser import request_is_limited
from api.balanser.models import OriginServer
from api.config import CDN_HOST


# Для теста балансировки
fake_uzer_db = {
    1 : {"server_s1": "http://balancer-domain/?video=http://s1.origin-cluster/video/1488/xcg2djHckad.m3u8"},
    2 : {"server_s2": "http://balancer-domain/?video=http://s2.origin-cluster/video/1488/xcg2djHckad.m3u8"},
    3 : {"server_s3": "http://balancer-domain/?video=http://s3.origin-cluster/video/1488/xcg2djHckad.m3u8",
    }
}

app = Sanic("sanic_balancer")

# подключаем кэш для CDN_HOST
redis_client = SanicRedis() # default config_name is "REDIS"
redis_client.init_app(app)


app.config.update(
    {
        'REDIS': "redis://localhost:6379/0",
    }
)

# редирект
@app.route('/CDN_HOST')
async def handler(request):
    return text(f'http://{CDN_HOST}/s{int}/video/1488/xcg2djHckad.m3u8')


# принимает запрос http://balancer-domain/?video=http://s1.origin-cluster/video/1488/xcg2djHcka
# d.m3u8' ведущий на s1 или другие сервера
@app.get(f"/origin/<pk:{int}>")
async def get_server(request):
    session = request.ctx.session
    async with session.begin():
        async with redis_client.conn as r:
            """
            Кэшируем 1й запрос и подключаем redirect на СDN_сервер
            как N истекает и снова идем на origin сервер
            """
            # 1го запроса нету в кеше
            cache_value = r.get(f'{int}')
            if cache_value is not None:
                if request_is_limited(r, f'{int}', 10):
                    return redirect(f'/CDN_HOST/<pk:{int}>')

            # делаем запрос нужного origin_server
            stmt = select(OriginServer).where(OriginServer.id == int)
            res = await session.execute(stmt)
            server = res.scalar()

            # отправляем url сервера в json формате
            result = json(server.to_dict(int))

            # добавляем url_s1 и дальше работаем в кеше до N запросов
            await r.set(f'{int}', str(result))
            return result



if __name__ == '__main__':
    app.run(debug=False)

