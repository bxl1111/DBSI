import json
import os


def convert_txt_to_json(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf - 8') as f:
        lines = f.readlines()
        if not lines:
            print(f'{txt_file_path} 为空文件，跳过该文件')
            return
        json_data = {}
        # 读取倾斜点
        try:
            json_data['slant_point'] = float(lines[0].strip())
        except ValueError:
            raise ValueError('倾斜点的格式不正确，应该为可转换为浮点数的格式')
        # 读取垂直位置
        try:
            vertical_pos = int(''.join(c for c in lines[1].strip() if c.isdigit()))
            json_data['vertical_position'] = vertical_pos
        except ValueError:
            raise ValueError('垂直位置的格式不正确，应该为可转换为整数的格式')
        # 读取水平位置
        try:
            horizontal_pos = int(''.join(c for c in lines[2].strip() if c.isdigit()))
            json_data['horizontal_position'] = horizontal_pos
        except ValueError:
            raise ValueError('水平位置的格式不正确，应该为可转换为整数的格式')

        if len(lines) < 4:
            raise ValueError('数据不完整，缺少盲文单元格注释部分')

        cells = []
        for i in range(3, len(lines)):
            line = lines[i].strip()
            parts = line.split()
            if len(parts)!= 8:
                raise ValueError(f'第{i + 1}行盲文单元格注释必须有8个数字')
            try:
                cell = {
                    "row": int(parts[0]),
                    "col": int(parts[1]),
                    "dots": list(map(int, parts[2:]))
                }
                cells.append(cell)
            except ValueError:
                raise ValueError(f'第{i + 1}行盲文单元格注释中的数字格式错误')
        json_data["cells"] = cells

    json_file_path = os.path.splitext(txt_file_path)[0] + '.json'
    with open(json_file_path, 'w') as f:
        json.dump(json_data, f, indent=4)


def convert_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                convert_txt_to_json(os.path.join(root, file))


if __name__ == '__main__':
    folder_path = '/home/zkhc/Desktop/UNet/datasets/labels'
    convert_folder(folder_path)

