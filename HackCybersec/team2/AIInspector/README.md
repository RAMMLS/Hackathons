Запуск с вашим model.pth:

docker build -t ai-artifact-detector .
docker run -v $(pwd)/data:/app/data -v $(pwd)/model.pth:/app/model.pth ai-artifact-detector


Если хотите протестировать на конкретном изображении:
bash

docker run -v $(pwd)/data:/app/data -v $(pwd)/model.pth:/app/model.pth -v $(pwd)/test_image.jpg:/app/test.jpg ai-artifact-detector

Или для использования test.py:
bash

docker run -v $(pwd)/data:/app/data -v $(pwd)/model.pth:/app/model.pth -v $(pwd)/test_image.jpg:/app/трал.jpg ai-artifact-detector python test.py
