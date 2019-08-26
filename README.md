### Общее

Постарался выполнить все пункты задания. Написал все 5 ручек. 

Особое внимание уделил написаню валидаторов запросов.

Используемая версия языка python: 3.7.4

#### Сервер

Выбрал асинхронный aiohttp [https://aiohttp.readthedocs.io]. Позволяет без особых проблем поднимать производительные приложения, способные обрабатывать несколько запросов одновременно.

#### База данных

В качестве базы данных выбрал postgreSQL, в частности так как она поддерживает массивы (для relatives). Это позволило без особых заморочек реализовать необходимую логику.

Скрипт на таблицу и на enum для неё в: init.sql (можно сделать через миграции)

Формально в задании можно было бы использовать нереляционная базу данных, такую как например mongoDB, так как реляционность особо не нужна, по крайней мере в такуй реализации, как написал я.
Поэтому использовать монгу было бы может даже более оправданно. Но надо мерить производительность.

### Деплой

1. При делое особых проблем не возникло. Поставил на сервер базу postgres, создал базу.

2. Настроил supervisord [http://supervisord.org/]. Включил автоподнятие при рестарте сервера и логгирование в файл.

3. Поставил virtualenv [https://virtualenv.pypa.io/], чтобы не засорять систему. 

4. Установил зависимости:

```
pip3 install -r requirements.txt
```

5. Запустил приложение:

```
sudo service supervisor start
```

### Что можно ещё сделать:

1. Повысить покрытие тестами. 

Сейчас есть интеграционный тест, покрывающий все ручки. В папке tests/integrations скрипт full_integration_start,py запускает прогон интеграционных тестов на все 5 ручек и частично анализирует правильность ответа. Надо сделать ещё unit-тесты на все ручки, с моками и ассертами ключевых функций.

2. Читать данные конфигурации из конфигурационного файла. 

Сделать изменение уровня логгирования, текущий уровень - info, в логах будет спам. Ещё хорошо бы сделать возможность управлять потоком вывода лога в stdout и в файл.

3. Написать нагрузочные тесты и провести нагрузочное тестирование приложения. 

Можно для стресс теста взять wkr. Но в идеале промерить яндекс танком [https://yandex.ru/dev/tank/] - шикарная штука, сам часто пользуюсь.

Само задание понравилось) Было интересно)