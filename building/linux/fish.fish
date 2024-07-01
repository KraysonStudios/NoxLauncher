echo "Building Nox Launcher..."
cd src/
fish_add_path -g -p /usr/bin/flutter/bin/

flet build linux \
    --project="NoxLauncher" \
    --description="Nox Launcher is a powerful and easy-to-use launcher for Minecraft develop by Krayson Studio." \
    --product="NoxLauncher" \
    --build-number=100 \
    --build-version="1.0.0" \
    -vv