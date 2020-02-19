### Creating a new release
Package the source code into a exe file with PyInstaller by running this command in the project source directory

```
pyinstaller m2q.py --onefile --icon=m2q.ico --add-data "m2q.ico;." --add-data "m2q-logo-v2.png;." --add-data "m2q-logo-v2-text.png;."
```
