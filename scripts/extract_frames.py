import cv2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
yolo_task_dir = os.path.dirname(script_dir)
video_dir = os.path.join(yolo_task_dir, "datasets", "my_products", "video")
images_root = os.path.join(yolo_task_dir, "datasets", "my_products", "images")
SKIP = 10

os.makedirs(images_root, exist_ok=True)

videos_to_process = [f"raw{i}.mp4" for i in range(1, 6)]
# common fallback in this dataset (exists in repo listing)
if "raw.mp4" not in videos_to_process:
    videos_to_process.append("raw.mp4")

total_saved = 0
for vid_name in videos_to_process:
    vid_path = os.path.join(video_dir, vid_name)
    if not os.path.exists(vid_path):
        print(f"⚠️ 视频未找到，跳过：{vid_name}")
        continue

    out_dir = os.path.join(images_root, os.path.splitext(vid_name)[0])
    os.makedirs(out_dir, exist_ok=True)

    print(f"▶ 开始处理：{vid_name} → {out_dir}")
    cap = cv2.VideoCapture(vid_path)
    if not cap.isOpened():
        print(f"✖ 无法打开视频：{vid_name}")
        continue

    frame_id = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % SKIP == 0:
            output_path = os.path.join(out_dir, f"frame_{saved:05d}.jpg")
            ret_enc, buffer = cv2.imencode('.jpg', frame)
            if ret_enc:
                with open(output_path, 'wb') as f:
                    f.write(buffer.tobytes())
                saved += 1
        frame_id += 1
    cap.release()
    total_saved += saved
    print(f"✅ 完成 {vid_name}：保存 {saved} 张图片")

print(f"🎉 所有处理结束，总共保存图片：{total_saved} 张")
