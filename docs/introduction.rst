Introduction
============
Composite project had began as a layer between XML (and xml like) documents and JSON in a
*already in production* project to move obsolete xml schema towards JSON compatible.

Though this didn't happen **composite** solved its issue designed for.
It can maintain layer of compatibility between different document formats and
allow user work with them in ODM/ORM style.

For example you have strict xml document schema:

.. code-block:: xml

  <?xml version="1.0" encoding="utf-8"?>
  <Company>
      <ceo first_name="Alexander" last_name="Pepyako" age="23"
            gender="male" phone="+79110010203" email="com@alexander.pepyako">
          <id>1</id>
          <sign>Pepyako inc.</sign>
      </ceo>
      <title>Pepyako industries</title>
      <address>Third Vydrokushskaya street, 7 building</address>
      <company_type>GHMb</company_type>
  </Company>

You would probably want to have python like object to handle its data, bind
different methods to it to maintain your own business logic and in final you want
to serialize this document to JSON or vice versa.

.. code-block:: json

  {
  "ceo": {
    "_attributes": {
      "first_name": "Alexander",
      "last_name": "Pepyako",
      "age": 23,
      "gender": "male",
      "phone": "+79110010203",
      "email": "com@alexander.pepyako"
    },
    "id": 1,
    "sign": "Pepyako inc."
  },
    "title": "Pepyako industries",
    "address": "Third Vydrokushskaya street, 7 building",
    "company_type": "GHMb"
  }

Useful links
------------
- You search for ODM/ORM library to handle JSON-like schemas, look for
  `marshmallow project <http://marshmallow.readthedocs.org/en/latest>`_

