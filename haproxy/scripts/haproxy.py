
from cloudify import ctx, utils, exceptions
from cloudify.state import ctx_parameters as inputs


CONFIG_PATH = '/etc/haproxy/haproxy.cfg'
NEW_CONFIG_FILE = 'resources/haproxy.cfg'


def configure():
    ctx.logger.info('Configuring HAProxy.')
    haproxy_config = ctx.download_resource(NEW_CONFIG_FILE)
    _run('sudo mv {0} {1}'.format(haproxy_config, CONFIG_PATH),
         error_message='Failed to write to {0}.'.format(CONFIG_PATH))
    _run('sudo /usr/sbin/haproxy -f {0} -c'.format(CONFIG_PATH),
         error_message='Failed to Configure')


def _run(command, error_message):
    runner = utils.LocalCommandRunner(logger=ctx.logger)
    try:
        runner.run(command)
    except exceptions.CommandExecutionException as e:
        raise exceptions.NonRecoverableError('{0}: {1}'.format(
                error_message, e))


def _main():
    invocation = inputs['invocation']
    function = invocation['function']
    args = invocation.get('args', [])
    kwargs = invocation.get('kwargs', {})
    globals()[function](*args, **kwargs)


if __name__ == '__main__':
    _main()
