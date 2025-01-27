```bash
git clone https://github.com/l1mero/bot \
echo "BOT_TOKEN=сюда токен свой поставь да" > bot/.env \
docker build -t gg -f bot/Dockerfile bot \
docker run gg
```
# Все да

### TODO:

- база данных
- redis cache
- хз потом придумаю
- мб middleware
- надо сервисы по умному интегрировать
- docker compose
