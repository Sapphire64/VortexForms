from vexceptions import EmptyTemplateError, ExcessiveAttributesError, ParsingTemplateError

import string

ALLOWED_ID_CHARACTERS = string.ascii_letters + string.digits + '_'

def check_id_syntax(string):
    return all(c in ALLOWED_ID_CHARACTERS for c in string)

def build_additional_params(param):
    try:
        param = param.split('=')
        if len(param) != 2 or not param[0].isalnum:
            raise ParsingTemplateError
    except (AttributeError, ParsingTemplateError):
        raise ParsingTemplateError('Wrong additional params for form')
    else:
        return {param[0].strip(): param[1].strip()}