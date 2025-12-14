import os
import random
import shutil

# --- 配置参数 ---
# 获取当前脚本的运行目录作为项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 定位到 yolo_task 根目录

# 根图片目录（包含若干待划分的子文件夹，例如 raw1/raw2/...）
IMAGES_ROOT = os.path.join(BASE_DIR, 'datasets', 'my_products', 'images')
# 原始标注可能位于 labels/raw、labels/<folder> 或 labels 根目录下
LABELS_ROOT = os.path.join(BASE_DIR, 'datasets', 'my_products', 'labels')

# 划分后图片存放的目录 (train/val)
TARGET_IMAGES_DIR = IMAGES_ROOT
# 划分后标注存放的目录 (train/val)
TARGET_LABELS_DIR = LABELS_ROOT

# 划分比例：80% 训练集，20% 验证集
TRAIN_RATIO = 0.8
VAL_RATIO = 1.0 - TRAIN_RATIO  

# --- 核心函数 ---

def create_dirs():
    """创建目标 train 和 val 文件夹。"""
    for folder in ['train', 'val']:
        os.makedirs(os.path.join(TARGET_IMAGES_DIR, folder), exist_ok=True)
        os.makedirs(os.path.join(TARGET_LABELS_DIR, folder), exist_ok=True)
    print("目标文件夹创建完毕。")

def split_data():
    """对 IMAGES_ROOT 下的每个子文件夹（排除 train/val）分别进行划分。

    为避免不同来源文件名冲突，复制到 train/val 时会在文件名前加上来源前缀：<src>_原文件名.jpg
    同名的标注文件也会按相同规则复制（如果能找到）。
    """
    if not os.path.exists(IMAGES_ROOT):
        print(f"错误：未找到图片根目录 '{IMAGES_ROOT}'。请检查。")
        return

    # 找到要处理的子文件夹（排除 train, val）
    subfolders = [d for d in os.listdir(IMAGES_ROOT)
                  if os.path.isdir(os.path.join(IMAGES_ROOT, d)) and d.lower() not in ('train', 'val')]

    if not subfolders:
        print(f"未找到待处理的子文件夹（在 {IMAGES_ROOT} 下）。")
        return

    def find_label_path(base_name):
        """尝试在可能的 labels 目录中查找标签文件，返回找到的路径或 None。"""
        candidates = [os.path.join(LABELS_ROOT, f) for f in (
            # 优先查找 labels/<subfolder>/<base>.txt
            # 在调用处会传入合适的目录前缀
            )]
        return None

    for src in subfolders:
        RAW_IMAGES_DIR = os.path.join(IMAGES_ROOT, src)

        all_images = os.listdir(RAW_IMAGES_DIR)
        image_files = [f for f in all_images if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        if not image_files:
            print(f"警告：'{RAW_IMAGES_DIR}' 中没有图片，跳过。")
            continue

        random.shuffle(image_files)
        total_count = len(image_files)
        train_count = int(total_count * TRAIN_RATIO)
        train_files = image_files[:train_count]
        val_files = image_files[train_count:]

        print(f"来源：{src}，总图片：{total_count}，训练：{len(train_files)}，验证：{len(val_files)}")

        images_train_dir = os.path.join(TARGET_IMAGES_DIR, 'train')
        images_val_dir = os.path.join(TARGET_IMAGES_DIR, 'val')
        labels_train_dir = os.path.join(TARGET_LABELS_DIR, 'train')
        labels_val_dir = os.path.join(TARGET_LABELS_DIR, 'val')

        def copy_with_prefix(file_list, target_images_dir, target_labels_dir):
            for image_name in file_list:
                src_image = os.path.join(RAW_IMAGES_DIR, image_name)
                prefix_name = f"{src}_" + image_name
                dst_image = os.path.join(target_images_dir, prefix_name)
                shutil.copy(src_image, dst_image)

                base_name, _ = os.path.splitext(image_name)
                label_name = base_name + '.txt'

                # 尝试在若干可能的标签目录中找到对应标注
                possible_label_paths = [
                    os.path.join(LABELS_ROOT, src, label_name),
                    os.path.join(LABELS_ROOT, 'raw', label_name),
                    os.path.join(LABELS_ROOT, label_name),
                ]
                found = False
                for lp in possible_label_paths:
                    if os.path.exists(lp):
                        dst_label = os.path.join(target_labels_dir, f"{src}_" + label_name)
                        shutil.copy(lp, dst_label)
                        found = True
                        break
                if not found:
                    # 没有找到标签也没关系，继续
                    pass

        print("  复制训练集...")
        copy_with_prefix(train_files, images_train_dir, labels_train_dir)
        print("  复制验证集...")
        copy_with_prefix(val_files, images_val_dir, labels_val_dir)

    print("\n✅ 数据集按来源子文件夹划分完成。")
    print(f"   训练集图片: {os.path.join(TARGET_IMAGES_DIR, 'train')}")
    print(f"   验证集图片: {os.path.join(TARGET_IMAGES_DIR, 'val')}")

if __name__ == '__main__':
    create_dirs()
    split_data()