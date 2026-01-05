import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bdbarber import DataBase

class WindowManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Barbearia Login")
        self.geometry("500x600")
        self.db = DataBase("clientes.txt")
        
        self.configure(bg="#f0f0f0")

        self.container = tk.Frame(self, bg="#f0f0f0")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.frames = {}
        for F in (LoginWindow, CreateAccountWindow, MainWindow):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginWindow")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() 

class LoginWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        tk.Label(self, text="Login", font=("Arial", 22, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        tk.Label(self, text="Email:", bg="#f0f0f0").pack()
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Senha:", bg="#f0f0f0").pack()
        self.pass_entry = tk.Entry(self, show="#", font=("Arial", 12))
        self.pass_entry.pack(pady=5)


        tk.Button(self, text="Entrar", width=20, bg="#00ff62", fg="white", 
                  command=self.login_btn).pack(pady=20)
        
        tk.Button(self, text="Não tem uma conta? Crie agora", relief="flat", bg="#2196F3", fg="white",
                  command=lambda: controller.show_frame("CreateAccountWindow")).pack()

    def login_btn(self):
        email = self.email_entry.get()
        senha = self.pass_entry.get()
        if self.controller.db.validate(email, senha):
            self.controller.current_user_email = email
            self.controller.frames["MainWindow"].update_info(email)
            self.controller.show_frame("MainWindow")
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")

class CreateAccountWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        self.config(bg="#f0f0f0")
        tk.Label(self, text="Crie uma conta", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        fields = [
            ("Nome:", "name_entry", False),
            ("Email:", "email_entry", False),
            ("Senha:", "pass_entry", True)
        ]

        
        for label_text, var_name, is_password in fields:
            tk.Label(self, text=label_text, bg="#f0f0f0").pack()
            
            
            entry = tk.Entry(self, show="#" if is_password else "")
            entry.pack(pady=5)
            setattr(self, var_name, entry)

    
        tk.Label(self, text="Gênero:", bg="#f0f0f0").pack()
        self.gender_combobox = ttk.Combobox(self, values=["Masculino", "Feminino", "Outro"], state="readonly")
        self.gender_combobox.current(0)
        self.gender_combobox.pack(pady=5)
        
   

        tk.Button(self, text="Confirmar", width=20, bg="#2196F3", fg="white", 
                  command=self.submit).pack(pady=10)
        
        tk.Button(self, text="Voltar para Login", relief="flat", bg="#00ff62",
                  command=lambda: controller.show_frame("LoginWindow")).pack()

    def submit(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.pass_entry.get()
        gender = self.gender_combobox.get()

        if name and email and password:
            res = self.controller.db.add_user(email, password, name, gender)
            if res == 1:
                messagebox.showinfo("Sucesso", "Conta criada!")
                self.controller.show_frame("LoginWindow")
            else:
                messagebox.showerror("Erro", "Email já existe!")
        else:
            messagebox.showwarning("Erro", "Preencha tudo!")


class MainWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        self.lbl_msg = tk.Label(self, text="Bem vindo(a) de volta!", font=("Arial", 16), bg="#fbff00")
        self.lbl_msg.pack(pady=20)

        self.lbl_email = tk.Label(self, text="Email: ", font=("Arial", 12), bg="#f0f0f0")
        self.lbl_email.pack(pady=10)

        tk.Button(self, text="Sair", width=15, command=lambda: controller.show_frame("LoginWindow")).pack(pady=30)

    def update_info(self, email):
        self.lbl_email.config(text=f"EMAIL: {email}")

if __name__ == "__main__":
    app = WindowManager()
    app.mainloop()

