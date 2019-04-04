import xml.etree.ElementTree as ET

NS = {'qlc': 'http://www.qlcplus.org/Workspace'}

class QLCFile(object):
    def __init__(self, filename):
        self.root = ET.parse(filename).getroot()

    def list_functions(self):
        return self.root.findall('qlc:Engine/qlc:Function', NS)

    def highest_function_id(self):
        return max(int(f.attrib['ID']) for f in self.list_functions())

    def used_function_ids(self):
        for f in self.list_functions():
            yield f.attrib['ID']

    def list_fixtures(self):
        return self.root.findall('qlc:Engine/qlc:Fixtures', NS)

    def all_used_function_ids(self):
        used_ids = set()
        for f in self._used_function_ids_by_vc():
            used_ids.add(f)

        for f in self._used_function_ids_by_chasers():
            used_ids.add(f)

        for f in self._used_function_ids_by_sequences():
            used_ids.add(f)

        for f in self._used_function_ids_by_collections():
            used_ids.add(f)

        for f in self._used_function_ids_by_shows():
            used_ids.add(f)

        return used_ids

    def _used_function_ids_by_vc(self):
        fs = self.root.findall('qlc:VirtualConsole//qlc:Function', NS)
        for f in fs:
            if 'ID' in f.attrib:
                yield f.attrib['ID']
            else:
                yield f.text

    def _used_function_ids_by_chasers(self):
        fs = self.root.findall("qlc:Engine//qlc:Function[@Type='Chaser']/qlc:Step", NS)
        for f in fs:
            yield f.text

    def _used_function_ids_by_collections(self):
        fs = self.root.findall("qlc:Engine//qlc:Function[@Type='Collection']/qlc:Step", NS)
        for f in fs:
            yield f.text

    def _used_function_ids_by_sequences(self):
        fs = self.root.findall("qlc:Engine//qlc:Function[@Type='Sequence']", NS)
        for f in fs:
            yield f.attrib["BoundScene"]

    def _used_function_ids_by_shows(self):
        fs = self.root.findall("qlc:Engine//qlc:Function[@Type='Show']//qlc:ShowFunction", NS)
        for f in fs:
            yield f.attrib["ID"]

    def function_by_id(self, fid):
        return self.root.find("qlc:Engine//qlc:Function[@ID='%i']" % int(fid), NS)

    def subfunctions(self, func):
        raise NotImplemented("subfuncs.... this is gonna get recursive")
        if func.attrib['Type'] == 'Show':
            for f in func.findall("*//qlc:ShowFunction", NS):
                yield self.function_by_id(f.attrib["ID"])

        # TODO!

    def paste_functions_here(self, clipboard):

        # Make fresh copies of all functions from clipboard,
        # so changes to data can't mess up other files.
        # This is probably not the most efficient way, but it should
        # work. I hope.
        new_functions = []
        for f in clipboard:
            new_functions.append(ET.fromstring(ET.tostring(f)))

        print(new_functions)

        fresh_id = self.highest_function_id() + 1

        current_ids = set(self.used_function_ids())

        for f in new_functions:
            if f.attrib['ID'] in current_ids:
                fresh_id += 1
                f.attrib['ID'] = str(fresh_id)
                current_ids.append(f.attrib['ID'])
                # TODO:
                #  - go through all other functions looking for any uses of the old
                #    function id, and replace it with the new one.
            # TODO:add the new functions to this file.


