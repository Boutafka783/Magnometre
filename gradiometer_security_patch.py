import os
import re

ROOT = os.getcwd()
GRADLE_FILE = os.path.join(ROOT, "app", "build.gradle.kts")
MANIFEST = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
MAIN_ACTIVITY = os.path.join(ROOT, "app", "src", "main", "java", "io", "mycompany", "gradiometer", "MainActivity.kt")
PROGUARD = os.path.join(ROOT, "app", "proguard-rules.pro")

def read(p):
    if not os.path.exists(p): return ""
    with open(p, "r", encoding="utf-8") as f: return f.read()

def write(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(c)

print(">> Applying Gradiometer Security Hardening Patch...")

# 1) تفعيل R8 وتشفير الكود
if os.path.exists(GRADLE_FILE):
    g = read(GRADLE_FILE)
    # تفعيل Minify وتقليص الموارد
    g = g.replace("isMinifyEnabled = false", "isMinifyEnabled = true")
    if "isShrinkResources" not in g:
        g = g.replace("isMinifyEnabled = true", "isMinifyEnabled = true\n            isShrinkResources = true")
    
    # إضافة ملف قواعد ProGuard
    if "proguardFiles" not in g:
        g = g.replace("isMinifyEnabled = true", 'isMinifyEnabled = true\n            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")')
    write(GRADLE_FILE, g)
    print(">> Enabled R8 Obfuscation and ProGuard in build.gradle.kts")

# 2) إنشاء قواعد ProGuard المخصصة لحماية Firebase و Bluetooth
proguard_rules = """
# Keep Bluetooth & Firebase models
-keep class io.mycompany.gradiometer.bluetooth.** { *; }
-keep class io.mycompany.gradiometer.community.** { *; }
-keep class com.google.firebase.** { *; }
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.firebase.**

# Keep Jetpack Compose
-keep class androidx.compose.runtime.** { *; }
-keep class androidx.compose.ui.** { *; }

# Keep JavascriptInterface (if any)
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
"""
write(PROGUARD, proguard_rules)
print(">> Generated proguard-rules.pro")

# 3) تأمين المانيفست (منع النسخ الاحتياطي، منع الاتصال غير المشفر، منع تصوير الشاشة)
if os.path.exists(MANIFEST):
    m = read(MANIFEST)
    if 'android:allowBackup="false"' not in m:
        m = m.replace('<application', '<application\n        android:allowBackup="false"\n        android:usesCleartextTraffic="false"\n        android:networkSecurityConfig="@xml/network_security_config"', 1)
    
    # إضافة صلاحية منع تصوير الشاشة (إذا كان أندرويد 14+)
    if "android:windowOptOutEdgeToEdgeEnforcement" not in m:
        pass # لا نحتاجها هنا، سنستخدم FLAG_SECURE برمجياً
        
    write(MANIFEST, m)
    print(">> Secured AndroidManifest.xml (allowBackup=false, cleartext=false)")

# 4) إنشاء ملف network_security_config.xml
nsc = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
"""
write(os.path.join(ROOT, "app", "src", "main", "res", "xml", "network_security_config.xml"), nsc)
print(">> Created network_security_config.xml (forces HTTPS)")

# 5) حماية شاشة المسح (منع تصوير الشاشة) وإضافة RASP بسيط
if os.path.exists(MAIN_ACTIVITY):
    ma = read(MAIN_ACTIVITY)
    if "FLAG_SECURE" not in ma:
        # حقن الكود بعد super.onCreate
        injection = """
        // 🛡️ Security: Prevent Screenshots of survey data
        window.setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE, android.view.WindowManager.LayoutParams.FLAG_SECURE)
        
        // 🛡️ Security: Basic Anti-Root Check
        val rootPaths = arrayOf("/system/app/Superuser.apk", "/sbin/su", "/system/bin/su", "/system/xbin/su", "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/xbin/su", "/system/bin/failsafe/su", "/data/local/su", "/su/bin/su")
        if (rootPaths.any { java.io.File(it).exists() }) {
            android.widget.Toast.makeText(this, "⚠️ Security Warning: Rooted device detected!", android.widget.Toast.LENGTH_LONG).show()
        }
        """
        ma = ma.replace("super.onCreate(savedInstanceState)", "super.onCreate(savedInstanceState)\n" + injection, 1)
        write(MAIN_ACTIVITY, ma)
        print(">> Injected FLAG_SECURE and RASP into MainActivity.kt")

print(">> Gradiometer Security Hardening Patch Applied Successfully!")