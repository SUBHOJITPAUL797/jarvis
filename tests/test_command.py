import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock the 'eel' library to avoid GUI errors during testing.
eel = MagicMock()

@patch.dict('sys.modules', {'eel': eel})
class TestCommand(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test. It ensures that we have a fresh,
        un-cached import of the 'backend.command' module for each test.
        """
        if 'backend.command' in sys.modules:
            del sys.modules['backend.command']

    @patch('pyttsx3.init')
    def test_engine_is_initialized_once_on_import(self, mock_init):
        """
        Test that the pyttsx3 engine is initialized exactly once when the
        'backend.command' module is first imported.
        """
        # Import the module under test. This will execute its top-level code.
        from backend import command

        # Verify that pyttsx3.init() was called once.
        mock_init.assert_called_once()

    def test_engine_properties_and_speak_function(self):
        """
        Test that the global engine instance has the correct properties set
        and that the speak function uses it as expected.
        """
        # Import the specific objects we need from the module.
        from backend.command import engine, speak

        # Check that the speech rate was set correctly on the global engine instance.
        self.assertEqual(engine.getProperty('rate'), 174, "The speech rate should be set to 174.")

        # Mock the methods on the actual engine instance to test the 'speak' function's behavior.
        with patch.object(engine, 'say') as mock_say, \
             patch.object(engine, 'runAndWait') as mock_runAndWait:

            test_phrase = "hello world"
            speak(test_phrase)

            # Verify that the 'speak' function called the engine's methods correctly.
            mock_say.assert_called_once_with(test_phrase)
            mock_runAndWait.assert_called_once()

if __name__ == '__main__':
    unittest.main()