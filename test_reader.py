import xml.etree.ElementTree as ET
from io import StringIO

from unittest import TestCase

from reader import NS, QLCFile
import snippets

class BasicFileTest(TestCase):
    def setUp(self):
        super().setUp()
        self.virtual_console = snippets.empty_virtual_console
        self.simple_desk = snippets.empty_simple_desk
        self.fixtures = []
        self.functions = []

    def get_xml(self):
        return '\n'.join((
            snippets.header,
            snippets.engine_header,
            '\n'.join(self.fixtures),
            '\n'.join(self.functions),
            snippets.engine_footer,
            self.virtual_console,
            self.simple_desk,
            snippets.footer))


class SanityTest(BasicFileTest):
    def test_basicfile(self):
        x = StringIO(self.get_xml())
        r = ET.parse(x).getroot()

    # TODO: callout to actual QLC+ to load the file and check it

    def test_some_fixtures(self):
        self.fixtures = [
                snippets.generic_fixture(0, 1),
                snippets.generic_fixture(1, 2),
                snippets.generic_fixture(2, 3, channels=6),
                ]

        x = StringIO(self.get_xml())
        r = ET.parse(x).getroot()

    def test_some_functions(self):
        self.functions = [
                snippets.function_scene(0, "Basic Scene"),
                snippets.function_scene(1, "Basic Scene 1"),
                snippets.function_scene(2, "Basic Scene 2"),
                ]
        x = StringIO(self.get_xml())
        r = ET.parse(x).getroot()

    def test_some_fixtures_and_functions(self):
        self.fixtures = [
                snippets.generic_fixture(0, 1),
                snippets.generic_fixture(1, 2),
                snippets.generic_fixture(2, 3, channels=6),
                ]

        self.functions = [
                snippets.function_scene(0, "Basic Scene"),
                snippets.function_scene(1, "Basic Scene 1"),
                snippets.function_scene(2, "Basic Scene 2"),
                ]

        x = StringIO(self.get_xml())
        r = ET.parse(x).getroot()

    # TODO: Functions USING fixtures...

##################################

class TestCopyingSimpleScene(BasicFileTest):
    def test_copy_to_blank_file(self):
        self.functions = []
        empty_file = QLCFile(StringIO(self.get_xml()))

        self.functions = [
                snippets.function_scene(0, "Basic Scene"),
                snippets.function_scene(1, "Basic Scene 1"),
                snippets.function_scene(2, "Basic Scene 2"),
                ]

        full_file = QLCFile(StringIO(self.get_xml()))

        clipboard = list(full_file.iter_functions_for_clipboard(['0','1','2']))
        empty_file.paste_functions_here(clipboard)

        new_functions = empty_file.list_functions()
        self.assertEqual(new_functions[0].attrib["Name"], "Basic Scene")
        self.assertEqual(new_functions[1].attrib["Name"], "Basic Scene 1")
        self.assertEqual(new_functions[2].attrib["Name"], "Basic Scene 2")

        self.assertEqual(new_functions[0].attrib["ID"], "0")
        self.assertEqual(new_functions[1].attrib["ID"], "1")
        self.assertEqual(new_functions[2].attrib["ID"], "2")

    def test_copy_to_nonempty_file(self):

        self.functions = [
                snippets.function_scene(0, "Basic Scene"),
                snippets.function_scene(1, "Basic Scene 1"),
                snippets.function_scene(2, "Basic Scene 2"),
                ]

        to_file = QLCFile(StringIO(self.get_xml()))

        self.functions = [
                snippets.function_scene(0, "Basic Scene A"),
                snippets.function_scene(1, "Basic Scene B"),
                snippets.function_scene(2, "Basic Scene C"),
                ]

        from_file = QLCFile(StringIO(self.get_xml()))

        clipboard = list(from_file.iter_functions_for_clipboard(['0','1','2']))
        to_file.paste_functions_here(clipboard)

        new_functions = to_file.list_functions()
        self.assertEqual(len(new_functions), 6)
        self.assertEqual(new_functions[0].attrib["Name"], "Basic Scene")
        self.assertEqual(new_functions[1].attrib["Name"], "Basic Scene 1")
        self.assertEqual(new_functions[2].attrib["Name"], "Basic Scene 2")
        self.assertEqual(new_functions[3].attrib["Name"], "Basic Scene A")
        self.assertEqual(new_functions[4].attrib["Name"], "Basic Scene B")
        self.assertEqual(new_functions[5].attrib["Name"], "Basic Scene C")


        self.assertEqual(new_functions[0].attrib["ID"], "0")
        self.assertEqual(new_functions[1].attrib["ID"], "1")
        self.assertEqual(new_functions[2].attrib["ID"], "2")
        self.assertEqual(new_functions[3].attrib["ID"], "3")
        self.assertEqual(new_functions[4].attrib["ID"], "4")
        self.assertEqual(new_functions[5].attrib["ID"], "5")




        

