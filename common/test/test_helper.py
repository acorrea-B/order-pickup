import vcr as orig_vcr

from os import path
from django.conf import settings

def vcr_fpg(funtion):
    """
        Provides a path for vcr cassettes
        associated to the recived function
    """

    base_dir, _ = path.split(settings.BASE_DIR)
    mod_str = str(function.__self__.__class__.__module__)
    submods = mod_str.split('.')
    path_compse = (
        [
            base_dir, submods[0],
             'vcr_cassettes' + submods[2:]] +
        [
            funtion.__self__.__class__.__name__,
            '{}.vcr', format(funtion.__name__)
        ]   
    )
    return path.join(*path_compse)

vcr = orig_vcr.VCR(func_path_generator=vcr_fpg)

    