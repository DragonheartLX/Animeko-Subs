import os
import json

def main():
    # 读取所有数据源文件，并检查格式
    pwd = os.path.dirname(os.path.abspath(__file__))
    dir_BT = os.path.join(pwd, "BT")
    dir_Web = os.path.join(pwd, "Web")
    dir_build = os.path.join(pwd, "build")

    list_BT = os.listdir(dir_BT)
    list_Web = os.listdir(dir_Web)
    
    # BT源
    merged_data_BT = []
    for single_file in list_BT:
        try:
            # 读取并解析JSON文件
            with open(os.path.join(dir_BT, single_file), 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "mediaSources" not in data or not isinstance(data["mediaSources"], list):
                print(f"跳过文件 {single_file}：未找到有效的 mediaSources 数组")
                continue
            
            # 处理每个 mediaSource 项，移除 tier 字段
            for source in data["mediaSources"]:
                # 深拷贝避免修改原数据
                cleaned_source = json.loads(json.dumps(source))
                
                # 移除 arguments 中的 tier 字段
                if "arguments" in cleaned_source and "tier" in cleaned_source["arguments"]:
                    del cleaned_source["arguments"]["tier"]
                
                # 添加到合并列表
                merged_data_BT.append(cleaned_source)

        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {single_file} - {str(e)}")
            continue
        except Exception as e:
            print(f"读取文件时出错: {single_file} - {str(e)}")
            continue
    
    # 在线源
    merged_data_Web = []
    for single_file in list_Web:
        try:
            # 读取并解析JSON文件
            with open(os.path.join(dir_Web, single_file), 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "mediaSources" not in data or not isinstance(data["mediaSources"], list):
                print(f"跳过文件 {single_file}：未找到有效的 mediaSources 数组")
                continue
            
            for source in data["mediaSources"]:
                # 深拷贝避免修改原数据
                cleaned_source = json.loads(json.dumps(source))
                
                # 添加到合并列表
                merged_data_Web.append(cleaned_source)

        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {single_file} - {str(e)}")
            continue
        except Exception as e:
            print(f"读取文件时出错: {single_file} - {str(e)}")
            continue

    output_data = {
        "exportedMediaSourceDataList": {
            "mediaSources": merged_data_BT
        }
    }

    os.makedirs(dir_build, exist_ok=True)
    try:
        with open(os.path.join(dir_build, "bt.json"), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"写入输出文件时出错：{str(e)}")

    output_data = {
        "exportedMediaSourceDataList": {
            "mediaSources": merged_data_Web
        }
    }

    try:
        with open(os.path.join(dir_build, "web.json"), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"写入输出文件时出错：{str(e)}")

if __name__ == "__main__":
    main()