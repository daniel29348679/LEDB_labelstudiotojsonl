# %%
import json
import numpy as np


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

        corners = []

        for x, y in label["points"]:
            corners.append(
                f"[{x * 0.01 * original_width}, {y * 0.01 * original_height}],"
            )
        matrix.append(corners)

    ofs.write(f'"paragraphs":[')
    for text, corners in zip(texts, matrix):
        ofs.write("{")
        ofs.write('"vertices": [')
        for corner in corners:
            ofs.write(corner)
        ofs.write("],")
        ofs.write(f'"legible": true,')

        ofs.write(f'"lines":[')
        ofs.write("{")
        ofs.write('"vertices": [')
        for corner in corners:
            ofs.write(corner)
        ofs.write("],")
        ofs.write(f'"text": "{text}",')
        ofs.write(f'"legible": true,')
        ofs.write(f'"handwritten": false,')
        ofs.write(f'"vertical": false,')

        ofs.write(f'"words":[')
        ofs.write("{")
        ofs.write('"vertices": [')
        for corner in corners:
            ofs.write(corner)
        ofs.write("],")
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
