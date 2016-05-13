import os

from charms.reactive import when, when_not, set_state, hook
from charmhelpers import fetch
from charmhelpers.core.templating import render
from charmhelpers.core import hookenv, host

SERVICE = 'freeciv-server'

@when_not('freeciv-server.installed')
def install_freeciv_server():
    fetch.apt_update(fatal=True)
    fetch.apt_install(['freeciv-server'])
    set_state('freeciv-server.installed')

@hook('config-changed')
def config_changed():
    restart = host.service_running(SERVICE)
    if restart:
        stop()
    if not os.path.exists('/etc/systemd/system'):
        os.makedirs('/etc/systemd/system')
    render(
        source = "freeciv-server.service",
        target = "/etc/systemd/system/freeciv-server.service",
        owner = "root",
        perms = 0o644,
        context = {'config': hookenv.config()}
    )
    if restart:
        start()

@hook('start')
def start():
    host.service_start(SERVICE)
    hookenv.open_port(hookenv.config()['port'])
    hookenv.status_set('active', 'started')

@hook('stop')
def stop():
    host.service_stop(SERVICE)
    hookenv.close_port(hookenv.config()['port'])
    hookenv.status_set('active', 'Stopped')
