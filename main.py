import tkinter as tk
from tkinter import filedialog
import boto3
from os.path import basename

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        self.controller.title('Facial Recognition Program')
        self.controller.state('zoomed')
        self.controller.iconphoto(False,
                                  tk.PhotoImage(file='C:/Users/serpe/OneDrive/Desktop/FRP/face.png'))

        headinglabel1 = tk.Label(self,
                               text='Facial Recognition Program',
                               font=('orbitron', 45, 'bold'),
                               foreground='white',
                               background='#3d3d5c')
        headinglabel1.pack(pady=25)

        space_label=tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        password_label = tk.Label(self,
                                  text='Enter your password',
                                  font=('orbitron', 13),
                                  bg='#3d3d5c',
                                  fg='white')
        password_label.pack(pady=10)

        my_password=tk.StringVar()
        password_entry_box=tk.Entry(self,
                                    textvariable=my_password,
                                    font=('orbitron', 12),
                                    width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)
        password_entry_box.configure(fg='black', show='*')

        def handle_focus_in(_):
            password_entry_box.bind('<Focusln>', handle_focus_in)




        def check_password():
            if my_password.get()=='123':
                controller.show_frame('MenuPage')
            else:
                incorrect_password_label['text']='Incorrect Password'
        enter_button=tk.Button(self,
                               text='Enter',
                               command=check_password,
                               relief='raised',
                               borderwidth= 3,
                               width=40,
                               height=3)
        enter_button.pack(pady=10)

        incorrect_password_label=tk.Label(self,
                                          text='',
                                          font=('orbitron',13),
                                          fg='white',
                                          bg='#33334d',
                                          anchor='n')
        incorrect_password_label.pack(fill='both',expand=True)
        def go_nt():
            controller.show_frame('PageTwo')


        bottom_frame= tk.Frame(self, relief='raised',borderwidth=3)
        bottom_frame.pack(pady=30,side='bottom')
        photo_r=tk.PhotoImage(file='C:/Users/serpe/OneDrive/Desktop/FRP/face.png')
        photo_r_label= tk.Button(bottom_frame,image=photo_r,text='', command=go_nt)
        photo_r_label.pack()
        photo_r_label.image=photo_r



class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        space_label = tk.Label(self, height=10, bg='#3d3d5c')
        space_label.pack()

        upload_label = tk.Label(self,
                                  text='Put a jpg',
                                  font=('orbitron', 13),
                                  bg='#3d3d5c',
                                  fg='white')
        upload_label.pack(pady=10)

        Upload = tk.StringVar()
        Upload_entry_box = tk.Entry(self,
                                      textvariable=Upload,
                                      font=('orbitron', 12),
                                      width=22)
        Upload_entry_box.focus_set()
        Upload_entry_box.pack(ipady=7)
        i=0
        def saveFile():
            text_file = filedialog.askopenfilename(defaultextension=".*",
                                                   initialdir="C:/Users/serpe/OneDrive/Desktop/FRP",
                                                   filetypes=(("jpeg files", "*.jpeg"),
                                                              ("all files", "*.*")))
            if  text_file:
                name = text_file
                s3 = boto3.client('s3')
                upload_file_bucket = 'mebucketrobert'
                upload_file_key = 'S3_project/'+basename(name)
                s3.upload_file(name, upload_file_bucket, upload_file_key)



        enter_button = tk.Button(self,
                                 text='Upload',
                                 command=saveFile,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)








class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
