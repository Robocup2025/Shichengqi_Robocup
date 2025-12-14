import cv2
import os
import sys

def convert(avi_path, mp4_path):
    cap = cv2.VideoCapture(avi_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {avi_path}")
        return 1

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(mp4_path, fourcc, fps, (width, height))
    if not out.isOpened():
        print(f"无法创建输出文件: {mp4_path}")
        cap.release()
        return 1

    print(f"开始转换: {avi_path} -> {mp4_path}，fps={fps}, size=({width},{height})")
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        count += 1

    cap.release()
    out.release()
    print(f"转换完成，写入帧数: {count}")
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python convert_avi_to_mp4.py <input.avi> <output.mp4>")
        sys.exit(1)
    avi = sys.argv[1]
    mp4 = sys.argv[2]
    sys.exit(convert(avi, mp4))
