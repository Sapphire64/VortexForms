from Core.Templates import TemplateProcessor
from Core.Exceptions import ExcessiveAttributesError, EmptyTemplateError


class VortexProcessor(object):

    def __init__(self, code=None, file_path=None):
        if not code and not file_path:
            raise EmptyTemplateError()
        if code and file_path:
            raise ExcessiveAttributesError()

        if code:
            self._template = code
        elif file_path:
            try:
                with open(file_path, 'r') as f:
                    self._template = f.read()
            except SystemError as e:
                raise

    def render(self, values=None):
        self._render_template(values)
        return self.rendered_template

    def _render_template(self, values):
        self._rendered_template = TemplateProcessor(self.template, values)

    def __hash_it(self):
        return sha.new(self.template).hexdigest()

    @property
    def hash(self):
        return self._hashed

    @property
    def template(self):
        return self._template

    @property
    def html(self):
        return self._rendered_template

    @property
    def rendered_template(self):
        return str(self._rendered_template)

if __name__ == '__main__':
    tmp = VortexProcessor(code="<form>\n<p>Your name: {{ first_name|text|width=100%|class=input_large green trololo }}</p>\n</form>")
    print ("Our code:")
    print (tmp.template)
    print ('\nRendered template:')
    print (tmp.render())
    print ('\nNow with value:')
    print (tmp.render({'first_name': 'Vortex'}))
