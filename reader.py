'''
    "QLC+ File Ferret" - (C) 2019 Daniel Fairhead
    ---------------------------------------------

    reader.py
     - QLC+ File reading / writing / modifying.

'''



import xml.etree.ElementTree as ET

QLC_NAMESPACE = 'http://www.qlcplus.org/Workspace'
NS = {'qlc': QLC_NAMESPACE}

ET.register_namespace('', QLC_NAMESPACE)

class QLCFile(object):
    def __init__(self, filename):
        self.root = ET.parse(filename).getroot()

    def write(self, filename, *vargs, **kwargs):
        new_file = ET.ElementTree(self.root)

        with open(filename, 'w') as f:
            # apparently etree cannot write doctypes :-(
            # oh well. we can.
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE Workspace>\n')
            new_file.write(f, encoding="unicode", xml_declaration=False, *vargs, **kwargs)

    def list_functions(self):
        return self.root.findall('qlc:Engine/qlc:Function', NS)

    def highest_function_id(self):
        '''
            When creating new functions, or copying a function in from another file
            we need to know where to start incrementing from.
        '''
        try:
            return max(int(f.attrib['ID']) for f in self.list_functions())
        except ValueError:
            return 0

    def used_function_ids(self):
        for f in self.list_functions():
            yield f.attrib['ID']

    def list_fixtures(self):
        return self.root.findall('qlc:Engine/qlc:Fixtures', NS)

    def all_used_function_ids(self):
        used_ids = set()
        used_ids.update(
                self._used_function_ids_by_vc(),
                self._used_function_ids_by_chasers(),
                self._used_function_ids_by_sequences(),
                self._used_function_ids_by_collections(),
                self._used_function_ids_by_shows(),
            )

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

    def subfunction_ids(self, func, recurse=False):

        if func.attrib['Type'] == 'Show':
            for f in func.findall(".//qlc:ShowFunction", NS):
                subfunc = self.function_by_id(f.attrib["ID"])
                yield subfunc
                if recurse:
                    yield from self.subfunction_ids(subfunc)
        elif func.attrib['Type'] == 'Sequence':
            yield func.attrib['BoundScene']
        elif func.attrib['Type'] in ('Collection', 'Chaser'):
            print(ET.tostring(func))
            for f in func.findall(".//qlc:Step", NS):
                print('step!')
                print(ET.tostring(f))
                subfunc = self.function_by_id(f.text)
                yield subfunc
                if recurse:
                    yield from self.subfunction_ids(subfunc)


    def subfunction_id_replace(self, func, old_id, new_id):
        if func.attrib['Type'] == 'Show':
            for f in func.findall(".//qlc:ShowFunction", NS):
                if f.attrib["ID"] == old_id:
                    f.attrib["ID"] = new_id
        elif func.attrib['Type'] == 'Sequence':
            if func.attrib['BoundScene'] == old_id:
                func.attrib['BoundScene'] = new_id
        elif func.attrib['Type'] in ('Collection', 'Chaser'):
            for f in func.findall(".//qlc:Step", NS):
                if f.text == old_id:
                    f.text = new_id


    def paste_functions_here(self, clipboard):

        # Make fresh copies of all functions from clipboard,
        # so changes to data can't mess up other files.
        # This is probably not the most efficient way, but it should
        # work. I hope.
        new_functions = []
        for f in clipboard:
            new_functions.append(ET.fromstring(ET.tostring(f)))

        # print(new_functions)

        fresh_id = self.highest_function_id() + 1

        current_ids = set(self.used_function_ids())

        # TODO: Look for Duplicate Functions - and don't copy them automatically,
        #       but instead ask the user what to do.

        replace_tables = {}

        for f in new_functions:
            if f.attrib['ID'] in current_ids:
                fresh_id += 1

                # Fix any references to this function_id in other functions:
                for ff in new_functions:
                    self.subfunction_id_replace(ff, f.attrib['ID'], str(fresh_id))

                # And update this function itself...
                f.attrib['ID'] = str(fresh_id)
                current_ids.add(f.attrib['ID'])

        enginenode = self.root.find('qlc:Engine', NS)

        for f in new_functions:
            enginenode.append(f)
