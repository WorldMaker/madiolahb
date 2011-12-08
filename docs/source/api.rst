API
===

Madiolahb is intended to provide a simple isomorphic API across a number
of useful platforms: Python, RESTful HTTP, and even from the command
line. It is written in pure Python so that it should be useful to things
written in Python itself and to any environments where Python may be
hosted as a scripting language such as C/C++ or .NET.

This API will be described by Python calls using Python dictionaries as
data formatting. The data will be the equivalent structure of the
:doc:`json` standards.

Play by Command Line
--------------------

One means that the API described here can be explored is to make use of
the command line :command:`madiolahb` script. This script is a UNIX-like
script that defaults to taking in a JSON file on standard input and
outputting a JSON file to standard out. (This means that you can pipe
together multiple commands.) If you have a Python YAML library installed
it can also support YAML input/output.

Using just this tool you could, for example, play a Bhaloidam game of a
sort using a file store such as Dropbox or a source control system.

.. vim: ai spell tw=72
