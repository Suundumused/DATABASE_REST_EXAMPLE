# CSV_DATABASE_REST_EXAMPLE
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
<p>*Start from __init__.py</p>
<h4>Editing database</h4>
<p>*Create csv_file: touch.json file already has a ready example in the "content" key of how columns and lines will be structured.</p>
<p>Add/Edit -- line/column in csv_file. nano.json file: Change value of key "method" to PUT, if key "line" is 0, new column will be created
  and the value assigned to the row, key "column" is column name. If line is greater than 0, it will replace the value of the specified 
  line and column, if the column does not exist, it will automatically create new column and assign value in the line, if the line does not exist either, 
  a new one will be created.</p>
<p>Remove -- line/column in csv_file. nano.json file: Change value of key "method" to DELETE, If the key line has value 0, The entire column specified 
  "column" will be deleted and all values. If the line key is greater than 0, it will delete the value of the specified line and column.</p>
<h4>Reading database</h4>
<p>cat.json: If the "Range" key is [0,0] it will list all lines. If "Range" is [any number,0] it will list lines from "any number" to the end. 
  If "Range" is [valueA, valueB] it will list between this range. If the key "column" value is different from "", it will only list values of this column.</p>
