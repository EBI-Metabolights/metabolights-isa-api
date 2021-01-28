import unittest
import tempfile
import shutil
import os
import logging


from isatools import isatab
from isatools.net.mw2isa import mw2isa_convert


log = logging.getLogger('isatools')

__author__ = 'proccaserra@gmail.com'


class mw2ISATest(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_conversion(self):
        success, study_id, validate = mw2isa_convert(studyid="ST000367", outputdir=self._tmp_dir, dl_option="no",
                                                     validate_option=True)
        # exit_code = sys.exit()

        if success and validate:
            log.info("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, 'i_investigation.txt')) as fp:
                report = isatab.validate(fp)
                if len(report['errors']) > 0:
                    self.fail("conversion successful but validation failed")
        else:
            self.fail("conversion failed, validation was not invoked")
