from hitnet import HitNet, ModelType

model_type = ModelType.eth3d
model_path = "models/eth3d/saved_model_120x160/model_float32.tflite"

hitnet_depth = HitNet(model_path, model_type)

print(hitnet_depth)
