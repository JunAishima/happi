import re
import pytest
import logging

from happi        import Device
from happi.errors import ContainerError, EntryError
from happi.device import EntryInfo

logger = logging.getLogger(__name__)


def test_get(device, device_info):
    assert device.alias == device_info['alias']

def test_init(device, device_info):
    assert device.base     == device_info['base']
    assert device.alias    == device_info['alias']
    assert device.z        == device_info['z']
    assert device.beamline == device_info['beamline']


def test_list_enforce():
    class MyDevice(Device):
        list_attr = EntryInfo(enforce=['a','b','c'])

    d = MyDevice()
    d.list_attr = 'b'

def test_list_enforce_failure():
    class MyDevice(Device):
        list_attr = EntryInfo(enforce=['a','b','c'])

    d = MyDevice()
    with pytest.raises(ValueError):
        d.list_attr = 'd'

def test_regex_enforce():
    class MyDevice(Device):
        re_attr = EntryInfo(enforce=re.compile(r'[A-Z]{2}$'))

    d = MyDevice()
    d.re_attr = 'AB'

def test_regex_enforce_failure():
    class MyDevice(Device):
        re_attr = EntryInfo(enforce=re.compile(r'[A-Z]{2}$'))

    d = MyDevice()
    with pytest.raises(ValueError):
        d.re_attr = 'ABC'

def test_set(device):
    device.alias = 'new_alias'
    assert device.alias == 'new_alias'

def test_optional(device):
    assert device.parent == None

def test_enforce(device):
    with pytest.raises(ValueError):
        device.z = 'Non-Float'

def test_container_error():
    with pytest.raises(ContainerError):
        class MyDevice(Device):
            fault = EntryInfo(enforce=int, default='not-int')

def test_mandatory_info(device):
    for info in ('base','alias','beamline'):
        assert info in device.mandatory_info

def test_restricted_attr():
    with pytest.raises(TypeError):
        class MyDevice(Device):
            info_names = EntryInfo()


def test_post(device, device_info):
    post = device.post()
    assert post['base']     == device_info['base']
    assert post['alias']    == device_info['alias']
    assert post['z']        == device_info['z']
    assert post['beamline'] == device_info['beamline']

