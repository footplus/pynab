import pytest

from nabd.tests.mock import NabdMockTestCase
from nabd.tests.utils import close_old_async_connections
from nabguinead.nabguinead import NabGuinead


@pytest.mark.django_db
class TestNabguinead(NabdMockTestCase):
    def tearDown(self):
        NabdMockTestCase.tearDown(self)
        close_old_async_connections()

    def test_connect(self):
        self.do_test_connect(NabGuinead)
