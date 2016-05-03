import unittest
import pet.models
from sqlalchemy.exc import OperationalError
import os.path
from mock import MagicMock
import pet.vcs

class TestPetModels(unittest.TestCase):

    def setUp(self):
        self.isfile = os.path.isfile
        self.engine = pet.engine

    def tearDown(self):
        os.path.isfile = self.isfile
        pet.engine = self.engine

    def test_check_ssl_certificate_with_file(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_with_file_ex(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            engine = pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None",cm.exception.message)

    def test_check_ssl_certificate_no_file(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_no_file_ex(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            engine = pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None",cm.exception.message)

    def test_get_col_spec(self):
        debversion = pet.models.DebVersion()
        self.assertEqual("DEBVERSION", debversion.get_col_spec())

    def test_bind_processor(self):
        debversion = pet.models.DebVersion()
        process = debversion.bind_processor(None)
        value = 123
        self.assertEqual(process(value), value)

    def test_result_processor(self):
        debversion = pet.models.DebVersion()
        process = debversion.result_processor(None, None)
        value = 123
        self.assertEqual(process(value), value)

    def test_vcs_if_vcs_exists(self):
        repository = pet.models.Repository()
        value = 123
        repository._vcs = value
        self.assertEqual(repository.vcs, value)

    def test_vcs_not_in_dict(self):
        repository = pet.models.Repository()
        value = 'git'
        pet.vcs.vcs_backend = MagicMock(return_value=value)
        self.assertEqual(repository.vcs, value)

    def test_named_trees(self):
        # NamedTree instances
        nt1 = pet.models.NamedTree()
        nt1.name = "name_nt1"
        nt2 = pet.models.NamedTree()
        nt2.name = "name_nt2"
        nts = [nt1, nt2]

        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=nts)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session =MagicMock(return_value=object_session_rv)

        expected = {
            nts[0].name : nts[0],
            nts[1].name : nts[1],
        }
        actual = pet.models.Package()._named_trees('branch')
        self.assertEqual(expected, actual)
