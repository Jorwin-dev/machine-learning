#!/bin/bash
docker run -it \
   --device=/dev/kfd \
   --device=/dev/dri \
   --privileged \
   --user=$(id -u) \
   -p 8080:8080 \
   -e DISPLAY=$DISPLAY \
   -e QT_X11_NO_MITSHM=1\
   -e PYVISTA_USERDATA_PATH=./tmp\
   -e HOME=/app \
   --workdir=/app \
   --volume="$PWD":/app \
   --volume="/etc/group:/etc/group:ro" \
   --volume="/etc/passwd:/etc/passwd:ro" \
   --volume="/etc/shadow:/etc/shadow:ro" \
   --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
   --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
   sdf python $1 $2 $3 $4 $5 $6 $7 $8 $9
