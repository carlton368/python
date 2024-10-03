name = "python"
version = "3.7.7"
authors = ["wonjin LEE"]
description = "Python programming language"

def commands():
    # Use {root} instead of calculating python_root
    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib/python3.7/site-packages")
    env.LD_LIBRARY_PATH.prepend("{root}/lib")
    import os
    # 더 나은 방식 찾을 필요있음(post_install로 테스트시 실패함)
    python_bin_dir = os.path.join("{root}", "bin")
    python_executable = os.path.join(python_bin_dir, "python3.7")
    python_symlink = os.path.join(python_bin_dir, "python")
    python3_symlink = os.path.join(python_bin_dir, "python3")
    if not os.path.exists(python_symlink):
        os.symlink(python_executable, python_symlink)

build_command = "cmake -DCMAKE_INSTALL_PREFIX={root} {root} && cmake --build . --target install_python"

def pre_build_commands():
    import os
    env.REZ_BUILD_CONFIG = "Release"
    env.PATH.prepend(os.path.expanduser("~/cmake-3.26.4/bin"))
