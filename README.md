# TXT_DATABASE_REST_EXAMPLE
<p align="center"># Creative Commons Zero v1.0 Universal -- @Caio Silva signed as Suundumused</p>
Simple client and HTTP interactions for handling text files.

<h3>Requirements</h2>
<p>*Python versions from 3.6.3 to 3.11..</p>
<p>*Last version of modules for that version of python.</p>
<p></p>
<h3>Server</h3>
<p>*use -ip or --host to change IP.</p>
<p>*use -p or --port to change port.</p>
<p>*Start from main.py.</p>
<p></p>
<h3>Client</h3>
<p>*In the client app, change the contents of the requests folder like IP, method and the content.</p>
<p>*First option type 1, then the file name including the json extension to run the script.</p>
<p>*Keep the file's structure for each method.</p>
<h4>Editing database</h4>
<p>*Create csv_file: touch.json file already has a ready example in the "content" key of how columns and lines will be structured.</p>
<p>*Add/Edit --  line/column csv_file: nano.json file: Change value of key "method" to PUT, if key "line" is 0, new column will be created, key 
  "column" is column name. If line is greater than 0, it will replace the value of the specified line and column, if the column does not 
  exist, it will automatically create new column and assign value in the line, if the line does not exist either, a new one will be created.</p>
<p>*Start from __init__.py</p>
