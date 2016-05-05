import unittest

from mock import MagicMock
from mock import patch

import pet.watch
import pet.perlre
import pet.exceptions


class TestPetWatch(unittest.TestCase):

    def setUp(self):
        self.watchRule = pet.watch.WatchRule()
        self.watcher = pet.watch.Watcher()
        self.cpan = pet.watch.CPAN()

    def test_timeout(self):
        self.assertEquals(180, pet.watch.TIMEOUT())

    def test_cpan_init(self):
        self.assertEqual('ftp://ftp.cs.uu.nl/pub/CPAN/', self.cpan.mirror)
        self.assertIsNone(self.cpan._dists)
        self.assertIsNone(self.cpan._files)

    def test_cpan_dists_when_not_none(self):
        value = 'distscpantest1'
        self.cpan._dists = value
        self.assertEqual(value, self.cpan.dists)

    def test_cpan_dists_when_is_none(self):
        entry1 = ["CGI::Header", "0.63", "A/AN/ANAZAWA/CGI-Header-0.63.tar.gz"]
        entry2 = ["Severo::Daniel", "7.63",
                  "Z/ZZ/ZZOITDBEM/Severo-Daniel-7.63.tar.gz"]
        entry3 = ["Alienware::Satellite", "5.41",
                  "D/DY/DYLAN/Alienware-Satellite-5.41.tar.gz"]
        entry4 = ["a::b", "0.23", "A/AB/ABC/a-b-0.23.tar.gz"]
        entry5 = ["c::d", "0.32", "B/BC/BCD/c-d-0.32.tar.gz"]
        space = "   "

        contents_mock = [
            # Valid entries, will appear on result.
            entry1[0] + space + entry1[1] + space + entry1[2],
            entry2[0] + space + entry2[1] + space + entry2[2],
            entry3[0] + space + entry3[1] + space + entry3[2],
            # Invalid entries, will not appear on result.
            entry4[0] + space + entry4[1] + entry4[2],
            entry5[0] + entry5[1] + space + entry5[2]
        ]

        # Mocking _get_and_uncompress and the close method from the object
        # it returns. Also, that object must be iterable. We do that with
        # the list we constructed (contents_mock).
        mock = MagicMock()
        mock.__iter__.return_value = contents_mock
        mock.close = MagicMock()
        self.cpan._get_and_uncompress = MagicMock(return_value=mock)

        expected = [entry1[2], entry2[2], entry3[2]]
        actual = self.cpan.dists
        self.assertEqual(expected, actual)

    def test_cpan_files_when_not_none(self):
        value = 'filescpantest1'
        self.cpan._files = value
        self.assertEqual(value, self.cpan.files)

    def test_watchrule_mangle(self):
        value = "05052016"
        pet.perlre.apply_perlre = MagicMock(return_value=value)
        self.assertEqual(value, self.watchRule._mangle(["1", "2"], "str"))

    def test_watchrule_uversionmangle_if_none(self):
        param = "str"
        self.watchRule.options = MagicMock()
        self.watchRule.options.get = MagicMock(return_value=None)
        self.assertEqual(param, self.watchRule.uversionmangle(param))

    def test_watchrule_uversionmangle_if_not_none(self):
        param = "str"
        value = "str2"
        self.watchRule.options = MagicMock()
        self.watchRule.options.get = MagicMock(return_value="string")
        self.watchRule._mangle = MagicMock(return_value=value)
        self.assertNotEqual(param, value)
        self.assertEqual(value, self.watchRule.uversionmangle(param))

    def test_watchrule_dversionmangle_if_none(self):
        param = "str"
        value = "str_rand"
        self._re_upstream_version = MagicMock()
        self._re_upstream_version.sub = MagicMock(return_value=value)
        self.watchRule.options = MagicMock()
        self.watchRule.options.get = MagicMock(return_value=None)
        self.assertEqual(param, self.watchRule.dversionmangle(param))

    def test_watchrule_dversionmangle_if_not_none(self):
        param = "str"
        value = "str2"
        value1 = "str3"
        self._re_upstream_version = MagicMock()
        self._re_upstream_version.sub = MagicMock(return_value=value1)
        self.watchRule.options = MagicMock()
        self.watchRule.options.get = MagicMock(return_value="string")
        self.watchRule._mangle = MagicMock(return_value=value)
        self.assertNotEqual(param, value)
        self.assertEqual(value, self.watchRule.dversionmangle(param))

    def test_watcher_init(self):
        self.assertIsNotNone(self.watcher._cpan);

    def test_urlopen_with_context(self):
        import ssl
        import urllib2
        ssl._create_unverified_context = MagicMock()
        urllib2.urlopen = MagicMock()
        pet.watch.urlopen([], context="value")
        self.assertFalse(ssl._create_unverified_context.called)

    def test_urlopen_without_context(self):
        import ssl
        import urllib2
        ssl._create_unverified_context = MagicMock()
        urllib2.urlopen = MagicMock()
        pet.watch.urlopen([], other="value")
        self.assertTrue(ssl._create_unverified_context.called)

    # def test_watchrule_parse_on_perlre_compile_error(self):
    #     import re
    #     rule = 'testrule1'
    #     pet.perlre.compile = MagicMock(side_effect=Exception())
    #     with self.assertRaises(pet.exceptions.InvalidWatchFile) as cm:
    #         self.watchRule.parse(rule)
    #     self.assertEquals("Could not parse regular expression '{0}': {1}.".format("ueioeioueiuo", "ueiuoeuoi"),
    #                       cm.exception.message)

    # def test_watchrule_parse_on_re_search_error(self):
    #     import re
    #     rule = 'testrule2'
    #     pet.watch._re_paren.search = MagicMock(side_effect=Exception())
    #     with self.assertRaises(pet.exceptions.InvalidWatchFile) as cm:
    #         self.watchRule.parse(rule)
    #     self.assertEquals("Rule '{0}' is invalid.".format(rule),
    #                       cm.exception.message)
