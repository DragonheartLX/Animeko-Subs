import os
import json
import hashlib

def merge_json(list_file, dir_path, isBT):
    count = 0
    merged_data = []
    for single_file in list_file:
        try:
            # 读取并解析JSON文件
            with open(os.path.join(dir_path, single_file), 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "mediaSources" not in data or not isinstance(data["mediaSources"], list):
                print(f"跳过文件 {single_file}：未找到有效的 mediaSources 数组")
                continue
            
            # 处理每个 mediaSource 项，移除 tier 字段
            for source in data["mediaSources"]:
                # 深拷贝避免修改原数据
                cleaned_source = json.loads(json.dumps(source))
                
                # 移除 arguments 中的 tier 字段
                if "arguments" in cleaned_source and "tier" in cleaned_source["arguments"] and isBT:
                    del cleaned_source["arguments"]["tier"]
                
                # 添加到合并列表
                merged_data.append(cleaned_source)
                count += 1

        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {single_file} - {str(e)}")
            continue
        except Exception as e:
            print(f"读取文件时出错: {single_file} - {str(e)}")
            continue
    
    
    return merged_data, count

def write_json(data, file, dir):
    output_data = {
        "exportedMediaSourceDataList": {
            "mediaSources": data
        }
    }

    os.makedirs(dir, exist_ok=True)
    try:
        with open(os.path.join(dir, file), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"写入输出文件时出错：{str(e)}")

def calculate_md5(file_path, block_size=8192):
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(block_size):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        print(f"计算 {file_path} 的MD5失败: {e}")
        return "计算失败"

def main():
    pwd = os.path.dirname(os.path.abspath(__file__))
    dir_BT = os.path.join(pwd, "BT")
    dir_Web = os.path.join(pwd, "Web")
    dir_build = os.path.join(pwd, "build")

    list_BT = os.listdir(dir_BT)
    list_Web = os.listdir(dir_Web)
    
    list_BT.sort()
    list_Web.sort()

    print(f"BT源数量: {len(list_BT)}")
    print(f"在线源数量: {len(list_Web)}")
    
    # 更新MD5
    

    # 合并数据源
    merged_data_BT, count = merge_json(list_BT, dir_BT, True)
    print(f"BT源合并数量: {count}")
    merged_data_Web, count = merge_json(list_Web, dir_Web, False)
    print(f"在线源合并数量: {count}")

    write_json(merged_data_BT, "bt.json", dir_build)
    write_json(merged_data_Web, "web.json", dir_build)

if __name__ == "__main__":
    main()