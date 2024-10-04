import os
import sys
import subprocess
import hashlib
import tarfile
import urllib.request
from pathlib import Path

class PythonBuilder:
    def __init__(self):
        self.python_version = "3.7.7" 
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/Python-{self.python_version}.tgz"
        self.python_sha256 = "8c8be91cd2648a1a0c251f04ea0bb4c2a5570feb9c45eaaa2241c785585b475a" # SHA256 hash(링크에 있는 파일의 해시값)
        self.install_prefix = os.environ.get('REZ_BUILD_INSTALL_PATH', '/usr/local') 
        self.source_dir = Path('Python-source') # 현재 디렉토리에 있는 'Python-source'를 의미 (존재여부 상관 없음) 
        self.build_dir = Path('Python-build')

    def download_source(self):
        """
        Download Python source code if it doesn't already exist.
        """
        
        if not self.source_dir.exists():    # 'Python-source' 디렉토리가 존재하지 않으면
            print(f"!Downloading Python {self.python_version}...!")
            filename, _ = urllib.request.urlretrieve(self.python_url)
            
            # Verify SHA256
            sha256_hash = hashlib.sha256()
            with open(filename, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() != self.python_sha256:
                raise ValueError("!Downloaded file hash does not match expected hash!")
            
            # Extract
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall(path=self.source_dir)
            
            os.remove(filename)
        else:
            print("Source directory already exists, skipping download.")

    def configure(self):
        os.makedirs(self.build_dir, exist_ok=True)
        os.chdir(self.build_dir)
        configure_cmd = [
            f"{self.source_dir}/Python-{self.python_version}/configure",
            f"--prefix={self.install_prefix}",
            "--enable-shared",
            "--with-ensurepip=install"
        ]
        subprocess.run(configure_cmd, check=True)

    def build(self):
        subprocess.run(["make", "-j4"], check=True)

    def install(self):
        subprocess.run(["make", "install"], check=True)

    def create_symlinks(self):
        bin_dir = Path(self.install_prefix) / "bin"
        python_executable = bin_dir / f"python{self.python_version.rsplit('.', 1)[0]}"
        python_symlink = bin_dir / "python"
        
        if python_executable.exists() and not python_symlink.exists():
            os.symlink(python_executable, python_symlink)
            print(f"Created symlink: {python_symlink} -> {python_executable}")
        elif not python_executable.exists():
            print(f"Error: {python_executable} does not exist.")
        else:
            print(f"Symlink {python_symlink} already exists.")

    def run(self):
        self.download_source()
        self.configure()
        self.build()
        self.install()
        self.create_symlinks()
        print(f"Python {self.python_version} installation complete.")

if __name__ == "__main__":
    builder = PythonBuilder()
    builder.run()