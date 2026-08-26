# R4C Interview Task
![MIT License](https://img.shields.io/github/license/JustKappaMan/R4C-Interview-Task)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Тестовое задание на должность Python/Django разработчик в [BST Digital](https://bst.digital).

## О проекте
Проект разработан на языке программирования Python с минимальным количеством зависимостей.

С поставленными задачами и вводными данными от работодателя можно ознакомиться в файлах [employer-readme.md](employer-readme.md) и [employer-tasks.md](employer-tasks.md).

Электронные письма отправляются в терминал в демонстрационных целях.

## Инструкции по запуску
```bash
git clone https://github.com/JustKappaMan/R4C-Interview-Task.git
cd R4C-Interview-Task
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd src
python3.10 manage.py migrate
python3.10 manage.py runserver --noreload
```

## Благодарности
* [Фавиконка](https://www.flaticon.com/free-icon/chip_9980230) — [rukanicon](https://www.flaticon.com/authors/rukanicon)

## Информация о лицензии
Продукт распространяется под лицензией [MIT](LICENSE).
