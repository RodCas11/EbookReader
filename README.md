# Ebook Fast Reader<br>

### How to install 

First you need to install python and it's dependences<br>

`install python3`<br><br>
After you install python, lets go to dependencies <br><br>
`pip install pypdf2==2.12.1`<br>
`pip install tk` <br>
`pip install time` <br>
`pip install pyinstaller`

Test code

`py .\ebookfreader.py` <br>
`python3 ./ebookfreader.py`

This code opens up a new screen if all the content functionality is working.

then we compile the code

`pyinstaller --onefile ebookfreader.py` <br><br>

the .exe is inside of ./dist.