import os
import sys
import subprocess
import urllib.request
import tarfile
import shutil

"""success"""
class PythonBuilder:
    def __init__(self):
        self.python_version = "3.7.7"
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/Python-{self.python_version}.tgz"
        
        # Rez 패키지 구조에 맞는 설치 경로
        self.install_path = os.environ.get('REZ_BUILD_INSTALL_PATH')
        if not self.install_path:
            raise ValueError("REZ_BUILD_INSTALL_PATH 환경 변수가 설정되지 않았습니다.")
        
        self.source_dir = os.path.join(os.getcwd(), "Python-source")
        self.build_dir = os.path.join(os.getcwd(), "Python-build")

    def download_source(self):
        print(f"Python {self.python_version} 소스 코드 다운로드 중...")
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        os.makedirs(self.source_dir)
        source_file, _ = urllib.request.urlretrieve(self.python_url)
        with tarfile.open(source_file, 'r:gz') as tar:
            tar.extractall(path=self.source_dir)
        os.remove(source_file)
        print("다운로드 및 압축 해제 완료")

    def configure(self):
        print("Python 빌드 설정 중...")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
        os.chdir(self.build_dir)
        configure_command = [
            os.path.join(self.source_dir, f"Python-{self.python_version}", "configure"),
            f"--prefix={self.install_path}",
            "--enable-shared",
            "--with-ensurepip=install"
        ]
        subprocess.run(configure_command, check=True)
        print("빌드 설정 완료")

    def build(self):
        print("Python 빌드 중...")
        subprocess.run(["make", "-j4"], check=True)
        print("빌드 완료")

    def install(self):
        print("Python 설치 중...")
        subprocess.run(["make", "install"], check=True)
        print(f"Python {self.python_version} 설치 완료")

    def create_symlinks(self):
        print("심볼릭 링크 생성 중...")
        bin_dir = os.path.join(self.install_path, "bin")
        python_exec = os.path.join(bin_dir, f"python{self.python_version.rsplit('.', 1)[0]}")
        python_symlink = os.path.join(bin_dir, "python")
        if os.path.exists(python_exec) and not os.path.exists(python_symlink):
            os.symlink(python_exec, python_symlink)
        print("심볼릭 링크 생성 완료")

    def cleanup(self):
        print("정리 중...")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.build_dir)
        print("정리 완료")

    def run(self):
        try:
            self.download_source()
            self.configure()
            self.build()
            self.install()
            self.create_symlinks()
            self.cleanup()
            print(f"Python {self.python_version}이 {self.install_path}에 성공적으로 설치되었습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")
            sys.exit(1)

if __name__ == "__main__":
    builder = PythonBuilder()
    builder.run()