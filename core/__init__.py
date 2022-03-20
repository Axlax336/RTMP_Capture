import os
import sys

# 设置VLC库路径
current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
vlcpath = os.path.join(current_path, "vlc-3.0.16")
libvlcpath = os.path.join(vlcpath, "libvlc.dll")
os.environ['PYTHON_VLC_MODULE_PATH'] = vlcpath
os.environ['PYTHON_VLC_LIB_PATH'] = libvlcpath
