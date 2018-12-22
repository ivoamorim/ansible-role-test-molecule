import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('distro, pkg', [
    ('centos', 'httpd'),
    ('debian', 'apache2'),
])
def test_packages_are_installed(host, distro, pkg):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    package = host.package(pkg)
    assert package.is_installed


@pytest.mark.parametrize('distro, svc', [
    ('centos', 'httpd'),
    ('debian,ubuntu', 'apache2'),
])
def test_svc(host, distro, svc):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    service = host.service(svc)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('file, content', [
    ("/var/www/html/index.html", "Managed by Ansible")
])
def test_files(host, file, content):
    file = host.file(file)
    assert file.exists
    assert file.contains(content)


def test_httpd_is_listened(host):
    socket_v4 = host.socket('tcp://0.0.0.0:80')
    assert socket_v4.is_listening
