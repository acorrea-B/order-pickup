import vcr as orig_vcr
import sys

from os import path
from django.conf import settings

def vcr_fpg(function):
    """
        Provides a path for vcr cassettes
        associated to the recived function
    """

    base_dir = settings.BASE_DIR
    mod_str = str(sys.modules[function.__self__.__class__.__module__].__file__).replace(".py", "")
    submods = mod_str.split('/')
    path_comps = (
        [
            base_dir, submods[2],
             'vcr_cassettes'
        ]+ submods[3:] +
        [
            function.__self__.__class__.__name__,
            '{0}.vcr'.format(function.__name__)
        ]   
    )
    target_path =path.join(*path_comps)

    return target_path

vcr = orig_vcr.VCR(func_path_generator=vcr_fpg)

    