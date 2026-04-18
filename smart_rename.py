# -*- coding: utf-8 -*-
import os
import re
import sys

def smart_rename():
    print("=== Universal Smart Renamer ===")
    print("\n--- Instructions ---")
    print("Example: Rename 'stef_2025_Jun_04-st.doc' to 'F_001-2028-06-04-st.docx'")
    print("1. Regex (to parse 'stef_2025_Jun_04-st.doc'):")
    print("   Regex: (.*)_(\\d{4})_([A-Za-z]{3})_(\\d{2})-(.*)\\.(.*)")
    print("   Mapping: {1}=stef, {2}=2025, {3}=Jun, {4}=04, {5}=st, {6}=doc")
    print("\n2. Target Format (Construction):")
    print("   - No Serial: F-{2}-{3}-{4}-{5}.{6}")
    print("   - With Serial: F_{#}-2028-{3}-{4}-{5}.{6} (Hardcode 2028 if needed)")
    print("-" * 60)

    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    # --- STEP 1: Directory ---
    while True:
        path = input(f"\n1. Folder Path (Enter for current dir): ").strip().strip('"') or "."
        if os.path.exists(path): break
        print(f"⚠️ Error: Path not found: {path}")

    # --- STEP 2: Regex ---
    pattern = None
    matched_filenames = []
    
    while True:
        regex_str = input(f"\n2. Regex Pattern: ").strip()
        if not regex_str:
            print("⚠️ Regex Pattern cannot be empty!")
            continue
            
        try:
            pattern = re.compile(regex_str, re.IGNORECASE)
            all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            matched_filenames = [f for f in all_files if pattern.search(f)]

            if matched_filenames:
                print(f"\n✅ Success! {len(matched_filenames)} files matched:")
                for i, f in enumerate(matched_filenames, 1):
                    print(f"  {i}. {f}")
                
                choice = input("\nAre these the files you want to rename? (y/n/q): ").lower()
                if choice == 'y': break
                elif choice == 'q': sys.exit()
                else: continue
            else:
                print("⚠️ No files matched. Try again.")
        except Exception as e:
            print(f"⚠️ Regex Error: {e}")

    # --- STEP 3: Format ---
    while True:
        print("\n" + "-"*30)
        print("Available Tags: {1}, {2}, {3}... | {#} (serial) | yyyy, mm, mmm, dd, ext")
        replace_format = input("3. Target format: ").strip()
        
        if not replace_format:
            print("⚠️ Target format cannot be empty! (r: Retry / q: Quit)")
            cmd = input("> ").lower()
            if cmd == 'q': sys.exit()
            continue

        matched_tasks = []
        for idx, f in enumerate(matched_filenames, 1):
            match = pattern.search(f)
            groups = match.groups()
            new_name = replace_format
            
            # 1. 动态序号替换 ({1}, {2}...)
            for i, val in enumerate(groups, 1):
                new_name = new_name.replace(f"{{{i}}}", val)
            
            # 2. 序列号注入 {#}
            serial_num = str(idx).zfill(3)
            new_name = new_name.replace("{#}", serial_num)
            
            # 3. 智能标签替换 (兼容性处理)
            if len(groups) >= 1:
                val = groups[0]
                new_name = new_name.replace("yyyy", val)
                if val.lower() in month_map:
                    new_name = new_name.replace("mmm", val.capitalize()).replace("mm", month_map[val.lower()])
                else:
                    new_name = new_name.replace("mm", val.zfill(2))
            if len(groups) >= 2:
                new_name = new_name.replace("mm", groups[1].zfill(2)).replace("dd", groups[1].zfill(2))
            if len(groups) >= 3:
                new_name = new_name.replace("dd", groups[2].zfill(2)).replace("yyyy", groups[2])
            if len(groups) >= 4:
                new_name = new_name.replace("ext", groups[3])

            matched_tasks.append((f, new_name))

        print("\n--- Full Preview ---")
        for i, (old, new) in enumerate(matched_tasks, 1):
            print(f"  {i}. {old}  ==>  {new}")
        
    # --- STEP 4: Execution ---
        print("\n" + "-"*30)
        mode = input("4. Select: [A]ll, [P]artial, [R]estart, [Q]uit: ").lower()
        if mode == 'q': sys.exit()
        if mode == 'r': continue

        if mode in ['a', 'p']:
            for old, new in matched_tasks:
                safe_new = "".join([c for c in new if c not in '<>:"/\\|?*'])
                
                # 修正后的逻辑：只调用一次 input，并保存结果
                if mode == 'p':
                    choice = input(f"  Rename '{old}'? (y/n/q): ").lower()
                    if choice == 'q': break
                    if choice == 'n': 
                        print(f"  Skipped: {old}")
                        continue # 这里使用 continue 直接跳过 rename 步骤
                
                # 执行重命名
                try:
                    os.rename(os.path.join(path, old), os.path.join(path, safe_new))
                    print(f"  Done: {safe_new}")
                except Exception as e:
                    print(f"  Error renaming {old}: {e}")
            break

if __name__ == "__main__":
    try:
        smart_rename()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("\nPress Enter to Exit...")