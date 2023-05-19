import re
import inspect

def get_members(class_name):
    all_method_list = dir(class_name)
    desired_method_list = []
    for method in all_method_list:
        add_to_list = True
        
        try:
            exec_method = getattr(class_name, method)
            exec_method()
        except Exception as e:
            add_to_list = False

        if not method.startswith('_') and check_method(method) is not False:
            desired_method_list.append(method)

    return desired_method_list


def convert_to_camel(name):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)

def convert_to_sentence(camel):
    if camel != '':
        result = re.sub('([A-Z])', r' \1', camel)
        return result[:1].upper() + result[1:].lower()


def check_method(method):
    keep_method = True

    undesired_list = [
        'add_provider',
        'zip',
        'dsv',
        'seed',
        'hexify',
        'bothify',
        'csv',
        'binary',
        'bytes',
        'lexify',
        'numerify',
        'random_choices',
        'random_element',
        'random_elements',
        'random_int',
        'random_letters',
        'random_numbers',
        'random_sample',
        'randomize_nb_elements',
        'date_between',
        'date_between_dates',
        'date_time_between',
        'date_time_between_dates',
        'iso8601',
        'pytimezone',
        'time_delta',
        'time_object',
        'time_series',
        'emoji',
        'image_url',
        'fixed_width',
        'image',
        'json',
        'json_bytes',
        'psv',
        'tar',
        'tsv',
        'profile',
        'simple_profile',
        'enum',
        'pybool',
        'pydecimal',
        'pydict',
        'pyfloat',
        'pyint',
        'pyiterable',
        'pylist',
        'pyobject',
        'pyset',
        'pystr',
        'pystr_format',
        'pystruct',
        'pytuple',
        'parse',
        'random',
        'seed_instance',
        'seed_locale',
        'weights',
        'cache_pattern']

    for ul in undesired_list:
        if ul == method:
            keep_method = False
            break

    return keep_method



                    