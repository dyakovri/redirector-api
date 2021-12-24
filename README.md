# Бэкэнд приложения для сокращения ссылок

Бэкэнд приложения, которое позволяет пользователям сокращать длинные ссылки в короткие.
Является очень упрощенным аналогом [bit.ly](https://bitly.com/) и многих других. Используется
совместно с [фронтэндом](https://github.com/dyakovri/redirector-ui).

## Использование

Демо можно найти по адресу https://to.dyakov.space/. Для создания ссылки нужно ввести токен
авторизации (задается через настройки сервиса в файле `.env`), короткое имя ссылки и саму ссылку,
которую нужно сократить.

## Установка

Для установки потребуются
- Docker
- Docker Compose (опционально, но инструкция для него)
- Caddy (или другой reverse proxy)

1. Создайте файл `.env` с паролем для базы данных и кодом авторизации пользователей
```
POSTGRES_PASSWORD=1234abcd...
SECRET=abcd1234...
```

2. Создайте файл `docker-compose.yml` с настройками запуска

```yaml
version: "3.6"

services:
  api:
    image: ghcr.io/dyakovri/redirector-api:master
    restart: always
    environment:
      DB_DSN: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/postgres
      SECRET: ${SECRET}
    networks:
      web:
        aliases:
          - to_api
      backend:
    depends_on:
      - postgres

  ui:
    image: ghcr.io/dyakovri/redirector-ui:master
    restart: always
    networks:
      web:
        aliases:
          - to_ui
    depends_on:
      - api

  postgres:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres:/var/lib/postgresql/data
    networks:
      backend:


networks:
  web:
    name: web
    external: true
  backend:

volumes:
  postgres:
    name: redirect-data
```

3. Запустите сервис

4. Настройте свой http сервер для обратного проксирования трафика. Для домена to.dyakov.space и
сервера [Caddy в докере](https://hub.docker.com/_/caddy), настрйка должна выглядеть следующим
образом:

*Caddy должен находиться в той же сети, что и контейнеры. В нашем примере у нас создана сеть web.*

```
to.dyakov.space:443 {
    route /ui/* {
        uri strip_prefix /ui
        reverse_proxy to_ui:80
    }
    reverse_proxy /* to_api:80
}
```

То есть для всех url на домене происходит переадресация на контейнер api, за исключением /ui,
который проксирует на контейнер ui с интерфейсом.
