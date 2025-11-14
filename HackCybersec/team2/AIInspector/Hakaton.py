from model import predict_image

model_path = "model.pth"
image_path = "test.jpg"

print(predict_image(model_path, image_path))