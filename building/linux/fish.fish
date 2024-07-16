echo "Building Nox Launcher..."
cd src/

flet build linux \
    --project="NoxLauncher" \
    --description="Nox Launcher is a powerful and easy-to-use Minecraft Launcher develop by Krayson Studio." \
    --product="NoxLauncher" \
    --build-number=100 \
    --build-version="1.0.0" \
    -vv