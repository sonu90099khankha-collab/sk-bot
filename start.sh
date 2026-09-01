#!/usr/bin/env bash
if [ ! -d "node-v18.16.0-linux-x64" ]; then
    echo "Downloading Node.js..."
    curl -O https://nodejs.org/dist/v18.16.0/node-v18.16.0-linux-x64.tar.xz
    tar -xf node-v18.16.0-linux-x64.tar.xz
    rm node-v18.16.0-linux-x64.tar.xz
fi
export PATH="$PWD/node-v18.16.0-linux-x64/bin:$PATH"
python3 bot.py
