from cepcenv.shell import Shell

class Csh(Shell):
    def set_env(self, env_name, env_value):
        return 'setenv {0} "{1}"\n'.format(env_name, env_value)

    def source(self, script_path):
        return 'source {0}\n'.format(script_path)

    def define_cepcenv(self):
        raise Exception('cepcenv() not implemented')
