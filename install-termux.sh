#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
pkg install -y python git
cd "$HOME"
if [ ! -d verity ]; then
  git clone https://github.com/jdkabattles/verity.git
fi
cd verity
pip install -e .
echo "installed: $(command -v verity)"
