Build Management
================

The main build management tool used was `Bazel`_. 
With this tool it is possible to build a Skat.exe and execute the tests. 
In order to use Bazel, a BUILD.bazel file must be written, which contains all the necessary information about the individual files and the relationships between them. 
This file can be found in the root folder of this project.
To build the .exe the command *bazel build Skat* can be executed in the root folder. 
This will create a Skat.exe in the bazel-bin folder. 
To run the tests, the command *bazel run test* can be used. 
For more information on installing `Bazel`_, please visit their website.

For further automation the tool `doit`_ can also be used. 
With this tool all unit tests can be executed with the command *doit run_test*. 
In addition, a coverage.xml is created which contains all information about the coverage of the code. 
Furthermore, with the command *doit lint_modules* all files in the folder modules can be viewed with pylint. 
With the command *doit bazel_build* the Skat.exe can be built with bazel. 
To use `doit`_ you just have to install all the required libraries with *pip install -r requirements.txt*.

.. _Bazel: https://bazel.build/
.. _doit: https://pydoit.org/contents.html#