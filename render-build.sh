#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Download ffmpeg static binary
FFMPEG_DIR=$HOME/ffmpeg
if [ ! -d "$FFMPEG_DIR" ]; then
  mkdir -p $FFMPEG_DIR
  cd $FFMPEG_DIR
  curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ --strip-components=1
  cd -
fi

# Make it accessible
export PATH=$PATH:$HOME/ffmpeg
