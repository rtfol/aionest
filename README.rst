=======
aionest
=======


.. image:: https://img.shields.io/pypi/v/aionest.svg
        :target: https://pypi.python.org/pypi/aionest

.. image:: https://img.shields.io/travis/rtfol/aionest.svg
        :target: https://travis-ci.org/rtfol/aionest

.. image:: https://readthedocs.org/projects/aionest/badge/?version=latest
        :target: https://aionest.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/rtfol/aionest/shield.svg
     :target: https://pyup.io/repos/github/rtfol/aionest/
     :alt: Updates



Asynchronous python library for Nest API


* Free software: Apache Software License 2.0
* Documentation: https://aionest.readthedocs.io.


Features
--------

* Minimium requirement is Python 3.5.3
* Full support of aysncio
* Use `Nest Stream API <https://developers.nest.com/documentation/cloud/rest-streaming-guide>`_


Installation
============

.. code-block:: bash

    pip install aionest


Nest Developer Account
=======================

You will need a Nest developer account, and a Product on the Nest developer portal to use this library:

1. Visit `Nest Developers <https://developers.nest.com/>`_, and sign in. Create an account if you don't have one already.

2. Fill in the account details:

  - The "Company Information" can be anything.

3. Submit changes.

4. Click "`Products <https://developers.nest.com/products>`_" at top of page.

5. Click "`Create New Product <https://developers.nest.com/products/new>`_"

6. Fill in details:

  - Product name must be unique.

  - The description, users, urls can all be anything you want.

7. For permissions, check every box and if it's an option select the read/write option.

  - The description requires a specific format, recommend use following format

  .. code-block::

      [Your product name] [Edit] [For Home Automation]

8. Click "Create Product".

9. Once the new product page opens the "Product ID" and "Product Secret" are located on the right side. These will be used as product_id and product_secret below.


Usage
=====

.. code-block:: python

    import aionest
    import asyncio
    
    async def nest_update():
        nest_api = aionest.NestApi(product_id=product_id)
        print('Go to {} to authorize, then enter PIN below'.format(nest_api.get_authorize_url()))
        pin = input("PIN: ")
        access_token, expires_in = await nest_api.authenticate(pin, product_secret)

        # you can cache access_token future reuse
        nest_api = aionest.NestApi(access_token=access_token)
        async for event in nest_api:
            print(event.data)

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(nest_update())
    finally:
        event_loop.close()
        
Credits
-------

This project was inspired by python-nest_.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _python-nest: https://github.com/jkoelker/python-nest
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
