import tkinter as tk   #for the GUI tKinter
from tkinter import *   
from tkinter import filedialog 
from tkinter import messagebox
from PIL import Image  #for image access
import base64    # for Advance Encryption Standard (Encryption and Decryption message that is to be passed)
import random    # random key generation
from Crypto.Cipher import AES
import os

class IMG_Stegno:
    
    def __init__(self, window):
        self.window = window  # Store the main window
        self.img_entry = None
        self.new_img_entry = None
        self.data_entry = None
        self.key_entry = None

    def main(self):  # Main window GUI parameters

        window.title("Steganography Tool")
        window.geometry('900x900')
        window.resizable(width=True, height=True)
        window.config(bg='#e3f4f1')
        frame = Frame(window)
        frame.grid()

        # Title
        title = Label(frame, text="Steganography Tool", font=('Times new roman', 25, 'bold'))
        title.grid(row=0, column=1, pady=20)
        title.config(bg='#e3f4f1')

        encode_button = Button(frame, text="Encode", command=lambda :self.encode_frame1(frame), padx=14, bg='#e3f4f1')
        encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
        encode_button.grid(row=1, column=0, padx=10, pady=20)

        decode_button = Button(frame, text="Decode", command=lambda :self.decode_frame1(frame), padx=14, bg='#e3f4f1')
        decode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
        decode_button.grid(row=1, column=2, padx=10, pady=20)


        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # Start the GUI application
        window.mainloop()

    def browse_image(self):  # For Browsing the image name which is to be used for the image steganography 
        image_path = filedialog.askopenfilename(filetypes=[("JPEG Files", "*.jpg")])
        image_name = os.path.basename(image_path)
        self.img_entry.delete(0, tk.END)
        self.img_entry.insert(0, image_name)
        

    def generate_aes_key(self):   # random key genration for the AES 
        key = random.SystemRandom().getrandbits(128)
        key_bytes = key.to_bytes(16, byteorder='big')
        return key_bytes

    def encrypt_message(self, message, key):  # The Encryption using AES algorithm
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext = cipher.encrypt(message)
        return base64.b64encode(nonce + ciphertext)

    def decrypt_message(self, encrypted_message, key):    # The Decryption using AES algorithm
        encrypted_message = base64.b64decode(encrypted_message)
        nonce = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_message = cipher.decrypt(ciphertext)
        return decrypted_message

    def encrypt_image(path, key):   # The Encryption of the steganographed image
        try:
            fin = open(path, 'rb')
            image = fin.read()
            fin.close()
            image = bytearray(image)
            for index, value in enumerate(image):
                image[index] = value ^ key
            fin = open(path, 'wb')
            fin.write(image)
            fin.close()
            messagebox.showinfo("Success!!","Image Encryption Done...")
        except Exception as e:
            messagebox.showerror("Error", f"Image Encryption failed: {str(e)}")


    def decrypt_image(self, path, key):   # The Decryption of the steganographed image
        try:
            fin = open(path, 'rb')
            image = fin.read()
            fin.close()
            image = bytearray(image)
            for index, values in enumerate(image):
                image[index] = values ^ key
            fin = open(path, 'wb')
            fin.write(image)
            fin.close()
            print('Image Decryption Done...')
        except Exception as e:
            print('Error caught:', e)

    def genData(self, data):    #convert input data into 8 bit binary formate
        newd = []
        for char in data:
            newd.append(format(ord(char), '08b'))
        return newd

    def modPix(self, pixels, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pixels)

        for i in range(lendata):
            # Extract the RGB values for current pixel
            pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
            for j in range(0, 8):
                # For each 8 bits of the data byte:
                if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                    # If the data bit is 0 and the least significant bit of the pixel component is odd, make it even
                    pix[j] -= 1
                elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                    # If the data bit is 1 and the least significant bit of the pixel component is even, make it odd
                    if pix[j] != 0:
                        pix[j] -= 1
                    else:
                        pix[j] += 1
            if i == lendata - 1:
                 # Handle padding for the last data byte
                if pix[-1] % 2 == 0:
                    if pix[-1] != 0:
                        pix[-1] -= 1
                    else:
                        pix[-1] += 1
            else:
                # Ensure that the last bit of the pixel component is even for all non-last data bytes
                if pix[-1] % 2 != 0:
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, image, data):   # Generating the steganography image 
        newimg = image.copy()
        pixels = newimg.getdata()
        encoded_pixels = list(self.modPix(pixels, data))
        newimg.putdata(encoded_pixels)
        return newimg

    def decode(self, image):#  decode the steganography image and return data
        data = ''
        imgdata = iter(image.getdata())
        while True:
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

    def encode_frame1(self,F):#  encode frame GUI

        F.destroy()
        F2 = Frame(window)
        title = Label(F2, text="Encode Data Using Steganography", font=('Times new roman', 20, 'bold'))
        title.grid(row=0, column=1, pady=20)
        title.config(bg='#e3f4f1')

        img_entry_label = Label(F2, text="Image Path (Name & Extension):", font=('Times New Roman', 16, 'bold'))
        img_entry_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.img_entry = tk.Entry(F2, font=('Times New Roman', 16))
        self.img_entry.grid(row=1, column=1, padx=10, pady=10)

        browse_image_button = tk.Button(F2, text="Browse Image", command=lambda: self.browse_image())
        browse_image_button.config(font=('Helvetica', 18), bg='#e8c1c7')
        browse_image_button.grid(row=2, column=0, columnspan=2, pady=20)

        data_entry_label = Label(F2, text="Data:", font=('Times New Roman', 16, 'bold'))
        data_entry_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.data_entry = tk.Entry(F2, font=('Times New Roman', 16))
        self.data_entry.grid(row=3, column=1, padx=10, pady=10)

        new_img_entry_label = Label(F2, text="New Image Name (Name & Extension):", font=('Times New Roman', 16, 'bold'))
        new_img_entry_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.new_img_entry = tk.Entry(F2, font=('Times New Roman', 16))
        self.new_img_entry.grid(row=4, column=1, padx=10, pady=10)

        key_entry_label = Label(F2, text="Image Key (for Encoding):", font=('Times New Roman', 16, 'bold'))
        key_entry_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.key_entry = tk.Entry(F2, font=('Times New Roman', 16))
        self.key_entry.grid(row=5, column=1, padx=10, pady=10)

        encode_button = Button(F2, text="Encrypt", command=lambda: self.encode_button_click(F2), padx=14, bg='#e3f4f1')
        encode_button.config(font=('Helvetica', 18), bg='#e8c1c7')
        encode_button.grid(row=6, column=0, pady=20)

        button_back = Button(F2, text='Cancel', command=lambda: IMG_Stegno.back(self, F2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(row=6, column=1, pady=20)  # Use column 1
        button_back.grid()

        F2.grid()

    def encode_button_click(self, e_F2):  # ENCODE BUTTON CLICK FUNCTION
        e_pg = Frame(window)
        img_path = self.img_entry.get()
        data = self.data_entry.get()
        new_img_name = self.new_img_entry.get()
        img_key = self.key_entry.get()

        try:
            if img_path and data and new_img_name and img_key:
                image = Image.open(img_path, 'r')
                new_img = self.encode_enc(image, data)
                new_img.save(new_img_name, 'PNG')
                self.encrypt_image_file(new_img_name, int(img_key))  # Convert img_key to an integer
                messagebox.showinfo("Success!", "Encoding and Encryption Successful\nFile is saved as provided_name.jpg in the same directory")
            else:
                messagebox.showinfo("All fields are required!")
        except Exception as e:
            messagebox.showinfo("Error", f"Encoding and Encryption failed: {str(e)}")

        # Destroy the frame F (e_F2 in your previous code)
        e_pg.destroy()

    def encrypt_image_file(self, path, key):    # The Encryption of the steganographed image
        try:
            fin = open(path, 'rb')
            image = fin.read()
            fin.close()
            image = bytearray(image)
            for index, value in enumerate(image):
                image[index] = value ^ key
            fin = open(path, 'wb')
            fin.write(image)
            fin.close()
        except Exception as e:
            messagebox.showinfo("Error", f"Image Encryption failed: {str(e)}")

    def decode_frame1(self, F):  #  Decode frame GUI
        F.destroy()
        d_f2 = Frame(window)

        title = Label(d_f2, text="Decode Data Using Steganography", font=('Times new roman', 20, 'bold'))
        title.grid(row=0, column=1, pady=20)
        title.config(bg='#e3f4f1')

        label1 = Label(d_f2, text='Enter Image with Hidden text \n(Name & Extension):')
        label1.config(font=('Times new roman', 16, 'bold'), bg='#e3f4f1')
        label1.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.img_entry = tk.Entry(d_f2, font=('Times New Roman', 16))
        self.img_entry.grid(row=1, column=1, padx=10, pady=10)

        button_bws = tk.Button(d_f2, text='Browse', command=lambda: self.browse_image())
        button_bws.config(font=('Helvetica', 14), bg='#e8c1c7')
        button_bws.grid(row=2, column=2, pady=10)
        
        key_entry_label = Label(d_f2, text="Image Key (for Decoding):", font=('Times New Roman', 16, 'bold'))
        key_entry_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.key_entry = tk.Entry(d_f2, font=('Times New Roman', 16))
        self.key_entry.grid(row=3, column=1, padx=10, pady=10)
        
        decode_button = Button(d_f2, text="Decrypt", command=lambda: self.decode_button_click(d_f2), padx=14, bg='#e3f4f1')
        decode_button.config(font=('Helvetica', 18), bg='#e8c1c7')
        decode_button.grid(row=5, column=0, pady=15)  # Use column 1

        button_back = Button(d_f2, text='Cancel', command=lambda: self.back(d_f2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(row=5, column=1, pady=15)  # Use column 1
        button_back.grid()
        d_f2.grid()

    def decode_button_click(self, d_F2):   # DECODE BUTTON CLICK FUNCTION
        e_pg = Frame(window)
        img_path = self.img_entry.get()
        img_key = self.key_entry.get()

        

        if img_path and img_key:
            try:
                img_key = int(img_key)
                self.encrypt_image_file(img_path, int(img_key))
          
            except ValueError:
                messagebox.showinfo("Error", "Image Key must be an integer.")
            image = Image.open(img_path, 'r')
            decoded_data = self.decode(image)
            messagebox.showinfo("Decoded Word", f"Decoded word: {decoded_data}")
        else:
            messagebox.showinfo("Error", "All fields are required!")

        e_pg.destroy()


    def back(self, frame): # BACK BUTTON
       frame.destroy()
       frame.pack_forget()  # Hide the current frame
       self.main()  # Bring back the main window

# Initialize the GUI
window = Tk()
stegno = IMG_Stegno(window)  # Pass the window instance as an argument
stegno.main()
window.mainloop()
