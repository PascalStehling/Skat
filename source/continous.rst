Continous Delivery
==================

`Travis-CI`_ was used as continuous delivery tool. 
First a Python container is started with version 3.7. 
After that all required libraries are loaded using pip and the requierements.txt. 
Then all tests are executed and the results of the tests are sent to `SonarCloud`_ and `Codacy`_. 
After that the metrics can be calculated and the code can be analyzed. 
The exact pipline can be seen in the .travis.yml

.. _Travis-CI: https://travis-ci.com/
.. _Codacy: https://app.codacy.com/manual/PascalStehling/Skat/dashboard
.. _SonarCloud: https://sonarcloud.io/dashboard?id=PascalStehling_Skat