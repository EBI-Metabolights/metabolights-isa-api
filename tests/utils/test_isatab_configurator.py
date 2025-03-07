import unittest
import os
from isatools.tests import utils


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTabConfigurator(unittest.TestCase):

    def setUp(self):
        self._config_dir = utils.DEFAULT2015_XML_CONFIGS_DATA_DIR

    def tearDown(self):
        pass

    def test_parse_configuration_genome_seq_xml(self):
        from isatools.io import isatab_configurator as configurator
        config_obj = configurator.parse(os.path.join(self._config_dir, 'genome_seq.xml'), True)  # Silent output
        self.assertEqual(len(config_obj.isatab_configuration), 1)
        self.assertEqual(config_obj.isatab_configuration[0].table_name, 'genome_seq')
        self.assertEqual(config_obj.isatab_configuration[0].isatab_assay_type, 'generic_assay')
        self.assertEqual(config_obj.isatab_configuration[0].isatab_conversion_target, 'sra')
        self.assertEqual(config_obj.isatab_configuration[0].measurement.term_label,
                         'genome sequencing')
        self.assertEqual(config_obj.isatab_configuration[0].technology.term_label,
                         'nucleotide sequencing')
        self.assertEqual(len(config_obj.isatab_configuration[0].field), 15)
        self.assertEqual(config_obj.isatab_configuration[0].field[0].header, 'Sample Name')
        self.assertEqual(config_obj.isatab_configuration[0].field[0].data_type, 'String')
        self.assertFalse(config_obj.isatab_configuration[0].field[0].is_file_field)
        self.assertFalse(config_obj.isatab_configuration[0].field[0].is_multiple_value)
        self.assertTrue(config_obj.isatab_configuration[0].field[0].is_required)
        self.assertFalse(config_obj.isatab_configuration[0].field[0].is_hidden)
        self.assertEqual(config_obj.isatab_configuration[0].field[0].description, 'sample name')
        self.assertEqual(config_obj.isatab_configuration[0].field[0].default_value, '')
        self.assertEqual(config_obj.isatab_configuration[0].field[0].generated_value_template,
                         '[INSTITUTION].Group-[GROUP_NO].Subject-[SUBJECT_NO].[SAMPLE_EXTRACT]')
        self.assertEqual(len(config_obj.isatab_configuration[0].protocol_field), 4)
        self.assertEqual(config_obj.isatab_configuration[0].protocol_field[0].protocol_type,
                         'nucleic acid extraction')

    def test_load_config_metagenome_seq(self):
        from isatools.io import isatab_configurator as configurator
        config_dict = configurator.load(self._config_dir)
        self.assertEqual(len(config_dict), 30)
        self.assertEqual(config_dict[('metagenome sequencing', 'nucleotide sequencing')].isatab_configuration[0]
                         .table_name, 'metagenome_seq')
        self.assertEqual(configurator.get_config(
            config_dict, 'metagenome sequencing', 'nucleotide sequencing')[0].header, 'Sample Name')
