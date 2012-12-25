VortexForms: simple template engine to generate HTML input blocks.

Before:
<form>
<p>Please enter your name: {{ first_name|text|width=100%|class=input_large green }}</p>
</form>

After:
<form>
<p>Please enter your name: <input id="first_name" type="text" width="100%" class="input_large green"></p>
</form>

As simple as that.

TODO:
- Better readme file :D
- Read dict and replace input with entered by user values