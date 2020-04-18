### Installing development environment

Install python 3.x

Create a virtualenv and activate it

``` python -m venv venv ```

```.\venv\Scripts\activate ```

make sure you are using a recent pip version, it might be neccesary to install a newer version with

``` python -m pip install --upgrade pip ```

install dependencies with

``` pip install -r requirements.txt ```

To run the software

``` python .\m2q.py ```

### Creating a new release
in VS Code you can run unittests, lint and packge with the shortcut
``` Shift + Ctrl + B ```

Now you can run the application from dist/m2q.exe