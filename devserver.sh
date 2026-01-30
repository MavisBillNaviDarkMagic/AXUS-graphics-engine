#!/bin/sh
export PATH="$HOME/.local/bin:$PATH"

poetry install
source .venv/bin/activate

if ! grep -q "$PATH" /home/user/.bashrc; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/user/.bashrc
fi

# Apuntamos al nuevo corazón de Flask y usamos el puerto 8080 para evitar conflictos
python -u -m flask --app src/app run --debug --port=8080
