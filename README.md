# Сервис для мониторинга и анализа состояния парковочных мест в реальном времени

[![Update Ubuntu 22.04](https://github.com/GachiSlave/sofg_eng/actions/workflows/linter.yml/badge.svg)](https://github.com/GachiSlave/sofg_eng/actions/workflows/linter.yml/)

Суть проекта состоит на обнаружении, без использования масок, парковочных мест, на основе детектирования стоящих автомобилей при помощи предварительно обученной модели [YOLOv8](https://github.com/ultralytics/ultralytics). Результаты обнаружения освободившегося/занятого парковочного места оповещается при помощи Telegram-бота.


## Документация по запуску проекта

#### 1. Клонирование репозитория:
```
git clone https://github.com/GachiSlave/sofg_eng.git
cd sofg_eng
```

#### 2. Установка зависимостей и запуск виртуальной среды:
* на Linux:
```
chmod +x install.sh
./install.sh
source venv/bin/activate
```

  * на Windows (cmd)
```
install.bat
```

#### 3. Настройка конфигурации:
Откройте файл `config.yaml`:
* Замените `chat_id` на ваш Telegram chat ID, если Вы используете свой бот, то так же замените `TOKEN`. Узнать `chat_id` интересующего чата, а так же воспользоваться готовым ботом можно при помощи [Parking space Notifier](https://t.me/freeparkingcar_bot) (при использовании `Parking space Notifier` бота `TOKEN` менять не нужно).
* В `path` вставьте путь до видео или `"0"` для камеры (video stream).

#### 4. Запуск проекта:
```
python main.py
```
#### 5. Запуск тестов:
Проверка модулей и качества данных.
```
pytest tests/
```
или
```
python -m unittest discover -s tests
```

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&duration=2000&pause=1000&color=1141f7&random=false&width=600&lines=You're+breathtaking!+%E2%9C%A8)](https://git.io/typing-svg)

-------
### Над проектом работали:

* Ахаимов Данила Игоревич РИМ-130907

* Луговых Владислав Витальевич РИМ-130908

* Чудинова Алена Сергеевна РИМ-130907

* Холоденко Мария Дмитриевна РИМ-130907

-------
### Финальный проект MLOps
Были выполнены все требования к реализации проекта: 
1.	Исходные коды проекта располагаются в репозитории [GitHub](https://github.com/GachiSlave/sofg_eng/).
2.	Проект оркестируется с помощью CI/CD Jenkins. 
3.	Датасеты версионируются с помощью dvc и синхронизируются с удалённым хранилищем. 
4.	Рефакторинг выполнен в отдельных ветках.
5.	В коневеере Jenkins запускаются модульные тесты и проверка тестами на качество данных.
6.	Итоговое приложение реализуется в виде Docker образа. Сборка образа происходит в конвеере Jenkins. 
7.	В проекте используется предварительно обученная модель [YOLOv8](https://github.com/ultralytics/ultralytics).

Так же выполняется проверка качества кода и запуск тестов через [GitHub Actions](https://github.com/GachiSlave/sofg_eng/actions/workflows/linter.yml).
