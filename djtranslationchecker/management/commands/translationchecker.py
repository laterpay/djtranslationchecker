from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app_paths

import fnmatch
import importlib
import subprocess
import os

class Command(BaseCommand):
    help = "Checks your message files for missing or fuzzy translations"

    def handle(self, *args, **kwargs):
        errors = []

        for po_filepath in get_po_filepaths():
            self.stdout.write("Checking %s" % po_filepath)

            out = check_po_for_fuzzy_translations(po_filepath)
            if out:
                errors.append("Fuzzy translation(s) found in %s" % po_filepath)
            out = check_po_for_untranslated(po_filepath)
            if out:
                errors.append("Untranslated message(s) found in %s" % po_filepath)

        if errors:
            raise CommandError('\n' + '\n'.join(errors)) # This is the best way I've found of setting management command exit code to nonzero


def check_po_for_fuzzy_translations(po_filepath):
    return check_po(["msgattrib", "--only-fuzzy"], po_filepath)


def check_po_for_untranslated(po_filepath):
    return check_po(["msgattrib", "--untranslated"], po_filepath)


def check_po(command, po_filepath):
    """
    :: [String] -> FilePath -> Maybe String

    Until I do some funky parsing, treat this as returning Maybe OpaqueErrorType
    """

    p = subprocess.Popen(command + [po_filepath], stdout=subprocess.PIPE)
    p.wait()

    output = p.stdout.read()
    p.stdout.close()

    if len(output):
        return output
    else:
        return None


def get_po_filepaths():
    apps = getattr(settings, 'PROJECT_APPS', settings.INSTALLED_APPS)

    pos = []
    for app_name in apps:
        path = os.path.dirname(importlib.import_module(app_name).__file__)

        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.po'):
                pos.append(os.path.join(root, filename))

    return pos
