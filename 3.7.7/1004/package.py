#import os

# current_path = os.environ.get('PWD')
# current_dirname = os.path.dirname(current_path)

# 패키지 이름 정의
name = "python"

# Python 버전 정의
version = "3.7.7"

# 패키지 작성자 리스트
authors = ["wonjin LEE"]

# 패키지에 대한 간단한 설명
description = "Python programming language"

# 패키지에 포함된 도구들의 리스트
tools = [
    "python",
    "python3",
    "pip",
    "pip3"
]

# 런타임 의존성 정의
# 이 패키지는 Linux x86_64 플랫폼에서 실행됨
requires = [
    "platform-linux",
    "arch-x86_64"
]

# 빌드 시 필요한 의존성 정의
build_requires = [
    "cmake-3.10+",  # CMake 3.10 이상 버전 필요
    "make",         # make 빌드 도구 필요
    "gcc"           # GCC 컴파일러 필요
]

# 지원하는 플랫폼 변형 정의
variants = [
    ["platform-linux", "arch-x86_64"]
]

# 환경 설정을 위한 명령어 함수
def commands():
    # PATH 환경 변수에 bin 디렉토리 추가
    env.PATH.prepend("{root}/bin")
    
    # PYTHONPATH에 사이트 패키지 디렉토리 추가
    env.PYTHONPATH.prepend("{root}/lib/python3.7/site-packages")
    
    # LD_LIBRARY_PATH에 lib 디렉토리 추가
    env.LD_LIBRARY_PATH.prepend("{root}/lib")
    
    import os
    
    # Python 실행 파일 경로 설정
    python_bin_dir = os.path.join(str(env.REZ_PYTHON_ROOT), "bin")
    python_executable = os.path.join(python_bin_dir, "python3.7")
    python_symlink = os.path.join(python_bin_dir, "python")
    
    # python3.7에서 python으로의 심볼릭 링크 생성
    if os.path.exists(python_executable) and not os.path.exists(python_symlink):
        os.symlink(python_executable, python_symlink)
        print(f"Created symlink: {python_symlink} -> {python_executable}")
    elif not os.path.exists(python_executable):
        print(f"Error: {python_executable} does not exist.")
    else:
        print(f"Symlink {python_symlink} already exists.")

# 빌드 명령어 정의
build_command = "python3 {root}/build.py"

# 빌드 전 실행될 명령어 함수
def pre_build_commands():
    # 빌드 설정을 Release로 설정
    env.REZ_BUILD_CONFIG = "Release"