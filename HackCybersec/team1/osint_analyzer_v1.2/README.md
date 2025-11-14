#Update requirements.txt - обновил файл

#Update app.py 

'''python
*** для не читающих коммиты: в строчке app.run(debug=True) внес 
***правки: app.run(host='0.0.0.0', port=5000, debug=True)
'''


# Собираем образ
docker build -t osint-analyzer .

# Запускаем контейнер
docker run -d -p 5000:5000 --name osint-app osint-analyzer

# Проверяем логи
docker logs osint-app

# Проверяем статус
docker ps

# Тестируем приложение
curl http://localhost:5000


# Даем права на выполнение
chmod +x debug_build.sh

# Запускаем отладочную сборку
./debug_build.sh
