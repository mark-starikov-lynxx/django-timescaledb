import logging
from . import base_impl
from django.db import ProgrammingError
from .schema import TimescaleSchemaEditor


logger = logging.getLogger(__name__)


class DatabaseWrapper(base_impl.backend()):
    SchemaEditorClass = TimescaleSchemaEditor

    def prepare_database(self):
        """
        Prepare the configured database.
        This is where we enable the `timescaledb` extension if it isn't enabled yet.
        """
        super().prepare_database()
        with self.cursor() as cursor:
            try:
                cursor.execute('CREATE EXTENSION IF NOT EXISTS timescaledb')
            except ProgrammingError:  # permission denied
                logger.warning(
                    msg='''
                    Failed to create "timescaledb" extension. 
                    Usage of timescale capabilities might fail
                    If timescale is needed, make sure you are connected 
                    to the database as a superuser 
                    or add the extension manually.
                    ''',
                    exc_info=True
                )
