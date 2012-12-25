from Core.AdditionalFunctions import build_additional_params
from Core.AdditionalFunctions import check_id_syntax
from Core.Exceptions import ParsingTemplateError

from functools import reduce

# Template engine control symbols. A place for limited customization

TAG_OPEN_SIGN = '{'
TAG_CLOSE_SIGN = '}'
SPLIT_CHAR = '|'
TAG_OPEN = TAG_OPEN_SIGN * 2
TAG_CLOSE = TAG_CLOSE_SIGN * 2

SERVICE_TAGS = [TAG_OPEN, TAG_CLOSE]
SERVICE_SIGNS = [TAG_OPEN_SIGN, TAG_CLOSE_SIGN]

# Standard HTML input types for forms
INPUT_TYPES = ['date', 'datetime', 'datetime-local', 'email',
             'month', 'number', 'password', 'range', 'search',
             'tel', 'text', 'time', 'url', 'week']


class Form(object):
    """
    Object which represents input form object with it's params and html code.
    """
    def __init__(self, id, type, additional_params):
        self._id = id
        self._type = type
        self._params = additional_params
        
    def __str__(self):
        params = ' '.join([key + '="' + value + '"' for (key, value) in self._params.items()])
        return '<input id="{id}" type="{type}" {params}>'.format(id=self._id, type=self._type, params=params)

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def html(self):
        return self.__str__


class Template(object):

    def __init__(self, forms, html_code, template_code):
        self._forms = forms
        self._html_code = html_code
        self._template_code = template_code

    def __str__(self):
        return self._html_code

    @property
    def template_code(self):
        return self._template_code

    @property
    def forms(self):
        return self._forms

    @property
    def html(self):
        return self._html_code


class TemplateProcessor(object):
    """
    Template processor. Searches for specially formatted tags, like {{ form|text }},
    adding them into list of forms, forming Form class as an answer.

    """
    def __new__(cls, template_code, values=None):
        cls.stream = iter(template_code)
        cls.rendered_html = []
        cls.forms = []
        cls._signs = ''
        cls._buffer = ''
        # Appending text, not input forms       
        cls._mode = bool(values) # True -> means we're appending values, not forms
        cls._values = values
        # Flags block for parsing
        cls._inside_flag = False
        # Run processor
        any(map(lambda x: cls.string_processor(x), cls.stream))
        return Template(forms = cls.forms,
                        html_code = "".join(cls.rendered_html),
                        template_code = template_code)

    @classmethod
    def set_inside_flag(cls):
        if not cls._inside_flag:
            # We are opening our special tag
            if cls._signs != TAG_OPEN:
                raise ParsingTemplateError
            cls._inside_flag = True
        else:
            # Closing our special tag and processing tag's content
            if cls._signs != TAG_CLOSE:
                raise ParsingTemplateError
            # Closing tag
            cls.process_form()
            cls._inside_flag = False


        cls._buffer = ''
        cls._signs = ''

    @classmethod
    def string_processor(cls, letter):
        if cls._inside_flag:
            if letter in SERVICE_SIGNS:
                if letter == TAG_OPEN_SIGN:
                    raise ValueError
                cls._signs += letter
                if cls._signs == TAG_CLOSE:
                    cls.set_inside_flag()
            else:
                cls._buffer += letter
        else:
            if letter in SERVICE_SIGNS:
                cls._signs += letter
                if len(cls._signs) > 1:
                    if cls._signs not in SERVICE_TAGS:
                        # Handling case when special signs used in context: like {USUAL_TEXT}, not like our {{ TAG }}
                        cls.rendered_html += cls._signs
                        cls._signs = ''
                    else:
                        # looks like it is our tag
                        cls.set_inside_flag()

            else:
                cls.rendered_html += letter
                cls._signs = ''

    @classmethod            
    def process_form(cls):
        """
        If we have got form, we should process it. 
            Proper form example:
            {string_id}|{type:text,number}
            Other params are optional and can be applied in any order:
            {string_id}|{type:text,number}|class="test test"|width="x{px,%}"|height="y{px,%}"|value="text"
        """
        try:
            form = cls._buffer.strip()
            form = form.split(SPLIT_CHAR)
        except AttributeError:
            raise
        if 7 > len(form) < 2:
            raise ParsingTemplateError('Too few arguments, ID or input type not specified')
        # Removing spaces in form
        any(map(str.strip, form))
        # Appending into variables: 
        id = None
        type = None
        additional_params = {}
        params_text = ''

        if check_id_syntax(form[0]):
            id = form.pop(0)
        else:
            raise ParsingTemplateError("Wrong input ID specified. It must be a string with no special signs")

        if not id:
            raise ParsingTemplateError("Wrong input ID")

        if cls._mode == False:
            # Dealing with new form (not appending values)
            if form[0] in INPUT_TYPES:
                type = form.pop(0)
            else:
                raise ParsingTemplateError("Wrong input type specified. It must be one of these: %s" % ",".join(INPUT_TYPES))

            if not type:
                raise ParsingTemplateError("Wrong input type")

            # Checking if we have any additional parameters
            if form:
                # Wicked functional construction:
                # We are splitting additional params by '=' in parse_additional_params function
                # and then packing them into dict. lambda function with reduce merge this dicts.
                additional_params = reduce(lambda x, y: dict(x.items() + y.items()), map(build_additional_params, form))
            new_form = Form(id=id, type=type, additional_params=additional_params)
            #import pdb; pdb.set_trace()
            cls.forms.append(str(new_form))
            cls.rendered_html += str(new_form)

        elif cls._mode == True:
            # Dealing with values
            try:
                value = cls._values.get(id)
            except AttributeError:
                raise ParsingValuesError('Bad values provided, please provide dictionary with form values')
            if not value:
                value = ''
            cls.rendered_html += str(value)
