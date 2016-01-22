1. Make class for reading document (*documents.py*)

    .. code-block:: python

      from composite import Document, fields


      class User(Document):
          id = fields.Field(name='id', type=int)
          sign = fields.Field(name='sign', type=str)

          def get_user_name(self):
              if self.get_attributes():
                  return '%s %s' % (self.attributes.first_name,
                                    self.attributes.last_name)
              return self.id

          def __str__(self):
              return '%s' % self.attributes.first_name

          class Attributes:
              first_name = fields.AttributeField(name='first_name', type=str)
              last_name = fields.AttributeField(name='last_name', type=str)
              age = fields.AttributeField(name='age', type=int)
              gender = fields.AttributeField(name='gender', type=str)
              phone = fields.AttributeField(name='phone', type=str)
              email = fields.AttributeField(name='email', type=str)

      class Company(Document):
      """
      Company document

      :param str title: title
      :param str address: address
      :param str company_type: company type
      :param User ceo: company CEO user profile
      """
      title = Field('title', str)
      address = Field('address', str)
      company_type = Field('company_type', str)
      ceo = Node('ceo', type=User)

      def __str__(self):
          return self.ceo.get_user_name()

2. Implement XML document

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

3. Read XML document with help of implemented classes

    .. code-block:: python

      >>> from documents import Company
      >>> from composite.builders import LXMLDocumentBuilder
      >>> from lxml import etree
      >>> xml_document = etree.fromstring(open('company.xml', 'rb').read())
      >>> company = Company.parse(LXMLDocumentBuilder, xml_document)
      >>> company
      <Company: Alexander Pepyako>
      >>> company.ceo.get_user_name()
      'Alexander Pepyako'

4. Convert company to JSON

    .. code-block:: python

        >>> from composite.builders import PythonDocumentBuilder
        >>> import json
        >>> company_dict = company.build(PythonDocumentBuilder, company)
        >>> company_dict
        {'address': 'Third Vydrokushskaya street, 7 building',
         'ceo': {'_attributes': {'age': 23,
           'email': 'com@alexander.pepyako',
           'first_name': 'Alexander',
           'gender': 'male',
           'last_name': 'Pepyako',
           'phone': '+79110010203'},
          'id': 1,
          'sign': 'Pepyako inc.'},
         'company_type': 'GHMb',
         'title': 'Pepyako industries'}
        >>> json.dumps(company_dict)
        '{"ceo": {"_attributes": {"phone": "+79110010203", "first_name": "Alexander", "last_name": "Pepyako",
        "gender": "male", "age": 23, "email": "com@alexander.pepyako"}, "id": 1,
        "sign": "Pepyako inc."}, "title": "Pepyako industries",
        "company_type": "GHMb", "address": "Third Vydrokushskaya street, 7 building"}'
