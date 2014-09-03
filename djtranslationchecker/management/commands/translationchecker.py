from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app_paths

import subprocess

class Command(BaseCommand):
    help = "Checks your message files for missing or fuzzy translations"

    def handle(self, *args, **kwargs):
        errors = []

        for po_filepath in get_po_filepaths():
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
    """
    In the absence of a nice Django cross-version "give me all the apps" to iterate through, I apologise...

    This is grim.
    """

    import subprocess

    pos = subprocess.check_output("find * -name django.po", shell=True) # * not . to avoid .git etc., with optimistic and awful shell expansion :(

    return pos.strip().split('\n')
