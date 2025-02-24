import tkinter as tk
from database import Database
from tkinterUtils import Field
import hashlib
import instructionScreen




class LoginScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.config(bg="#3f0073")
        self.root.title("Login")
    
        titleField = Field(50, 50, 500, 50, "Login with your details")
        self.EmailField = Field(50, 125, 225, 50, "Enter your Email")
        self.PasswordField = Field(50, 200, 225, 50, "Enter your Password")
    
        titleField.createLabel(self.root)
        self.EmailField.createField(self.root)
        self.PasswordField.createField(self.root)
    
        submitButton = tk.Button(self.root, width=50, text="Submit", command=self.submitLogin)
        submitButton.place(x=175, y=300, width=250, height=50)
    
        self.root.mainloop()

    def submitLogin(self):
        email = self.EmailField.getEntry().get().lower()
        password = self.PasswordField.getEntry().get()
        salt = "5gz"

        # Adding salt at the last of the password
        dataBase_password = password + salt
        # Encoding the password
        hashed = hashlib.sha256(dataBase_password.encode())
        hashedPassword = hashed.hexdigest()
        db = Database("Evolution")

        # print(email, password)

        sql = f"SELECT UserID, Email, Password FROM User WHERE email=?"
        records = db.cur.execute(sql, (email,)).fetchall()
        db.conn.commit()
        print("1:", records)
        if len(records) == 0:
            noRecordsText = tk.Label(self.root, bg="#3f0073", fg="red", height=50,
                                     text="Email address not found. Have you registered?",
                                     font=("Helvetica", "16"))
            noRecordsText.place(x=50, y=275, width=500, height=50)
            noRecordsText.after(1000, noRecordsText.destroy)
            return False
        for record in records:
            if hashedPassword == record[-1]:
                print("Found")
                print(record)
                userID = record[0]
                self.root.destroy()
                self.goToInstructions(userID)

                return True
        print("Not Found")
        noMatchText = tk.Label(self.root, bg="#3f0073", fg="red", height=50, text="Email and Password do not match",
                               font=("Helvetica", "16"))
        noMatchText.place(x=50, y=275, width=500, height=50)
        noMatchText.after(1000, noMatchText.destroy)
        print("Passwords do not match")
        return False

    def goToInstructions(self, userID):
        instructionScreen.InstructionScreen(userID)
    

if __name__ == "__main__":
    LoginScreen()
