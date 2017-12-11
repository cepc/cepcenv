import click

try:
    input = raw_input
except NameError:
    pass

from cepcenv.config.config_release import ConfigReleaseTransformError
from cepcenv.install import Install as CepcenvInstall

from cepcenv.logger import get_logger
_logger = get_logger()

def _output_preview_lines(pkg_list):
    pkg_max = 0
    version_max = 0

    for pkg_single in pkg_list:
        pkg_len = len(pkg_single[0])
        if pkg_len > pkg_max:
            pkg_max = pkg_len

        ver_len = len(pkg_single[1])
        if ver_len > version_max:
            version_max = ver_len

    for pkg_single in pkg_list:
        click.echo('{0:{pmax}} {1:{vmax}} : {2}'.format(*pkg_single, pmax=pkg_max, vmax=version_max))

class Install(object):
    def execute(self, config, config_version, source, force, yes):
        transformer = []
        if source:
            transformer = [source + '_source']

        install = CepcenvInstall(config, config_version, transformer)

        if not force:
            missing_pkg, install_cmd, pkg_install_name = install.check()
            if missing_pkg:
                click.echo('Missing package(s): {0}'.format(', '.join(missing_pkg)))
                click.echo('Suggest installing with the following command:')
                click.echo(' '.join(install_cmd+pkg_install_name))
                click.echo('If you would like to skip installing these packages and are confirmed they are available, try to use "cepcenv install --force"')
                return


        click.echo('CEPCEnv is going to install the following packages:')
        click.echo('')

        _output_preview_lines(install.package_list())

        click.echo('')
        click.echo('Version: {0}'.format(config_version.get('version')))
        click.echo('Software root: {0}'.format(config_version.get('software_root')))
        click.echo('')


        if not yes and not click.confirm('Proceed with installation?', default=True):
            return


        try:
            install.install_packages()
        except ConfigReleaseTransformError as e:
            _logger.critical('Install source error: {0}'.format(source))
            raise

        click.echo('Installation finished successfully')
        click.echo('Version: {0}'.format(config_version.get('version')))
        click.echo('Software root: {0}'.format(config_version.get('software_root')))
