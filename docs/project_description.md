**Task description:**

Необходимо разработать веб-приложение простой платежной системы (для
упрощения, все переводы и зачисления без комиссии). Требования:
1) Каждый клиент в системе имеет один "кошелек", содержащий денежные
средства.
2) Сохраняется информация о кошельке и остатке средств на нем.
3) Клиенты могут делать друг другу денежные переводы.
4) Сохраняется информация о всех операциях на кошельке клиента.
5) Проект представляет из себя HTTP API, содержащее основные операции по
"кошелькам":
1) создание клиента с кошельком;
2) зачисление денежных средств на кошелек клиента;
3) перевод денежных средств с одного кошелька на другой.
6) ​Весь проект, со всеми зависимостями должен разворачиваться командой
docker-compose up.
   
----
**Реализованы сервисы:**
* wallet_service. Доступен по [http://localhost:8000//api/v1/wallet](http://localhost:8000//api/v1/wallet)
* transaction_service. Доступен по [http://localhost:8000//api/v1/transaction](http://localhost:8000//api/v1/transaction)

Сервисы принимают POST-запросы на создание, GET-запросы на получение информации из кеша/БД.
При первоначальном запросе на создание, в ответе будет содержаться уникальный **handshake_id**,
который будет в дальнейшем испльзоваться для получения данных.
Запрос на создание и само создание разделено. Транспортом является amqp.

Пример запроса создания кошелька
```shell script
curl -d '{"user_id":1, "amount": 7100}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/wallet/
```
output
```shell script
{"user_id":null,"handshake_id":"e49792b55c82a2971c9c69a3144c604cec32bf6dd2a80c08660cb7b001e7363e","wallet_id":null,"status":null,"amount":null,"created_at":null,"updated_at":null,"currency":null}
```
Как видно, кроме **handshake_id** в теле ответа ничего нет. 

Добавим **handshake_id** в payload и запросим информацию по кошельку
```shell script
curl -d '{"user_id":1, "handshake_id":"e49792b55c82a2971c9c69a3144c604cec32bf6dd2a80c08660cb7b001e7363e"}' -H "Content-Type: application/json" -X GET http://127.0.0.1:8000/api/v1/wallet/
```
output
```shell script
{"user_id":null,"handshake_id":"e49792b55c82a2971c9c69a3144c604cec32bf6dd2a80c08660cb7b001e7363e","wallet_id":3,"status":"active","amount":7100.0,"created_at":"2021-05-04T22:14:24.943205","updated_at":"2021-05-04T22:14:24.943228","currency":"usd"}
```

Транзакция создается похожим образом. Отличие в том, что необходимо иметь 2 активных кошелька и необходимую сумму на source_wallet
```shell script
curl -d '{"user_id": 1, "source_wallet_id": 1, "dest_wallet_id": 2, "trans_sum": 777.88}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/transaction/
```
output
```shell
{"user_id":null,"handshake_id":"8e43f69a267479d340bbddda0ffa26b1d7f3fc51acae0e859067f98977e88f5e","transaction_id":null,"status":null,"source_wallet_id":null,"destination_wallet_id":null,"info":null}
```
Повторный запрос на получение данных по транзакции
```shell script
curl -d '{"user_id":1, "handshake_id":"8e43f69a267479d340bbddda0ffa26b1d7f3fc51acae0e859067f98977e88f5e"}' -H "Content-Type: application/json" -X GET http://127.0.0.1:8000/api/v1/transaction/
```

output
```shell
{"user_id":null,"handshake_id":"8e43f69a267479d340bbddda0ffa26b1d7f3fc51acae0e859067f98977e88f5e","transaction_id":2,"status":"processed","source_wallet_id":1,"destination_wallet_id":2,"info":{"msg":"transaction was successful"}}
```

Теперь можно запросить детальную инфу по каждому из кошельков.

-----
Также для GET-запросов есть асинхронная реализация (наверн стоит использовать в debug-режиме) - /wallet/async и /transaction/async
Реализована как асинхронный запрос к DB, минуя очереди.

-----
!WARN! Т.к. при каждом запросе сервер возвращает обновленный handshake_id, то для исключения получения "протухших" данных
стоит ВСЕГДА использовать новый handshake_id

Enjoy!