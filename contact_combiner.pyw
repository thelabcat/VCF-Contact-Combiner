#!/usr/bin/env python3
#Contact File Combining Program v1.0

"""
This program is designed to concatenate multiple vCard 
files into one vCard file for quicker importing on phones.

version 1.0:
    -Initial working release
"""

#Module imports
from tkinter import *
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import glob

EOL="\n" #\r\n for Windows, \r for Mac, \n for Unix. Most systems and programs can overlook this :)

#Root window object
class Root(Tk):
    """Valoin eBook Formatter Window"""
    def __init__(self):
        super(Root, self).__init__()
        self.grid()
        self.title("Contact File Combiner")
        self.build()
        self.mainloop()
    def build(self):
        """Main construction of the window"""
        #Setup input file field and button
        Label(self, text="Input folder:").grid(row=0, column=0, sticky=E)
        self.input_ent=Entry(self)
        self.input_ent.grid(row=0, column=1, sticky=W)
        Button(self, text="Browse", command=self.browse_input).grid(row=0, column=2)

        #Setup converter button
        Button(self, text="Combine", command=self.run_combiner).grid(row=1, column=1)

    def run_combiner(self):
        """Initiate the combining process"""

        infolder=self.input_ent.get()
        try:
            infiles=glob.glob(infolder+"\\*")
        except PermissionError:
            mb.showerror("Access Denied", "The program was denied access\nto the input folder.")
            self.input_ent.delete(0, END)
            return
        if not infiles:
            mb.showerror("No input", "No input files found.")
            self.input_ent.delete(0, END)
            return
        for inf in infiles[:]:
            if inf.split(".")[-1]!="vcf":
                infiles.remove(inf)
        if not infiles:
            mb.showerror("No input", "Program only reads vCard files.")
            self.input_ent.delete(0, END)
            return

        try:
            combined=""
            for fn in infiles:
                f=open(fn)
                text=f.read()
                f.close()
                for l in text.splitlines():
                    combined+=l+EOL #Convert all EOLs to specified EOL escape sequence
            self.save_output(text)
                
        except PermissionError:
            mb.showerror("Access Denied", "The program was denied access\nto the output folder.")
            return
        mb.showinfo("Complete", "Contacts combined successfuly :)")
            
    def browse_input(self):
        """Browse for input directory"""
        self.input_ent.delete(0, END)
        self.input_ent.insert(0, fd.askdirectory(title="Folder of contacts to combine"))
    
    def save_output(self, text):
        """Save to output file"""
        f=fd.asksaveasfile(title="Save combined contact", filetypes=[("vCard contact", "*.vcf")], defaultextension=".vcf")
        f.write(text)
        f.close()

Root()

#Solo Deo gloria et lauda, amen.
