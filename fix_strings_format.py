import os
import re

print(">> Fixing Android String Formatting Errors safely...")

paths = ["app/src/main/res/values/strings.xml", "app/src/main/res/values-ar/strings.xml"]

for path in paths:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. التنظيف الشامل: إزالة أي "formatted" سابقة (سواء كانت مكررة أو مفردة)
        # هذا يمنع خطأ "Attribute formatted was already specified"
        content = content.replace(' formatted="false"', '')
        content = content.replace(' formatted="true"', '')
        content = content.replace('formatted="false"', '')
        content = content.replace('formatted="true"', '')

        # 2. الإصلاح الصحيح: البحث عن النصوص التي تحتوي على % وإضافة %% وإضافة formatted="false"
        def fix_string(match):
            name = match.group(1)
            text = match.group(2)
            
            # إذا كان النص يحتوي على % ولا يحتوي على متغيرات مثل %1$s
            if '%' in text and not re.search(r'%\d+\$[sd]', text):
                text = text.replace('%', '%%')
                return f'<string name="{name}" formatted="false">{text}</string>'
            
            return match.group(0) # إرجاع النص كما هو إذا لم يحتج تعديل

        # نطبق هذا الإصلاح على كل النصوص في الملف
        content = re.sub(r'<string name="([^"]+)">([^<]+)</string>', fix_string, content)

        # 3. حفظ الملف
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f">> Patched safely: {path}")
    else:
        print(f"!! File not found: {path}")