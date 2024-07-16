echo "Building Nox Launcher..."
cd src/

pyinstaller \
    main.py \
    --clean \
    --name="NoxLauncher" \
    --target-arch="x64_86" \
    --optimize=2 \
    --strip \
    --nowindowed \
    --onefile

mkdir linux

cd linux/

zip NoxLauncher ../assets 
zip NoxLauncher -j ../dist/NoxLauncher

cd ..

zip linux/NoxLauncher -j ../LICENSE

echo "Building complete!"