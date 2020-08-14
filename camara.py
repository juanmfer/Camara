# Camara 2020
from tkinter import E, W, S, N
from tkinter.ttk import Scrollbar
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os
import numpy as np


# global contador


class Application:
    def __init__(self, output_path='./'):

        self.contador = 0
        global contador
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0)  # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.root = tk.Tk()  # initialize root window
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)
        self.root.columnconfigure(2, weight=5)
        self.root.columnconfigure(3, weight=5)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=5)
        self.root.rowconfigure(2, weight=5)
        self.root.rowconfigure(3, weight=5)
        self.root.geometry('820x1000')  # ancho y alto de ventana
        self.root.title("Camara")  # set window title
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.grid(row=0, column=0, columnspan=4, sticky=S + N + E + W)

        # BOTON FOTO
        btn = tk.Button(self.root, text="Foto!", command=self.take_snapshot)
        btn.grid(row=1, column=0, sticky=W + E)

        # BOTON BUSCAR
        bt = tk.Button(self.root, text="Buscar Imagenes", command=lambda: self.searchfiles('.jpg', './'))
        bt.grid(row=1, column=1, sticky=W)

        # BOTON Eliminar
        btd = tk.Button(self.root, text='Eliminar', command=self.eliminar)
        btd.grid(row=1, column=2, sticky=E)

        # CANTIDAD DE IMAGENES
        self.imagenes = tk.Label(self.root, text='Cantidad de imagenes en espera...', width=30)
        self.imagenes.grid(row=1, column=3, sticky=S + N + E + W)

        # BOTON SALIR
        bt2 = tk.Button(self.root, text='Salir', command=self.salida)
        bt2.grid(row=5, column=0, columnspan=4, sticky=S + N + E + W)

        scrollbar = Scrollbar(self.root)

        # LISTBOX IMAGENES
        scrollbar.grid(row=2, column=3, rowspan=3, sticky=W + N + S)
        self.lb = tk.Listbox(self.root)
        self.lb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lb.yview)
        self.lb.grid(row=2, column=0, rowspan=3, columnspan=3, sticky=S + N + E + W)

        # boton ventana
        btdere1 = tk.Button(self.root, text='Ventana', command=self.ventana1)
        btdere1.grid(row=2, column=3, sticky=E, ipadx=80)

        btdere2 = tk.Button(self.root, text='Salir', command=self.salida)
        btdere2.grid(row=2, column=3, sticky=E + S, ipadx=92)
        self.video_loop()

    def ventana1(self):
        global value4, guardo, comandodef
        self.comandodef = 0
        if self.lb.curselection():
            self.ventana1 = tk.Toplevel()
            value4 = self.lb.get(self.lb.curselection()[0])
            value5 = self.lb.get(self.lb.curselection()[0])
            self.ventana1.geometry('720x660')
            self.ventana1.title('Ventana 2')
            self.imgmuestro = value4
            self.img1 = Image.open(value4)
            self.img1 = self.img1.resize((640, 480), Image.ANTIALIAS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            self.muestro = tk.Label(self.ventana1, image=self.img1)
            self.muestro.grid(row=0, column=0, columnspan=5)

            botonfoto = tk.Button(self.ventana1, text='BORDES', command=lambda: self.comando1(value4))
            botonfoto.grid(padx=10, pady=10, ipadx=10, ipady=10, row=2, column=0, sticky=S)  # ipadx=150)

            botonfoto2 = tk.Button(self.ventana1, text='CONTRASTE', command=lambda: self.comando2(value4))
            botonfoto2.grid(padx=10, pady=10, ipadx=10, ipady=10, row=2, column=1, sticky=S)  # ipadx=150)

            botonfoto3 = tk.Button(self.ventana1, text='ORIGINAL', command=lambda: self.comando3(value4))
            botonfoto3.grid(padx=10, pady=10, ipadx=10, ipady=10, row=2, column=2, sticky=S)  # ipadx=150)

            botonfoto4 = tk.Button(self.ventana1, text='DETECCION DE ROSTRO', command=lambda: self.comando4(value5))
            botonfoto4.grid(padx=10, pady=10, ipadx=10, ipady=10, row=2, column=3, sticky=S)  # ipadx=150)

            botonfoto5 = tk.Button(self.ventana1, text='GRIS', command=lambda: self.comando5(value5))
            botonfoto5.grid(padx=10, pady=10, ipadx=10, ipady=10, row=2, column=4, sticky=S)  # ipadx=150)

            botguardar = tk.Button(self.ventana1, text='GUARDAR FOTO ACTUAL', command=lambda: self.comandog())
            botguardar.grid(padx=10, pady=10, ipadx=10, ipady=10, row=3, columnspan=5, sticky=S)  # ipadx=150)

        else:
            tk.messagebox.showinfo('Seleccionar imagen', 'Debes seleccionar una imagen')

    def searchfiles(self, extension, folder):
        # folder='./'
        self.lb.delete('0', 'end')
        con = 0
        # result = next(os.walk(folder))[2]
        contenido = os.listdir(folder)
        for file in contenido:
            if os.path.isfile(os.path.join(folder, file)) and file.endswith(extension):
                self.lb.insert(0, file)
                con += 1
        self.setnum(con)

    def setnum(self, con):
        # self.contador = tk.StringVar()
        self.imagenes['text'] = (con, 'imagenes')

    def open_file(self):
        try:
            photo2 = Image.open(self.lb.get(self.lb.curselection()[0]))
            photo2.show()
        except IndexError:
            pass

    def eliminar(self):
        try:
            MsgBox = tk.messagebox.askquestion('Eliminar imagen', 'Seguro de eliminar la imagen', icon='warning')
            if MsgBox == 'yes':
                index = self.lb.curselection()
                value = self.lb.get(index[0])
                os.unlink(value)
                self.lb.delete(self.lb.curselection()[0])
            else:
                tk.messagebox.showinfo('Volver', 'Ahora volverá a la pantalla de la aplicación')
        except IndexError:
            pass

    def salida(self):
        print("[INFO] Salida...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            frame = cv2.resize(frame, (800, 600), Image.ANTIALIAS)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR, Image.ANTIALIAS)
            # cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def take_snapshot(self):
        """ Take snapshot and save it to the file """
        ts = datetime.datetime.now()  # grab the current timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        self.current_image.save(p, "jpeg")  # save image as jpeg file
        print("[INFO] Guardado {}".format(filename))

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] Cerrando...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

    def comando1(self, value4):
        value42 = Image.open(value4)
        value42 = value42.resize((640, 480))
        self.imagev11 = cv2.cvtColor(np.asarray(value42), cv2.COLOR_BGR2GRAY)
        self.imagev1 = cv2.Canny(self.imagev11, 50, 100)
        self.imagev = ImageTk.PhotoImage(image=Image.fromarray(self.imagev1))
        self.muestro.configure(image=self.imagev)
        self.muestro.image = self.imagev
        self.guardo = self.imagev1
        self.comandodef = 1

    def comando2(self, value4):
        value42 = Image.open(value4)
        value42 = value42.resize((640, 480))
        self.imagev1 = cv2.cvtColor(np.asarray(value42), cv2.COLOR_BGR2RGB)
        self.imagev = ImageTk.PhotoImage(image=Image.fromarray(self.imagev1))
        self.muestro.configure(image=self.imagev)
        self.muestro.image = self.imagev
        self.guardo = cv2.cvtColor(np.asarray(value42), cv2.COLOR_BGRA2BGR)
        self.comandodef = 2

    def comando3(self, value4):
        # value421 = self.lb.get(self.lb.curselection()[0])
        self.value412 = Image.open(value4)
        self.value421 = self.value412.resize((640, 480), Image.ANTIALIAS)
        # self.imagev12 = cv2.cvtColor(np.asarray(value421), cv2.COLOR_RGB2BGR)
        self.imagev123 = ImageTk.PhotoImage(self.value421)
        self.muestro.configure(image=self.imagev123)
        self.muestro.image = self.imagev123
        self.guardo = cv2.cvtColor(np.asarray(self.value421), cv2.COLOR_RGB2BGR)
        self.comandodef = 3

    def comando4(self, value5):
        face_cascade = cv2.CascadeClassifier('face_detector.xml')
        img = cv2.imread(value5)
        img = cv2.resize(img, (640, 480))
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        self.imgrostro = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2RGB)
        self.imgrostro1 = ImageTk.PhotoImage(image=Image.fromarray(self.imgrostro))
        # self.imgrostro1 = self.imgrostro1.resize((640, 480))
        self.muestro.configure(image=self.imgrostro1)
        self.muestro.image = self.imgrostro1
        self.comando4img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGRA2BGR)
        self.comandodef = 4

    def comando5(self, value4):
        # value421 = self.lb.get(self.lb.curselection()[0])
        value42 = Image.open(value4)
        value42 = value42.resize((640, 480))
        self.imagev11 = cv2.cvtColor(np.asarray(value42), cv2.COLOR_BGR2GRAY)
        # self.imagev1 = cv2.Canny(self.imagev11, 50, 100)
        self.imagev = ImageTk.PhotoImage(image=Image.fromarray(self.imagev11))
        self.muestro.configure(image=self.imagev)
        self.muestro.image = self.imagev
        self.guardo = self.imagev11
        self.comandodef = 5

    def comandog(self):
        if self.comandodef == 1:
            ts1 = datetime.datetime.now()
            filename = "{}.jpg".format(ts1.strftime("%Y-%m-%d_%H-%M-%S"))
            p2 = os.path.join(self.output_path, filename)
            print("[INFO] Guardado {}".format(filename))
            cv2.imwrite(p2, self.guardo)
        elif self.comandodef == 2:
            ts1 = datetime.datetime.now()
            filename = "{}.jpg".format(ts1.strftime("%Y-%m-%d_%H-%M-%S"))
            p2 = os.path.join(self.output_path, filename)
            print("[INFO] Guardado {}".format(filename))
            cv2.imwrite(p2, self.guardo)
        elif self.comandodef == 3:
            ts1 = datetime.datetime.now()
            filename = "{}.jpg".format(ts1.strftime("%Y-%m-%d_%H-%M-%S"))
            p2 = os.path.join(self.output_path, filename)
            print("[INFO] Guardado {}".format(filename))
            cv2.imwrite(p2, self.guardo)
        elif self.comandodef == 4:
            ts1 = datetime.datetime.now()
            filename = "{}.jpg".format(ts1.strftime("%Y-%m-%d_%H-%M-%S"))
            p2 = os.path.join(self.output_path, filename)
            print("[INFO] Guardado {}".format(filename))
            cv2.imwrite(p2, self.comando4img)
        elif self.comandodef == 5:
            ts1 = datetime.datetime.now()
            filename = "{}.jpg".format(ts1.strftime("%Y-%m-%d_%H-%M-%S"))
            p2 = os.path.join(self.output_path, filename)
            print("[INFO] Guardado {}".format(filename))
            cv2.imwrite(p2, self.guardo)
        else:
            print('Ingrese algun efecto antes de guardar la foto')


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default='./', help="direccion de fotos (default: carpeta actual")
args = vars(ap.parse_args())


print('[INFO] Iniciado...')
pba = Application(args['output'])
pba.root.mainloop()
