# OSINT Analyzer

Веб-приложение для анализа открытой разведывательной информации (OSINT).

## Быстрый старт

### Требования
- Установленный Docker
- Порт 5000 должен быть свободен

### Установка и запуск

**Windows:**
```cmd
start.bat
```
При ошибках используйте `debug.bat`

**Linux/Mac:**
```bash
chmod +x debug_build.sh
./debug_build.sh
```

### Ручная установка через Docker
```bash
# Сборка образа
docker build -t osint-analyzer .

# Запуск контейнера
docker run -d -p 5000:5000 --name osint-app osint-analyzer

# Проверка статуса
docker ps

# Просмотр логов
docker logs osint-app
```

### Доступ к приложению
После запуска приложение доступно по адресу: `http://localhost:5000`

## Структура проекта
```
osint-analyzer/
├── app.py              # Основное приложение Flask
├── requirements.txt    # Зависимости Python
├── Dockerfile         # Конфигурация Docker
├── start.bat          # Скрипт запуска для Windows
├── debug.bat          # Скрипт отладки для Windows
├── debug_build.sh     # Скрипт сборки для Linux/Mac
├── templates/         # HTML шаблоны
└── static/           # CSS, JavaScript файлы
```

## Решение проблем

### Частые ошибки:

**Порт 5000 занят:**
```bash
# Используйте другой порт
docker run -d -p 5001:5000 --name osint-app osint-analyzer
```

**Docker не запущен:**
- Убедитесь, что Docker Desktop/Engine работает
- Проверьте: `docker version`

**Контейнер не запускается:**
```bash
# Проверьте логи
docker logs osint-app

# Перезапустите контейнер
docker restart osint-app
```

### Команды для отладки:
```bash
# Проверка статуса контейнеров
docker ps -a

# Детальные логи
docker logs osint-app

# Остановка и удаление контейнера
docker stop osint-app
docker rm osint-app

# Удаление образа
docker rmi osint-analyzer
```

## Конфигурация

Приложение запускается с настройками:
- **Порт**: 5000
- **Хост**: 0.0.0.0 (доступно со всех интерфейсов)
- **Режим отладки**: включен

## Разработка

Для локальной разработки без Docker:
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python app.py
```

## Примечание

Приложение предназначено для легитимного сбора и анализа открытой информации. Используйте в соответствии с законодательством и правилами платформ.
