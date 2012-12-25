
VortexForms
==================

Simple template engine to convert HTML templates with service tags into HTML with input forms.

Implemented with Jinja2 in mind :)

Create forms from templates
--------------

Write template like this one:


.. code::

  <p>Your name: {{ first_name|text|class=myclass }}</p>


Implementation:

.. code::

	>>> VortexProcessor(code="<p>Your name: {{ first_name|text|class=myclass }}</p>").render()


Result:

.. code::

  <p>Your name: <input id="first_name" type="text" class="myclass"></p>

Replace forms with user input
--------------

Use template as usual:

.. code::

  <p>Your name: {{ first_name|text|class=myclass }}</p>


Pass dictionary with values to processor:

.. code::

	>>> values = {'first_name':'Vortex'}
	>>> VortexProcessor(code="<p>Your name: {{ first_name|text|class=myclass }}</p>").render(values)


Result:

.. code::

  <p>Your name: Vortex</p>


TODO
--------------
1) Convert into module
2) Add functional and unit testings
3) Add more comments
