[app]
title = SystemService
package.name = systemservice
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 0.1
requirements = python3,kivy,requests,openssl,pyjnius

[buildozer]
log_level = 2

[android]
api = 30
minapi = 24
ndk = 25b
android.ndk_path = 
android.allow_backup = True
android.permissions = CAMERA,RECORD_AUDIO,READ_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,READ_CONTACTS,READ_SMS,INTERNET,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE

[android.entrypoint]
main = main.py

[android.app]
presplash.color = #000000
fullscreen = 1
orientation = portrait

[buildozer.android]
build_tools_version = 30.0.3
android_sdk_path = 
android_ndk_path = 