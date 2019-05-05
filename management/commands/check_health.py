import requests
from django.core.management.base import BaseCommand, CommandError
from requests import RequestException


class Command(BaseCommand):
    """
    This command checks the health of the running Django microservice
    """

    help = 'Checks the health of the running Django microservice'

    def add_arguments(self, parser):
        """
        Configure the parser to accept the CLI arguments
        :param parser: the parser to configure
        """

        parser.add_argument(
            'ports',
            metavar='ports',
            type=int,
            nargs='+',
            help='list of TCP ports to run health checks on'
        )

    def handle(self, *args, **options):
        """
        Run the health checks against the supplied ports
        :param args: arguments
        :param options: CLI options parsed via argparse
        """

        ports = options.get('ports')

        for port in ports:
            self.stdout.write(f'Testing port {port}... ', ending='')

            try:
                response = requests.post(
                    f'http://localhost:{port}/hello/',
                    json={
                        'recipient': 'Monty Python',
                    }
                )
                response = response.json()
                message = response.get('message', None)

                if message is not None and message == 'Hello Monty Python!':
                    self.stdout.write(self.style.SUCCESS('pass'))
                else:
                    raise RequestException()
            except RequestException:
                self.stdout.write(self.style.ERROR('fail'))
                raise CommandError('Server is unhealthy')

        self.stdout.write(self.style.SUCCESS('Server is healthy'))
