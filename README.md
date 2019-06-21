boostnote-dump
==============

This is a utility to convert notes from [Boostnote](https://boostnote.io) to
[Notable](https://github.com/notable/notable), or mostly straight markdown
files. 

Installation
------------
The script requires Python 3.6+.

You'll probably want a virtual environment:

```
python -m venv .venv
```

Then activate the virtual environment, and install the dependencies. For
example: 

```
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Running
-------

```
python boostnote_dump.py <boostnote notes directory> <output directory>
```

The output directory and parents will be created if needed.

"Snippet" notes are currently ignored, as is any note in the trash.

If you're happy with the output, you can copy it to your Notable notes
directory. 
