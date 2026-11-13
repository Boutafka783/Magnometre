import os

print(">> Fixing Android String Formatting Errors...")

paths = ["app/src/main/res/values/strings.xml", "app/src/main/res/values-ar/strings.xml"]

for path in paths:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. إصلاح علامات النسبة المئوية (استبدال % بـ %%)
        content = content.replace("2%–98%", "2%%–98%%")
        content = content.replace("تلقائي (2%–98%)", "تلقائي (2%%–98%%)")
        
        # 2. تنظيف أي تكرار للخاصية formatted="false" نتج عن سكربتات سابقة
        content = content.replace(' formatted="false" formatted="false"', ' formatted="false"')
        content = content.replace(' formatted="false"formatted="false"', ' formatted="false"')

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f">> Patched {path}")
    else:
        print(f"!! File not found: {path}")
