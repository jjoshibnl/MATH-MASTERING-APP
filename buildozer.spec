[app]

title = Math App
package.name = mathapp
package.domain = org.jatinder
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Force Cython 0.29.x compatible syntax
requirements = python3,kivy==2.2.1,cython==0.29.33

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Standard API and NDK specs
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
