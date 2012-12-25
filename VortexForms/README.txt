VortexForms: simple template engine to generate HTML input blocks. Inspired by Jinja2.

Before:
<form>
<p>Please enter your name: {{ first_name|text|width=100%|class=input_large green }}</p>
</form>

After:
<form>
<p>Please enter your name: <input id="first_name" type="text" width="100%" class="input_large green"></p>
</form>

As simple as that.

Current usage algorithm should be changed, but anyway:
>>> return VortexProcessor(code="<form>\n<p>Please enter your name: {{ first_name|text|width=100%|class=input_large green }}</p>\n</form>").rendered_html

TODO:
- Better readme file :D
- Improve usage as library
- Unit & functional testing
- Read dict and replace input with entered by user values