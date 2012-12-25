from Core.Templates import TemplateProcessor
from Core.Exceptions import ExcessiveAttributesError, EmptyTemplateError

import sha


class VortexProcessor(object):

    def __init__(self, code=None, file_path=None, hash_digest=None, hash_map=None):
        if not hash_digest:
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
            hash_digest = self.__hash_it()

        if hash_map:   
            template = hash_map.get(hash_digest)
            # This place should be checked carefully, something wrong
            if not template:
                self._rendered_template = self._render_template()
            else:
                self._rendered_template = template.html
                self._template = template.template_code
            self._hashed = {hash_digest : self._rendered_template}
        else:
            self._rendered_template = self._render_template()
            self._hashed = {hash_digest : self._rendered_template}

    def _render_template(self):
        return TemplateProcessor(self.template)
        
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
        return self._rendered_template

if __name__ == '__main__':
    tmp = VortexProcessor(code="<form>\n<p>Please enter your name: {{ first_name|text|width=100%|class=input_large green }}</p>\n</form>")
    print (str(tmp.template))
    print ('')
    print (str(tmp.rendered_template))