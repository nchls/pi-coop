from decimal import Decimal
from unittest.mock import mock_open, patch

from django.test import TestCase

from pi.views import get_temperature, get_temperature_from_sysfs


class PiStatusViewTests(TestCase):
	def test_get_temperature_from_sysfs_reads_millidegrees(self):
		with patch('pi.views.os.path.exists', return_value=True), patch('builtins.open', mock_open(read_data='45000\n')):
			self.assertEqual(get_temperature_from_sysfs(), Decimal('45'))

	@patch('pi.views.get_temperature_from_sysfs', return_value=None)
	def test_get_temperature_raises_when_sysfs_source_is_unavailable(self, _mock_get_temperature_from_sysfs):
		with self.assertRaises(RuntimeError):
			get_temperature()
