import unittestimport jsonimport loggingimport sysimport inspectimport osfrom customassertions import CustomAssertionsfrom mockFields import field_mapcmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(    inspect.currentframe()))[0], ".."))if cmd_folder not in sys.path:    sys.path.insert(0, cmd_folder)from rejira.lib.issue import Issuefrom example import configclass ReJIRATest(unittest.TestCase, CustomAssertions):    def setUp(self):        instance_config = self.setup_config()        instance_logging = self.setup_logging(instance_config)        with open('mock-req-1.txt', 'r') as file:            data = file.read()            file.close()        req = json.loads(data)        self.issue = Issue(instance_config, instance_logging)        self.issue.create_object(req, field_map)    def setup_config(self):        config.cache_host = os.getenv('REJIRA_CACHE_HOST', 'localhost')        config.cache_port = os.getenv('REJIRA_CACHE_PORT', 6379)        config.cache_db = os.getenv('REJIRA_CACHE_DB', 0)        config.cache_on = os.getenv('REJIRA_CACHE_ON', True)        config.cache_expire = os.getenv('REJIRA_CACHE_EXPIRE', 3600)        config.jira_user = os.getenv('REJIRA_JIRA_USER', '')        config.jira_pass = os.getenv('REJIRA_JIRA_PASS', '')        config.jira_options["server"] = os.getenv('REJIRA_JIRA_SERVER', '')        config.logging_level = os.getenv('REJIRA_LOGGING_LEVEL', 'ERROR')        config.logging_file = os.getenv('REJIRA_LOGGING_FILE', '')        return config    def setup_logging(self, instance_config):        logging.basicConfig(level=instance_config.logging_level)        logger = logging.getLogger(__name__)        if instance_config.logging_file:            handler = logging.FileHandler(instance_config.logging_file)            handler.setLevel(logging.INFO)            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")            handler.setFormatter(formatter)            logger.addHandler(handler)        return logger    def test_issue_close(self):        self.assertAttrNotExists(self.issue, "config")        self.assertAttrNotExists(self.issue, "logger")    def test_handle_sprint(self):        self.assertAttrExists(self.issue, "sprint")        self.assertEqual(self.issue.sprint.name, 'OM Sprint 1')        self.assertEqual(self.issue.sprint.state, 'ACTIVE')        self.assertEqual(self.issue.sprint.completeDate, '<null>')if __name__ == '__main__':    unittest.main()