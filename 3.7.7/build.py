# build.py

import os
import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: build.py <install_dir>")
        sys.exit(1)

    install_dir = sys.argv[1]

    # Python 소스 코드 다운로드 및 압축 해제
    python_version = "3.7.7"
    tarball = f"Python-{python_version}.tgz"
    if not os.path.exists(tarball):
        subprocess.check_call([
            "curl",
            "-O",
            f"https://www.python.org/ftp/python/{python_version}/Python-{python_version}.tgz"
        ])

    subprocess.check_call(["tar", "xzf", tarball])

    # Python 컴파일 및 설치
    os.chdir(f"Python-{python_version}")
    subprocess.check_call([
        "./configure",
        f"--prefix={install_dir}",
        "--enable-shared"
    ])
    subprocess.check_call(["make"])
    subprocess.check_call(["make", "install"])
    print(f"Python {python_version} successfully built and installed to {install_dir}.")


if __name__ == "__main__":
    main()
