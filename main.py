# %%
import json
import numpy as np


def get_rotated_bounding_box_corners(original_width, original_height, value):
    # 轉換邊界框的 x, y, width, height 百分比為 px 值
    box_x = (value["x"] / 100) * original_width
    box_y = (value["y"] / 100) * original_height
    box_width = (value["width"] / 100) * original_width
    box_height = (value["height"] / 100) * original_height

    # 計算未旋轉時的邊界框頂點
    corners = np.array(
        [
            [box_x, box_y],  # 左上角
            [box_x + box_width, box_y],  # 右上角
            [box_x + box_width, box_y + box_height],  # 右下角
            [box_x, box_y + box_height],  # 左下角
        ]
    )

    # 計算邊界框的中心
    center_x = box_x + box_width / 2
    center_y = box_y + box_height / 2

    # 邊界框的旋轉矩陣 (針對 value.rotation)
    theta_box = np.radians(value["rotation"])  # 邊界框旋轉角度轉換為弧度
    rotation_matrix_box = np.array(
        [
            [np.cos(theta_box), -np.sin(theta_box)],
            [np.sin(theta_box), np.cos(theta_box)],
        ]
    )

    # 以中心為基準旋轉邊界框的四個角
    rotated_corners = np.dot(corners - [center_x, center_y], rotation_matrix_box) + [
        center_x,
        center_y,
    ]

    return rotated_corners


with open("input.json", "r") as file:
    origin_data = json.load(file)

ofs = open("output.jsonl", "w")

for image in origin_data:
    print(image)
    print(image.keys())
    texts = image["text"]
    ofs.write("{")
    name = image["image"]
    name_start = 0
    for i in range(len(name)):
        if name[i] == "/":
            name_start = i + 1
    name = name[name_start:]
    ofs.write(f'"image_id": "{name}",')

    labels = image["label"]

    matrix = []
    for label in labels:
        print(label)
        # 示例資料
        original_width = label["original_width"]
        original_height = label["original_height"]
        value = {
            "x": label["x"],  # 百分比
            "y": label["y"],  # 百分比
            "width": label["width"],  # 百分比
            "height": label["height"],  # 百分比
            "rotation": label["rotation"],  # 邊界框旋轉 45 度
        }

        corners = get_rotated_bounding_box_corners(
            original_width, original_height, value
        )
        matrix.append(corners)

    ofs.write(f'"paragraphs":[')
    for text, corners in zip(texts, matrix):
        corners = f"[[{corners[0][0]},{corners[0][1]}],[{corners[1][0]},{corners[1][1]}],[{corners[2][0]},{corners[2][1]}],[{corners[3][0]},{corners[3][1]}]]"
        ofs.write("{")
        ofs.write(f'"vertices": {corners},')
        ofs.write(f'"legible": true,')

        ofs.write(f'"lines":[')
        ofs.write("{")
        ofs.write(f'"vertices": {corners},')
        ofs.write(f'"text": "{text}",')
        ofs.write(f'"legible": true,')
        ofs.write(f'"handwritten": false,')
        ofs.write(f'"vertical": false,')

        ofs.write(f'"words":[')
        ofs.write("{")
        ofs.write(f'"vertices": {corners},')
        ofs.write(f'"text": "{text}",')
        ofs.write(f'"legible": true,')
        ofs.write(f'"handwritten": false,')
        ofs.write(f'"vertical": false,')

        ofs.write("},")
        ofs.write("],")
        ofs.write("},")
        ofs.write("],")
        ofs.write("},")

    ofs.write(f"]")

    ofs.write("}\n")


ofs.close()
# %%
