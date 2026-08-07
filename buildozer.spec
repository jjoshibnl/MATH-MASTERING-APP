[app]

# (str) Title of your application
title = Math App

# (str) Package name
package.name = mathapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.jatinder

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Presumed orientation ("all", "portrait", "landscape", "square")
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use (Using 25b prevents NDK r28c build failures)
android.ndk = 25b

# (str) Android Build Tools version
android.build_tools_version = 34.0.0

# (bool) Automatically accept Android SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for (Using single architecture arm64-v8a prevents multi-arch build crash)
android.archs = arm64-v8a

# (bool) Copy library instead of making a symlink
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
