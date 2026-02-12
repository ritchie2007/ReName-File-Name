import os
import re

def smart_rename():
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    print("=== Python 智能万能重命名工具 (严谨版) ===")
    
    # 第 1 步：确定路径
    while True:
        path = input("1. 请输入目标文件夹路径 (直接回车表示当前目录): ").strip().strip('"') or "."
        if os.path.exists(path):
            break
        print(f"❌ 路径不存在: {path}，请重新输入。")

    # 第 2 步：正则表达式匹配 (循环直到匹配成功)
    matched_filenames = []
    pattern = None
    
    while True:
        print("\n" + "-"*30)
        print("2. 输入匹配正则表达式 (需包含3个括号，分别对应 月、日、年):")
        print("   示例: .*_([a-z]{3})_(\\d+)_(\\d{4})\\.pdf")
        regex_str = input("> ").strip()
        
        try:
            pattern = re.compile(regex_str, re.IGNORECASE)
            all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            matched_filenames = [f for f in all_files if pattern.search(f)]

            if matched_filenames:
                print(f"✅ 成功匹配到 {len(matched_filenames)} 个文件！")
                print("匹配到的前3个文件示例：")
                for f in matched_filenames[:3]:
                    print(f"  - {f}")
                break  # 匹配成功，跳出循环进入下一步
            else:
                print("⚠️ 匹配失败！该目录下没有任何文件名符合此正则。")
                print("提示：请检查拼写、下划线位置，或是否漏掉了扩展名 .pdf")
                # 停留在此循环，重新输入正则
                
        except Exception as e:
            print(f"⚠️ 正则语法错误: {e}")

    # 第 3 步：设定目标格式
    while True:
        print("\n" + "-"*30)
        print("3. 输入目标格式 (可用: yyyy, mm, mmm, dd):")
        print("   示例: 房贷-yyyy-mm-dd.pdf")
        replace_format = input("> ").strip()

        matched_tasks = []
        for f in matched_filenames:
            match = pattern.search(f)
            
            # 提取并转换
            raw_m = match.group(1)
            raw_d = match.group(2).zfill(2)
            raw_y = match.group(3)
            
            num_m = month_map.get(raw_m.lower(), raw_m)
            eng_m = raw_m.capitalize()
            
            new_name = replace_format.replace("yyyy", raw_y).replace("mmm", eng_m).replace("mm", num_m).replace("dd", raw_d)
            matched_tasks.append((f, new_name))

        print("\n--- 重命名预览 (前5个) ---")
        for old, new in matched_tasks[:5]:
            print(f"  {old}  ==>  {new}")

        confirm = input("\n确认执行以上重命名？(y=执行 / n=重新输入格式 / q=退出): ").lower()
        if confirm == 'y':
            for old, new in matched_tasks:
                safe_new_name = new.replace("/", "-").replace("\\", "-")
                os.rename(os.path.join(path, old), os.path.join(path, safe_new_name))
            print("🎉 恭喜！批量重命名成功完成。")
            break
        elif confirm == 'q':
            break

if __name__ == "__main__":
    smart_rename()
    input("\n按回车键结束...")