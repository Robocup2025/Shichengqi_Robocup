# scripts/predict_camera.py

from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 加载训练好的模型权重
    # 请确保路径指向您训练完成后生成的 best.pt 文件
    model_path = 'runs/detect/product_detection_run_final10/weights/best.pt'
    try:
        model = YOLO(model_path)
    except FileNotFoundError:
        print(f"错误：未找到模型文件 {model_path}。请先运行 train.py 并确保路径正确。")
        exit()

    print(f"成功加载模型：{model_path}")
    print("开始实时摄像头检测，按 'q' 键退出...")

    # 2. 使用模型进行推理
    # source=0: 使用默认摄像头
    # show=True: 实时显示结果
    # conf=0.5: 只有置信度高于 0.5 的目标才显示 (可根据效果调整)
    results = model.predict(
        source=0, 
        show=True, 
        conf=0.5, 
        save=False, 
        # project='runs/predict', # 推理结果保存目录，此处我们实时显示
        # name='camera_test',
    )
    
    # model.predict() 会自动在画面上画框、显示类别名称和置信度。