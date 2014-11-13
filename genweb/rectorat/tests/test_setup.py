# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from genweb.rectorat.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of genweb.rectorat into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb.rectorat is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('genweb.rectorat'))

    def test_uninstall(self):
        """Test if genweb.rectorat is cleanly uninstalled."""
        self.installer.uninstallProducts(['genweb.rectorat'])
        self.assertFalse(self.installer.isProductInstalled('genweb.rectorat'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IGenwebRectoratLayer is registered."""
        from genweb.rectorat.interfaces import IGenwebRectoratLayer
        from plone.browserlayer import utils
        self.failUnless(IGenwebRectoratLayer in utils.registered_layers())
