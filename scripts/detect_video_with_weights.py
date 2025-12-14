from ultralytics import YOLO
import os

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_root = os.path.dirname(base_dir)
    # 支持两种可能的位置：项目内 yolo_task/runs/... 或 workspace 根 runs/...
    candidate1 = os.path.join(base_dir, 'runs', 'detect', 'product_detection_run_final10', 'weights', 'best.pt')
    candidate2 = os.path.join(workspace_root, 'runs', 'detect', 'product_detection_run_final10', 'weights', 'best.pt')
    if os.path.exists(candidate1):
        weights = candidate1
    else:
        weights = candidate2
    video = os.path.join(base_dir, 'datasets', 'my_products', 'video', 'raw4.mp4')

    if not os.path.exists(weights):
        print(f"错误：未找到权重文件 {weights}")
        raise SystemExit(1)
    if not os.path.exists(video):
        print(f"错误：未找到视频文件 {video}")
        raise SystemExit(1)

    print(f"加载模型：{weights}")
    model = YOLO(weights)

    # 保存到 runs/detect/product_detection_run_final10_raw1
    project = os.path.join(base_dir, 'runs', 'detect')
    name = 'product_detection_run_final4_raw1'

    print(f"开始对视频进行检测：{video}")
    results = model.predict(
        source=video,
        conf=0.25,
        save=True,
        save_txt=True,
        project=project,
        name=name,
        show=False,
    )

    out_dir = os.path.join(project, name)
    print(f"检测完成，结果保存在：{out_dir}")
