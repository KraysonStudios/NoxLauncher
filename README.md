<p align="center">
   <img alt= "NoxLauncher logo" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/assets/icon.png" style= "width: 75%; height: 55%;">
</p>

<h1 align="center">NoxLauncher</h1>

<p align="center">
   <img alt= "NoxLauncher Home page" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/github-assets/home.png" style= "width: 75%; height: 55%;">
</p>

**NoxLauncher** is a powerful **Open Source** launcher created by **Krayson Studio** and its main developers, to provide secure access and fast to a minecraft launcher. 

> [!NOTE]  
> **This launcher is not affiliated with Mojang Studios and their games.**

> [!WARNING]  
> Any error caused by the **user's interference** with the launcher's configuration center is not considered an error or bug of the launcher.

<!---
Discord Markdown Badge API
https://github.com/gitlimes/discord-md-badge?
-->
[![](https://dcbadge.limes.pink/api/server/https://discord.com/invite/DWfuQRsxwb)](https://discord.com/invite/DWfuQRsxwb)

## Features 🎉

### Support the almost popular modloaders 🕹️

- **[Fabric](https://fabricmc.net/)**
- **[Forge](https://files.minecraftforge.net/net/minecraftforge/forge/)**

### Automatic installation of mods via Modrinth 🚀

- **Fabric** mods
- **Forge** mods

<p align="center">
   <img alt= "NoxLauncher Modrinth page" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/github-assets/modrinth.png" style= "width: 75%; height: 55%;">
</p>

<p align="center">
   <img alt= "NoxLauncher Modrinth page" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/github-assets/modrinth-dropdown.png" style= "width: 75%; height: 55%;">
</p>

### Easy to Use and configurable 👑

- Is **extremely configurable** launcher of Minecraft.

<p align="center">
   <img alt= "NoxLauncher Settings page" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/github-assets/settings.png" style= "width: 75%; height: 55%;">
</p>

<p align="center">
   <img alt= "NoxLauncher Customization page" src= "https://github.com/KraysonStudios/NoxLauncher/blob/master/github-assets/customization.png" style= "width: 75%; height: 55%;">
</p>

### Solid as an rock 🪨

- The **official** releases are completely stable and almost **problem-free**.

### Fast ⚡

- On comparasion with others minecraft launchers and mostly with official Minecraft Launcher; **Nox Launcher** is blazingly fast on startup. 

### Multiplatform 💻

- **Windows**
- **Linux**

### FOSS 👐

- If you want to know if the launcher is a *virus*, have the source code at hand, wink wink...

-------------------------------------------

# System dependencies 💻

## Linux

   - **libmpv.so**

   ### Installation

   - Distributions derived from Arch: `sudo pacman -S mpv && sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1`
   - Distributions derived from Ubuntu/Debian: `sudo apt install libmpv-dev mpv && sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1`

-------------------------------------------

# Build dependencies 🏗️

## Python

- minecraft-launcher-lib==6.5
- flet==0.24.1
- flet-contrib==2024.3.6
- pypresence==4.3.0
- psutil==6.1.0
- colorama==0.4.6

### python >= 3.12

## Rust

- zip

### rust >= 1.18.0

## External tools needed

- upx https://github.com/upx/upx (for optimization)
- cargo https://github.com/rust-lang/cargo (for build NoxLauncher Updater)

### Command

`python build.py <platform>`
