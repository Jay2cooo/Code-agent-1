import unittest
from pathlib import Path
from types import SimpleNamespace
from tempfile import TemporaryDirectory
from unittest.mock import patch
import agent

class AgentTests(unittest.TestCase):
    def test_container_boundary(self):
        cmd = agent.docker_command(Path('/tmp/task'), 'test', 'echo hello')
        for flag in ['--network=none', '--read-only', '--cap-drop=ALL', '--user=65534:65534']:
            self.assertIn(flag, cmd)
        self.assertIn('type=bind,source=/tmp/task,target=/workspace', cmd)
        self.assertEqual(cmd[-3:], ['sh', '-c', 'echo hello'])
        self.assertNotIn('ANTHROPIC_API_KEY', ' '.join(cmd))

    def test_denied_command_never_executes(self):
        with patch('builtins.input', return_value='n'), patch('agent.subprocess.Popen') as process:
            output, error = agent.run_command(Path('/tmp/task'), 'echo hello', 1)
            self.assertTrue(error)
            self.assertIn('DENIED', output)
            process.assert_not_called()

    def test_truncated_response_is_not_success(self):
        client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw:
                    SimpleNamespace(content=[], stop_reason='max_tokens')))
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(agent.run_agent('task', root, 'model', 1, 1, client, root/'log'), 1)

if __name__ == '__main__':
    unittest.main()
