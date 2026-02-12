# -*- coding: utf-8 -*-
import os
import re
import sys

def smart_rename():
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    # 默认正则：包含4个分组（月、日、年、扩展名）
    DEFAULT_REGEX = r'.*_([a-z]{3})_(\d+)_(\d{4})\.([a-z0-9]+)'
    DEFAULT_FORMAT = "File-yyyy-mm-dd.ext"

    print("=== Universal Smart Renamer (Full List Preview) ===")
    
    # --- STEP 1: Directory ---
    while True:
        path = input(f"1. Folder Path (Enter for current dir): ").strip().strip('"') or "."
        if os.path.exists(path): break
        print(f"Error: Path not found: {path}")

    # --- STEP 2: Regex ---
    matched_filenames = []
    pattern = None
    while True:
        print("\n" + "-"*30)
        print(f"2. Regex Pattern (Press Enter for: {DEFAULT_REGEX}):")
        regex_str = input("> ").strip() or DEFAULT_REGEX
        
        try:
            pattern = re.compile(regex_str, re.IGNORECASE)
            all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            matched_filenames = [f for f in all_files if pattern.search(f)]

            if matched_filenames:
                print(f"\n✅ Success! {len(matched_filenames)} files matched:")
                # 修改点：列出所有匹配的文件名
                for i, f in enumerate(matched_filenames, 1):
                    print(f"  {i}. {f}")
                break
            else:
                print("⚠️  No files matched.")
                if input("Retry regex? (y/q): ").lower() == 'q': sys.exit()
        except Exception as e:
            print(f"⚠️  Regex Error: {e}")

    # --- STEP 3: Format ---
    while True:
        print("\n" + "-"*30)
        print("Available Tags: yyyy, mm, mmm, dd, ext")
        print(f"3. Target format (Press Enter for: {DEFAULT_FORMAT}):")
        replace_format = input("> ").strip() or DEFAULT_FORMAT

        matched_tasks = []
        for f in matched_filenames:
            match = pattern.search(f)
            # 确保至少有4个捕获组
            if len(match.groups()) >= 4:
                raw_m, raw_d, raw_y, raw_ext = match.group(1), match.group(2).zfill(2), match.group(3), match.group(4)
                num_m, eng_m = month_map.get(raw_m.lower(), raw_m), raw_m.capitalize()
                
                new_name = replace_format.replace("yyyy", raw_y).replace("mmm", eng_m).replace("mm", num_m).replace("dd", raw_d).replace("ext", raw_ext)
                matched_tasks.append((f, new_name))

        if not matched_tasks:
            print("⚠️  Error: Regex needs 4 groups: (Month) (Day) (Year) (Extension)")
            if input("Retry format? (y/q): ").lower() == 'q': sys.exit()
            continue
        
        # 修改点：在确认前展示所有即将修改的新文件名
        print("\n--- Full Preview of New Filenames ---")
        for i, (old, new) in enumerate(matched_tasks, 1):
            print(f"  {i}. {old}  ==>  {new}")
        
        # --- STEP 4: Execution ---
        print("\n" + "-"*30)
        print("4. Execution Options:")
        print("   [A] Rename ALL files listed above")
        print("   [P] Partial rename (Ask for each file)")
        print("   [R] Restart format selection")
        print("   [Q] Quit")
        
        mode = input("Select an option (a/p/r/q): ").lower()
        if mode == 'q': sys.exit()
        if mode == 'r': continue

        if mode == 'a':
            print("\nRenaming all...")
            for old, new in matched_tasks:
                safe_new = new.replace("/", "-").replace("\\", "-")
                os.rename(os.path.join(path, old), os.path.join(path, safe_new))
                print(f"  Done: {old} -> {safe_new}")
            break

        if mode == 'p':
            print("\nStarting individual confirmation:")
            for old, new in matched_tasks:
                safe_new = new.replace("/", "-").replace("\\", "-")
                confirm = input(f"  Rename '{old}' to '{safe_new}'? (y/n/q): ").lower()
                if confirm == 'y':
                    os.rename(os.path.join(path, old), os.path.join(path, safe_new))
                    print("  [OK]")
                elif confirm == 'q': 
                    print("Stopped.")
                    break
                else:
                    print("  [Skipped]")
            break

if __name__ == "__main__":
    try:
        smart_rename()
    except SystemExit: pass
    input("\nProcess finished. Press Enter to Exit...")