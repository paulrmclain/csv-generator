import re

def get_members(class_name):
    all_method_list = dir(class_name)
    desired_method_list = []
    for method in all_method_list:
        if not method.startswith('_') \
           and method != 'add_provider' \
           and method != 'zip' \
           and method != 'dsv' \
           and 'seed' not in method \
           and 'hexify' not in method \
           and 'bothify' not in method \
           and 'csv' not in method  \
           and 'binary' not in method \
           and 'bytes' not in method:
            desired_method_list.append(method)

    return desired_method_list


def convert_to_camel(name):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)

def convert_to_sentence(camel):
    if camel != '':
        result = re.sub('([A-Z])', r' \1', camel)
        return result[:1].upper() + result[1:].lower()