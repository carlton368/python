# package.py

name = "python"
version = "3.7.7"

requires = []

build_command = "python3 {root}/build.py {install}"

def commands():
    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib/python3.7/site-packages")
    env.LD_LIBRARY_PATH.prepend("{root}/lib")
    env.PYTHONHOME = "{root}"