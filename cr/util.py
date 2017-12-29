"""
Utilities
"""
import re


def camelcase_split(s):
    """Split camel case into list of strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)

def camelcase_to_snakecase(s):
    """Convert camelcase to snakecawse"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
