import tkinter as tk
from database import Database
from tkinterUtils import Field
import re
from tkinter import messagebox
import hashlib


def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)


class RegisterScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.config(bg="#3f0073")
        self.root.title("Registration")

        self.titleField = Field(50, 50, 500, 50, "Enter your details")
        self.FNameField = Field(50, 125, 225, 50, "Enter your First Name")
        self.LNameField = Field(50, 200, 225, 50, "Enter your Last Name")
        self.EmailField = Field(50, 275, 225, 50, "Enter your Email")
        self.PasswordField = Field(50, 350, 225, 50, "Enter your Password")
        self.PasswordField2 = Field(50, 425, 225, 50, "Re-Enter your Password")

        self.titleField.createLabel(self.root)
        self.FNameField.createField(self.root)
        self.LNameField.createField(self.root)
        self.EmailField.createField(self.root)
        self.PasswordField.createField(self.root)
        self.PasswordField2.createField(self.root)

        submitButton = tk.Button(self.root, width=50, text="Submit", command=self.submitReg)
        submitButton.place(x=175, y=550, width=250, height=50)

        self.root.mainloop()

    def submitReg(self):
        FName = self.FNameField.getEntry().get()
        LName = self.LNameField.getEntry().get()
        email = self.EmailField.getEntry().get().lower()
        password = self.PasswordField.getEntry().get()
        password2 = self.PasswordField2.getEntry().get()
        if not (FName and LName and email and password and password2):
            messagebox.showinfo("Status", "All fields must be filled out")
            return False
        domain = "@sherborne.org"
        if domain not in email:
            messagebox.showinfo("Email status", "Email must be a Sherborne School email")
            return False
        if password == password2:
            if not validate_password(password):
                messagebox.showinfo("Password status", "Password must be 8+ characters, with uppercase and lowercase")
                return False
            salt = "5gz"

            # Adding salt at the last of the password
            dataBase_password = password + salt
            # Encoding the password
            hashed = hashlib.sha256(dataBase_password.encode())
            data = [FName, LName, email, hashed.hexdigest()]

            db = Database("Evolution")
            sql1 = f"SELECT Email FROM User WHERE email=?"
            records = db.cur.execute(sql1, (email,)).fetchall()
            db.conn.commit()
            if len(records) == 0:
                sql2 = """INSERT INTO User(FName, LName, Email, Password) VALUES(?, ?, ?, ?)"""
                db.cur.execute(sql2, data)
                db.conn.commit()
                print("Entry Submitted")
                self.root.destroy()
                return True
            else:
                messagebox.showinfo("Status", "Submitted email already exists, try logging in.")
                return False
        else:
            noMatchText = tk.Label(self.root, bg="#3f0073", fg="red", height=50, text="Passwords do not match",
                                   font=("Helvetica", "16"))
            noMatchText.place(x=175, y=500, width=250, height=50)
            print("Passwords do not match")
            return False

if __name__ == "__main__":
    RegisterScreen()