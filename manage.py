from click import option

from jokes_api.cli import cli


@cli.command(with_appcontext=False)
@option('-d', '--dir', default='tests', help='Directory with tests')
def test(dir):
    """Discover and run unit tests."""
    from unittest import TestLoader, TextTestRunner
    testsuite = TestLoader().discover(f'./{dir}')
    TextTestRunner(verbosity=2, buffer=True).run(testsuite)


@cli.command(with_appcontext=False)
@option('-o', '--output', default='html', help='Output dir for docs')
def docs(output):
    """Build documentation with Sphinx"""
    from sphinx.cmd import build
    build.main(['docs', output])


if __name__ == '__main__':
    cli()
