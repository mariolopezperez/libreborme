# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from borme.models import Config

import time
from datetime import datetime
from libreborme.utils import get_git_revision_short_hash
from borme.utils import import_borme_download


class Command(BaseCommand):
    args = '<ISO formmated date (ex. 2015-01-01)>'
    help = 'Import BORMEs from date'

    def handle(self, *args, **options):
        start_time = time.time()

        if args:
            date = (args[0], args[1], args[2])
            import_borme_download((date))

            config = Config.objects.first()
            if config:
                config.last_modified = datetime.today()
            else:
                config = Config(last_modified=datetime.today())
            config.version = get_git_revision_short_hash()
            config.save()

            # Elapsed time
            elapsed_time = time.time() - start_time
            print('\nElapsed time: %.2f seconds' % elapsed_time)
