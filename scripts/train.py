# scripts/train.py 最终修正代码

import os
from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 确定当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    
    # 2. 确定项目根目录 (D:\XJTU\robocup)
    # 假设文件结构是: D:\XJTU\robocup\yolo_task\scripts\train.py
    # 需要往上退三层目录：
    # \scripts -> \yolo_task -> \robocup (项目根目录)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    
    # 3. 构造 data.yaml 的绝对路径
    DATASET_CONFIG_PATH = os.path.join(BASE_DIR, 'yolo_task','datasets', 'my_products', 'data.yaml')
    
    # 4. 检查文件是否存在
    # 如果文件不存在，立即停止并显示用户可读的错误信息
    if not os.path.exists(DATASET_CONFIG_PATH):
        print("❌ 致命错误：数据集配置文件未找到！")
        print(f"请检查文件是否存在于: {DATASET_CONFIG_PATH}")
        # 这里使用 exit() 而不是抛出 FileNotFoundError，以便输出更清晰
        exit(1)

    print(f"✅ 配置文件路径确认: {DATASET_CONFIG_PATH}")

    # 5. (可选) 确保YOLOv8s.pt存在于项目根目录
    # 由于您之前成功下载了yolov8s.pt，我们使用绝对路径引用它
    MODEL_PATH = os.path.join(BASE_DIR, 'yolov8s.pt')
    
    # 6. 加载模型
    model = YOLO(MODEL_PATH)
    
    # 7. 开始训练，使用绝对路径
    print("🚀 启动模型训练...")
    results = model.train(
        data=DATASET_CONFIG_PATH,  # <-- 使用绝对路径
        epochs=300, 
        imgsz=640,
        batch=16,
        name='product_detection_run_final',
        patience=50
    )