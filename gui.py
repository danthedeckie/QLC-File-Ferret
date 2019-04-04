'''
    "QLC+ File Ferret" - (C) 2019 Daniel Fairhead
    ---------------------------------------------

    gui.py
     - The main Graphical User Interface

'''

########
# One Day TODO:
# - Checking Fixtures as well when moving functions.
########

import sys
from os.path import basename

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import askyesno

from reader import QLCFile

# Constants:
FUNCTION_TYPES = [
    #('QLC Function TYPE', 'Plural Display Name')
    ('Scene', 'Scenes'),
    ('Sequence', 'Sequences'),
    ('Collection', 'Collections'),
    ('EFX', 'EFX'),
    ('Audio', 'Audio Files'),
    ('Show', 'Shows'),
    ('Chaser', 'Chasers'),
    ]

# Global State: (oh noes)
CLIPBOARD = []

class QLCFileBox(ttk.Frame):
    '''
        Multiple files can be loaded into the main window.  Each one gets its own
        QLCFileBox which is a vertical strip with a treeview showing all the functions,
        some filtering/searching tools and some buttons to Copy/Paste/Delete functions.
        ---

        The TreeView widget stores the Function ID (fid) as its unique item idenifier (iid)
        which is useful for getting back to the original function in the XML file.

        However, since we also need some 'fake' other nodes in the tree (Such as section
        nodes, and possibly folder, etc later on) all function iids are prefixed with 'FUNC:'
        and all section nodes are prefixed with '_'.

    '''

    def __init__(self, master=None, filename=None):
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        self.filename=filename

        self.create_widgets()
        self.load_file()
        self.update_treeview()

    def create_widgets(self):
        self.filenameText = tk.StringVar()
        ttk.Label(self, textvariable=self.filenameText).pack() 

        self.filterText = ttk.Entry(self) # TODO
        self.filterText.pack(padx=0.1)

        self.functionList = ttk.Treeview(self)
        self.functionList.pack(fill=tk.BOTH, expand=1)

        self.toolbar = tk.Frame(self)

        self.saveBtn = ttk.Button(self, text="Save As", command=self.save_as)
        self.saveBtn.pack(side=tk.RIGHT)

        self.saveBtn = ttk.Button(self, text="Close") # TODO
        self.saveBtn.pack(side=tk.RIGHT)

        self.pasteBtn = ttk.Button(self, text="Paste here", command=self.pasteToHere)
        self.pasteBtn.pack(side=tk.RIGHT)

        ttk.Button(self, text="Copy Selected", command=self.copySelected).pack(side=tk.RIGHT)

        self.toolbar.pack(fill=tk.BOTH, expand=1)

    def save_as(self):
        filename = asksaveasfile(
                filetypes=[("QLC+ File", '*.qxw')]
                )

        if not filename: return

        filename = filename.name

        self.qfile.write(filename)
        self.filename = filename
        self.update_treeview()

    def load_file(self):
        self.qfile = QLCFile(self.filename)
        self.filenameText.set(basename(self.filename))

    def update_treeview(self):
        '''
            This should be able to be called multiple times without mucking up
            data.  It's called after file load, and also after paste / delete
            operations.  If performance is an issue those might get replaced with
            simpler refresh functions.
        '''
        funcs = self.qfile.list_functions()
        used_ids = self.qfile.all_used_function_ids()

        self.functionList.delete(*self.functionList.get_children())

        # Top level tree items (Sections):
        for iid, plural in FUNCTION_TYPES:
            self.functionList.insert('', 'end', '_' + iid, text=plural)

        allcount = 0
        orphancount = 0

        # TODO: Add an extra column showing if a function is used or not?
        # TODO: some kind of renaming functions capacity?
        # TODO: An 'auto-update all buttons and sliders' in the VC to have new names?
        # TODO: Show in folders mode
        # TODO: Create folders and sort out functions into new folders depending on usage.
        # TODO: Images for function type...

        for f in funcs:
            allcount += 1
            name = "{} [{}]".format(f.attrib["Name"],f.attrib["ID"])
            self.functionList.insert('_' + f.attrib["Type"],'end', 'FUNC:' + f.attrib["ID"], text=name)

            #[print(x) for x in self.qfile.subfunction_ids(f)]

            #if f.attrib['ID'] not in used_ids:
            #    self.orphanFunctions.insert(tk.END, name)
            #    orphancount += 1

        #self.allFuncLabel.set("All Functions ({})".format(allcount))
        #self.orphanFuncLabel.set("Orphan Functions ({})".format(orphancount))

    def copySelected(self):
        # Only get selected functions, and strip FUNC: treeview iid prefix:
        selected_ids = [iid[5:] for iid in self.functionList.selection()
                if iid.startswith('FUNC:')]

        CLIPBOARD.clear()

        for iid in selected_ids:
            func = self.qfile.function_by_id(iid)
            if not func: continue

            if not func in CLIPBOARD:
                CLIPBOARD.append(func)

            for func in self.qfile.subfunction_ids(func, recurse=True):
                if not func in CLIPBOARD:
                    CLIPBOARD.append(func)


    def pasteToHere(self):
        self.qfile.paste_functions_here(CLIPBOARD)
        self.update_treeview()


class Application(ttk.Frame):
    '''
        The main Application Frame.
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def createToolbar(self):
        self.toolBar = tk.Frame()
        def btn(text, command):
            b = ttk.Button(self.toolBar, text=text, command=command)
            b.pack(side=tk.LEFT)
            return b

        btn('Quit', self.quit)

        btn('Load File', self.load_file)

        # TODO: a Status bar or something showing whats in the clipboard?
        # TODO: an UNDO system?

        self.toolBar.pack(side=tk.TOP)

    def create_widgets(self):
        self.createToolbar()

        self.filesArea = tk.PanedWindow(orient=tk.HORIZONTAL, sashpad=10, sashwidth=2, height=400, width=600)
        self.filesArea.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def load_file(self, filename=None):
        filename = filename or askopenfile(
                filetypes=[("QLC+ File",'*.qxw'),
                           ("XML File", '*.xml'),
                           ('Other...','*')])

        if not filename:
            return

        if hasattr(filename, 'name'):
            filename = filename.name

        x = QLCFileBox(self.filesArea, filename)
        self.filesArea.add(x, minsize=100)


if __name__ == '__main__':
    app = Application()
    app.master.title('QLC+ Multi-file Helper Utility')

    for f in (sys.argv[1:]):
        try:
            app.load_file(f)
        except Exception as e:
            print(e)

    app.mainloop()

