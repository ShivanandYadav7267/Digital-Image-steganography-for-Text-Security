from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import  os

class Stegno:

    art ='''¯\_(ツ)_/¯'''
    art2 = '''
@(\/)
(\/)-{}-)@
@(={}=)/\)(\/)
(\/(/\)@| (-{}-)
(={}=)@(\/)@(/\)@
(/\)\(={}=)/(\/)
@(\/)\(/\)/(={}=)
(-{}-)""""@/(/\)
|:   |
/::'   \\
/:::     \\
|::'       |
|::        |
\::.       /
':______.'
`""""""`'''
    output_image_size = 0

    def main(self,root):
        root.title('ImageSteganography')
        root.geometry('500x600')
        root.resizable(width =False, height=False)
        f = Frame(root)

        title = Label(f,text='Image Steganography')
        title.config(font=('courier',33))
        title.grid(pady=10)

        b_encode = Button(f,text="Hide Message",command= lambda :self.frame1_encode(f), padx=25)
        b_encode.config(font=('courier',14))
        b_decode = Button(f, text="Reveal Message",padx=14,command=lambda :self.frame1_decode(f))
        b_decode.config(font=('courier',14))
        b_decode.grid(pady = 12)

        ascii_art = Label(f,text=self.art)
        # ascii_art.config(font=('MingLiU-ExtB',50))
        ascii_art.config(font=('courier',60))

        ascii_art2 = Label(f,text=self.art2)
        # ascii_art.config(font=('MingLiU-ExtB',50))
        ascii_art2.config(font=('courier',12,'bold'))

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)
        ascii_art.grid(row=4,pady=10)
        ascii_art2.grid(row=5,pady=5)

    def home(self, frame=None):
        if frame is not None:
            try:
                frame.destroy()
            except:
                pass
        for widget in root.winfo_children():
            widget.destroy()
        self.main(root)

    def frame1_decode(self,f):
        f.destroy()
        d_f2 = Frame(root)
        label_art = Label(d_f2, text='٩(^‿^)۶')
        label_art.config(font=('courier',90))
        label_art.grid(row =1,pady=50)
        l1 = Label(d_f2, text='Select Image with Hidden text:')
        l1.config(font=('courier',18))
        l1.grid()
        bws_button = Button(d_f2, text='Select', command=lambda :self.frame2_decode(d_f2))
        bws_button.config(font=('courier',18))
        bws_button.grid()
        back_button = Button(d_f2, text='Cancel', command=lambda : Stegno.home(self,d_f2))
        back_button.config(font=('courier',18))
        back_button.grid(pady=15)
        back_button.grid()
        d_f2.grid()

    def frame2_decode(self,d_f2):
        d_f3 = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4= Label(d_f3,text='Selected Image :')
            l4.config(font=('courier',18))
            l4.grid()
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.grid()
            hidden_data = self.decode(myimg)

            if "||" in hidden_data:
                stored_password, secret_text = hidden_data.split("||", 1)

                entered_password = self.ask_password_dialog()

                if entered_password == stored_password:
                    l2 = Label(d_f3, text='Hidden data is :')
                    l2.config(font=('courier',18))
                    l2.grid(pady=10)
                    text_area = Text(d_f3, width=50, height=10)
                    text_area.insert(INSERT, secret_text)
                    text_area.configure(state='disabled')
                    text_area.grid()
                else:
                    messagebox.showerror("Error", "Incorrect password! Access denied.")
                    self.home(d_f3)
                    return
            else:
                messagebox.showinfo("Info", "No password-protected message found or invalid data.")

            back_button = Button(d_f3, text='Cancel', command= lambda :self.page3(d_f3), padx=14)
            back_button.config(font=('courier',11))
            back_button.grid(pady=15)
            back_button.grid()
            show_info = Button(d_f3,text='More Info',command=self.info)
            show_info.config(font=('courier',11))
            show_info.grid()
            d_f3.grid(row=1)
            d_f2.destroy()

    def ask_password_dialog(self):
        pw_window = Toplevel()
        pw_window.title("Password Required")
        pw_window.geometry("400x200")  # Increased size
        pw_window.resizable(False, False)

        pw_window.update_idletasks()
        x = (pw_window.winfo_screenwidth() - pw_window.winfo_reqwidth()) // 2
        y = (pw_window.winfo_screenheight() - pw_window.winfo_reqheight()) // 2
        pw_window.geometry(f"+{x}+{y}")

        Label(pw_window, text="Enter password to decode:", font=('courier', 16)).pack(pady=20)

        password_var = StringVar()
        password_entry = Entry(pw_window, textvariable=password_var, show='*', font=('courier', 14), width=25)
        password_entry.pack(pady=10)
        password_entry.focus()

        pw_value = {'password': None}

        def submit_pw(event=None):
            pw_value['password'] = password_var.get()
            pw_window.destroy()
    
        pw_window.bind('<Return>', submit_pw)

        Button(pw_window, text="Submit", command=submit_pw, font=('courier', 12), width=10).pack(pady=10)

        pw_window.wait_window()  # Wait for user input
        return pw_value['password']

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def frame1_encode(self,f):
        f.destroy()
        f2 = Frame(root)
        label_art = Label(f2, text='\'\(°Ω°)/\'')
        label_art.config(font=('courier',70))
        label_art.grid(row =1,pady=50)
        l1= Label(f2,text='Select the Image in which \nyou want to hide text :')
        l1.config(font=('courier',18))
        l1.grid()

        bws_button = Button(f2,text='Select',command=lambda : self.frame2_encode(f2))
        bws_button.config(font=('courier',18))
        bws_button.grid()
        back_button = Button(f2, text='Cancel', command=lambda : Stegno.home(self,f2))
        back_button.config(font=('courier',18))
        back_button.grid(pady=15)
        back_button.grid()
        f2.grid()


    def frame2_encode(self,f2):
        ep= Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('All Files', '*.*'),('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300,200))
            img = ImageTk.PhotoImage(myimage)
            l3= Label(ep,text='Selected Image')
            l3.config(font=('courier',18))
            l3.grid()
            panel = Label(ep, image=img)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text='Enter the message')
            l2.config(font=('courier',18))
            l2.grid(pady=10)
            
            text_area = Text(ep, width=50, height=8)
            text_area.grid()
            
            l3 = Label(ep, text='Set a password for this message:')
            l3.config(font=('courier',18))
            l3.grid(pady=10)

            password_entry = Entry(ep, width=33, show='*')
            password_entry.grid()

            encode_button = Button(ep, text='Cancel', command=lambda : Stegno.home(self,ep), padx=31)
            encode_button.config(font=('courier',12))

            back_button = Button(ep, text='Hide Message', command=lambda : [self.enc_fun(text_area, myimg, password_entry.get()), Stegno.home(self,ep)],)
            back_button.config(font=('courier',12))

            back_button.grid(pady=15)
            encode_button.grid()

            ep.grid(row=1)
            f2.destroy()


    def info(self):
        try:
            str = 'original image:-\nsize of original image:{}mb\nwidth: {}\nheight: {}\n\n' \
                  'decoded image:-\nsize of decoded image: {}mb\nwidth: {}' \
                '\nheight: {}'.format(self.output_image_size.st_size/1000000,
                                    self.o_image_w,self.o_image_h,
                                    self.d_image_size/1000000,
                                    self.d_image_w,self.d_image_h)
            messagebox.showinfo('info',str)
        except:
            messagebox.showinfo('Info','Unable to get the information')
    def genData(self,data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self,pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            # Eigh^th pixel of every set tells
            # whether to stop or read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self,newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):

            # Putting modified pixels in the new image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg, password):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
            return
        if len(password.strip()) == 0:
            messagebox.showinfo("Alert", "Please set a password before encoding")
            return

        # Combine password + separator + secret text
        combined_data = password + "||" + data

        newimg = myimg.copy()
        self.encode_enc(newimg, combined_data)
        my_file = BytesIO()
        temp = os.path.splitext(os.path.basename(myimg.filename))[0]
        newimg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=[('png', '*.png')], defaultextension=".png"))
        self.d_image_size = my_file.tell()
        self.d_image_w, self.d_image_h = newimg.size
        messagebox.showinfo("Success", "Encoding Successful!\nFile saved with password protection.")
        
    def page3(self,frame):
        frame.destroy()
        self.main(root)

root = Tk()

o = Stegno()
o.main(root)

root.mainloop()
