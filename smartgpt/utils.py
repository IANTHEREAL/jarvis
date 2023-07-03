# Description: Utility functions

from smartgpt import jvm


def wrap_string_to_eval(text):
    return jvm.LAZY_EVAL_PREFIX + text + ")"

def strip_yaml(text):
    # remove the last "```" if it exists
    if text.endswith("```"):
        return text[:-3]
    return text

def sys_eval(text):
    return eval(text)

def str_to_bool(s):
    if isinstance(s, bool):
        return s
    elif isinstance(s, str):
        return s.lower() == 'true'
    else:
        return False