#!/bin/bash
# Version macOS de run.sh : même container, sans l'affichage X11 ni /dev (n'existent pas sur Mac).
# 1) une seule fois :  docker build -t ghcr.io/epflxplore/base:humble-desktop -f Dockerfile.local .
# 2) à chaque fois  :  ./run_mac.sh
cd "$(dirname "$0")" || exit 1
parent_dir="$(cd .. && pwd)"     # le dépôt entier est monté dans ~/dev_ws/src du container

docker run -it \
    --name base_humble_desktop \
    --rm \
    -e QT_X11_NO_MITSHM=1 \
    -v "$parent_dir":/home/xplore/dev_ws/src \
    -v base_humble_desktop_home_volume:/home/xplore \
    ghcr.io/epflxplore/base:humble-desktop
