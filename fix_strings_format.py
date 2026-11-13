import os
import re

print(">> Fixing String Formatting Errors...")

for path in ["app/src/main/res/values/strings.xml", "app/src/main/res/values-ar/strings.xml"]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # إصلاح الخطأ الشائع في setup.py للنسبة المئوية
        content = content.replace("Auto (2%–98%)", "Auto (2%%–98%%)")
        content = content.replace("تلقائي (2%–98%)", "تلقائي (2%%–98%%)")
        
        # إضافة formatted="false" لكل النصوص التي تحتوي على علامة % كاحتياط إضافي
        content = re.sub(r'<string name="(.*?)">(.*?%%.*?)</string>', r'<string name="\1" formatted="false">\2</string>', content)
        content = re.sub(r'<string name="(.*?)">(.*?[^%]%[^%].*?)</string>', r'<string name="\1" formatted="false">\2</string>', content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f">> Patched {path}")