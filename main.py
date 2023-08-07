import json
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle

BG = "white"


# PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = []
    password_list.extend(password_letter)
    password_list.extend(password_number)
    password_list.extend(password_symbol)

    shuffle(password_list)

    password = "".join(password_list)

    window.clipboard_clear()
    window.clipboard_append(password)
    password_txt.delete(0, END)
    password_txt.insert(0, password)


# SAVE PASSWORD
def save_password():
    new_data = {
        website_txt.get().title(): {
            "email": username_txt.get(),
            "password": password_txt.get()
        }}
    if website_txt.get() == "" or username_txt.get() == "" or password_txt.get() == "":
        messagebox.showerror("Oops", "Please fill the field.")
    else:
        try:
            with open("data.json") as data_dict:
                data = json.load(data_dict)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            messagebox.showinfo("Success!", "Your detail successfully stored")
            website_txt.delete(0, END)
            password_txt.delete(0, END)
            website_txt.focus()


# SEARCH
def search_detail():
    website = website_txt.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
        emails = data[website]["email"]
        passwords = data[website]["password"]
    except FileNotFoundError:
        messagebox.showerror("Error", f"There is no data found")
    except KeyError:
        messagebox.showerror("Error", f"There is no such {website} website on your data")
    else:
        if messagebox.askyesno("Details", f"Email : {emails}\nPassword : {passwords}"):
            window.clipboard_clear()
            window.clipboard_append(passwords)


# UI SETUP
window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40, bg=BG)

# canvas
canva = Canvas(width=200, height=200, bg=BG, highlightthickness=0)
img = PhotoImage(file="logo.png")
canva.create_image(100, 100, image=img)
canva.grid(row=0, columnspan=3)

# label
Label(text="Website: ", font=("Arel", 15, "normal"), bg=BG).grid(row=1, column=0, pady=10)
Label(text="Email/Username: ", font=("Arel", 15, "normal"), bg=BG).grid(row=2, column=0, pady=10)
Label(text="Password: ", font=("Arel", 15, "normal"), bg=BG).grid(row=3, column=0, pady=10)

# Entry
website_txt = Entry(font=("Arel", 14, "normal"), bg="#fefefe", selectbackground="#eeeeee")
website_txt.grid(row=1, column=1)
website_txt.focus()

username_txt = Entry(font=("Arel", 14, "normal"), width=38, bg="#fefefe")
username_txt.grid(row=2, column=1, columnspan=2)
username_txt.insert(0, "karthirs602@gmail.com")

password_txt = Entry(font=("Arel", 14, "normal"), bg="#fefefe")
password_txt.grid(row=3, column=1)

# button
Button(text="Generate Password", font=("Poppies", 13, "normal"), width=18, command=generate_password,
       highlightthickness=0,
       activebackground="blue",
       bd=0.5).grid(row=3, column=2, padx=10)

Button(text="Add", font=("Poppies", 13, "normal"), command=save_password, width=46, highlightthickness=0,
       activebackground="blue",
       bd=0.5).grid(row=4, column=1, columnspan=2, padx=10)

Button(text="Search", font=("Poppies", 13, "normal"), width=18, command=search_detail, highlightthickness=0,
       activebackground="blue",
       bd=0.5).grid(row=1, column=2, padx=10)
window.mainloop()
