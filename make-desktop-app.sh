#!/bin/bash
# Português Zero→B1 — 桌面 App 图标安装脚本
# 用法: bash ~/Documents/kimi/workspace/portugues-zero-b1/make-desktop-app.sh
set -e

WS="/Users/benjawork/Documents/kimi/workspace/portugues-zero-b1"
DESK="/Users/benjawork/Desktop"
SRC="$WS/icon-source.png"

if [ ! -f "$SRC" ]; then
  echo "错误: 找不到图标源文件 $SRC" >&2
  exit 1
fi

# 1. 生成 iconset 全套尺寸
ICONSET="$WS/AppIcon.iconset"
mkdir -p "$ICONSET"
cd "$ICONSET"
sips -z 16 16     "$SRC" --out icon_16x16.png      >/dev/null
sips -z 32 32     "$SRC" --out icon_16x16@2x.png   >/dev/null
sips -z 32 32     "$SRC" --out icon_32x32.png      >/dev/null
sips -z 64 64     "$SRC" --out icon_32x32@2x.png   >/dev/null
sips -z 128 128   "$SRC" --out icon_128x128.png    >/dev/null
sips -z 256 256   "$SRC" --out icon_128x128@2x.png >/dev/null
sips -z 256 256   "$SRC" --out icon_256x256.png    >/dev/null
sips -z 512 512   "$SRC" --out icon_256x256@2x.png >/dev/null
sips -z 512 512   "$SRC" --out icon_512x512.png    >/dev/null
sips -z 1024 1024 "$SRC" --out icon_512x512@2x.png >/dev/null

# 2. 打包为 icns
iconutil -c icns . -o "$WS/AppIcon.icns"
echo "✅ AppIcon.icns 生成: $(stat -f%z "$WS/AppIcon.icns") bytes"

# 3. 创建桌面 App 启动器
APP="$DESK/Português Zero→B1.app"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$WS/AppIcon.icns" "$APP/Contents/Resources/AppIcon.icns"

cat > "$APP/Contents/MacOS/launcher" <<'EOF'
#!/bin/bash
# Português Zero→B1 启动器
# 设计：App 进程本身就是服务器（exec 前台运行），launchd 不会回收
DIR="/Users/benjawork/Documents/kimi/workspace/portugues-zero-b1"
PORT=8899
PY="/Users/benjawork/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/.venv/bin/python3"
[ -x "$PY" ] || PY="/usr/bin/python3"

# 服务器已在运行：直接开浏览器
if nc -z 127.0.0.1 $PORT 2>/dev/null; then
  open "http://localhost:$PORT/"
  exit 0
fi

# 2 秒后开浏览器（此后台子任务的父进程是下面的服务器，会一直存活）
( sleep 2; open "http://localhost:$PORT/" ) &

# App 进程变成服务器本体，保持存活
cd "$DIR"
exec "$PY" -m http.server $PORT
EOF
chmod +x "$APP/Contents/MacOS/launcher"

cat > "$APP/Contents/Info.plist" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Português Zero→B1</string>
  <key>CFBundleDisplayName</key><string>Português Zero→B1</string>
  <key>CFBundleIdentifier</key><string>com.benjawork.portugues-zero-b1</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>launcher</string>
  <key>CFBundleIconFile</key><string>AppIcon</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
</dict>
</plist>
EOF

# 4. PNG 图标副本也放桌面
cp "$SRC" "$DESK/portugues-zero-b1-icon.png"

echo "✅ 桌面 App 已创建: $APP"
echo "✅ 图标 PNG 已复制: $DESK/portugues-zero-b1-icon.png"
echo ""
echo "双击桌面上的「Português Zero→B1」即可启动学习仪表盘"
echo "（首次打开如提示安全性，到 系统设置 → 隐私与安全性 点「仍要打开」）"
