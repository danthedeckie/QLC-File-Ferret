import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter import N,S,E,W

from reader import QLCFile

# Constants:
FUNCTION_TYPES = [
    ('Scene','Scenes'),
    ('Sequence','Sequences'),
    ('Collection','Collections'),
    ('EFX', 'EFX'),
    ('Audio', 'Audio Files'),
    ('Show','Shows'),
    ('Chaser','Chasers')
    ]

# Global State: (oh noes)
CLIPBOARD = []

class QLCFileBox(ttk.Frame):
    def __init__(self, master=None, filename=None):
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        self.filename=filename

        self.createWidgets()
        self.loadfile()

    def createWidgets(self):
        ttk.Label(self, text=self.filename).pack() 

        self.filterText = ttk.Entry(self)
        self.filterText.pack(padx=0.1)

        self.functionList = ttk.Treeview(self)
        self.functionList.pack(fill=tk.BOTH, expand=1)

        self.toolbar = tk.Frame(self)

        self.saveBtn = ttk.Button(self, text="Save As")
        self.saveBtn.pack(side=tk.RIGHT)

        self.saveBtn = ttk.Button(self, text="Close")
        self.saveBtn.pack(side=tk.RIGHT)

        self.pasteBtn = ttk.Button(self, text="Paste here")
        self.pasteBtn.pack(side=tk.RIGHT)

        ttk.Button(self, text="Copy Selected", command=self.copySelected).pack(side=tk.RIGHT)

        self.toolbar.pack(fill=tk.BOTH, expand=1)

    def loadfile(self):
        self.qfile = QLCFile(self.filename)
        funcs = self.qfile.list_functions()
        used_ids = self.qfile.all_used_function_ids()

        self.functionList.delete(*self.functionList.get_children())
        #self.functionList.delete(0, tk.END)

        # Top level tree items:
        for iid, plural in FUNCTION_TYPES:
            self.functionList.insert('', 'end', '_' + iid, text=plural)

        allcount = 0
        orphancount = 0

        for f in funcs:
            allcount += 1
            name = "[{}] {}".format(f.attrib["ID"], f.attrib["Name"])
            self.functionList.insert('_' + f.attrib["Type"],'end', 'FUNC:' + f.attrib["ID"], text=name)
            [print(x) for x in self.qfile.subfunctions(f)]
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

            CLIPBOARD.append(subfunc)

            for func in self.qfile.subfunctions(func, recurse=True):
                CLIPBOARD.append(subfunc)


    def pasteToHere(self):
        this.qfile.paste_functions_here(CLIPBOARD)
        # TODO: now update the function listbox.

class Application(ttk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        self.loadfile('C:/Users/daniel.fairhead/Desktop/LWW reimagein tests.qxw')

    def savefile(self):
        filename = asksaveasfile(filetypes=[("QLC+ File", "*.qxw")])

    def createToolbar(self):
        self.toolBar = tk.Frame()
        def btn(text, command):
            b = ttk.Button(self.toolBar, text=text, command=command)
            b.pack(side=tk.LEFT)
            return b

        btn('Quit', self.quit)

        btn('Load File', self.loadfile)

        #btn('Save File', self.savefile)

        #btn('Delete Selected', self.deleteFromAll)

        self.toolBar.pack(side=tk.TOP)

    def createWidgets(self):
        self.createToolbar()

        self.filesArea = tk.PanedWindow(orient=tk.HORIZONTAL, sashpad=10, sashwidth=2, height=400, width=300)
        self.filesArea.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def loadfile(self, filename=None):
        filename = filename or askopenfile(
                filetypes=[("QLC+ File",'*.qxw'),
                           ("XML File", '*.xml'),
                           ('Other...','*')])

        x = QLCFileBox(self.filesArea, filename)
        self.filesArea.add(x)

    def copyFunctions(self):
        pass

app = Application()
app.master.title('QLC+ Multi-file Helper Utility')
app.mainloop()

