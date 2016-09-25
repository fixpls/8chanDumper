8chanDumper
------------------------------

A directory dumper for 8chan ([8ch.net](https://8ch.net)).

Provide a directory, board and thread and 8chanDumper will post all files from the directory alphabetically up to 5 at a time using 8chan's multi-upload feature.


Requirements
--------------------
* Python 3
* Requests (https://github.com/kennethreitz/requests) and RequestsToolBelt (https://pypi.python.org/pypi/requests-toolbelt)


Limitations & Notes
--------------------
* Only works for [8chan](https://8ch.net), could be tweaked to support other imageboards based off 8chan.
* Only tested on Linux so far, it probably works with Windows.
* 8chanDumper supports all filetypes 8chan supports, however some boards may have filetypes disabled, the program doesn't check for that yet so please be careful.
* Will not work on boards with Captcha-per-post enabled.
* [8chan's DNSBL](https://8ch.net/dnsbls_bypass.php) will invisibly prevent posts from getting through if it crops up, the program doesn't check for it yet so please ensure you have filled it every 50-75 or so posts.
* Do not post from the same IP Address 8chanDumper is running from, otherwise flood detection will mess both your posts and the script up.
* Beware of very large filesizes, at the moment 8chanDumper uses 8chan's multi-uploader to blindly upload as many files as possible per post, if the total filesize exceeds the current filesize limit on 8chan the post will not get through.
* Irresponsible use of this script is likely to get you banned. Some sites/boards may not want you dumping. Act accordingly.


Instructions
--------------------
See `python 8chanDumper -h` for details.

To start, run `python 8chanDumper <Directory> <Board> <Thread>`


If you find a bug please make a thread on [/test/](https://8ch.net/test) detailing it and I'll probably notice it.


License
--------------------
MIT License

Copyright (c) 2016 fixpls <fixpls@openmailbox.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.