import os
import sys
import subprocess
import urllib.request
import tarfile

class PythonBuilder:
    def __init__(self):
        # Python 버전과 다운로드 URL 설정
        self.python_version = "3.7.7"
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/Python-{self.python_version}.tgz"
        
        # 설치 경로 설정 (기본값은 /usr/local)
        self.install_path = os.environ.get('PYTHON_INSTALL_PATH', '/usr/local')
        
        # 소스 코드와 빌드 디렉토리 이름 설정
        self.source_dir = "Python-source"
        self.build_dir = "Python-build"

    def download_source(self):
        print(f"Python {self.python_version} 소스 코드 다운로드 중...")
        
        # 소스 코드 다운로드
        source_file, _ = urllib.request.urlretrieve(self.python_url)
        
        # 다운로드한 파일 압축 해제
        with tarfile.open(source_file, 'r:gz') as tar:
            tar.extractall(path=self.source_dir)
        
        print("다운로드 및 압축 해제 완료")

    def configure(self):
        print("Python 빌드 설정 중...")
        
        # 빌드 디렉토리 생성
        os.makedirs(self.build_dir, exist_ok=True)
        os.chdir(self.build_dir)
        
        # configure 스크립트 실행
        configure_command = [
            f"../{self.source_dir}/Python-{self.python_version}/configure",
            f"--prefix={self.install_path}",
            "--enable-shared",
            "--with-ensurepip=install"
        ]
        subprocess.run(configure_command, check=True)
        
        print("빌드 설정 완료")

    def build(self):
        print("Python 빌드 중...")
        
        # make 명령어로 빌드
        subprocess.run(["make", "-j4"], check=True)
        
        print("빌드 완료")

    def install(self):
        print("Python 설치 중...")
        
        # make install 명령어로 설치
        subprocess.run(["make", "install"], check=True)
        
        print(f"Python {self.python_version} 설치 완료")

    def run(self):
        try:
            self.download_source()
            self.configure()
            self.build()
            self.install()
            print(f"Python {self.python_version}이 {self.install_path}에 성공적으로 설치되었습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")
            sys.exit(1)

if __name__ == "__main__":
    builder = PythonBuilder()
    builder.run()