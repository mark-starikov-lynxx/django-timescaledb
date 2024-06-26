from migrations.test_base import OperationTestBase


class TimescaleDBMigrationTest(OperationTestBase):
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to     properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class ModelTest(TestCase):
    def _run_command(self, *args):
        from django.core.management import execute_from_command_line
        argv = ['manage.py'] + list(args)
        execute_from_command_line(argv)

    def create_hypertable(self):
        pass

    def create_aggregation(self):
        pass

    def create_retention(self):
        pass

    def create_compression(self):
        pass
