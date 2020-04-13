### Installing development environment

Install python 3.x
python -m venv venv
.\venv\Scripts\activate

make sure you are using a recent pip version, it might be neccesary to install a newer version with
python -m pip install --upgrade pip
pip install --upgrade setuptools

install dependencies with
pip install -r requirements.txt

To run the software
python .\m2q.py 


### Creating a new release
Package the source code into a exe file with PyInstaller by running this command in the project source directory
.\package.bat

Now you can run dist/m2q.exe
