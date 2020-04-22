# pydb
A JSON file-based light Python database.
<br>
<h1>Installation</h1>
PyDB does NOT require installation(not recommended to do that for now, PyDB in pip is coming soon). Just download pydb.py from this repo.
<br>
The installation of cryptography package is required for the PyDB.Encryption class.
<br>
<code>pip install cryptography</code>
<br>
PyDB is pretty easy to learn. Below is an example.
<br>
<code>
from pydb import PyDB<br>
<br>
db = PyDB("test.json")<br>
<br>
db.add("name", "John");<br>
db.commit() # Commit changes to file
<br>
print(db.get("name")) # Output: John
</code>
