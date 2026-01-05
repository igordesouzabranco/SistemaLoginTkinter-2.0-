import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                
                    dados = line.strip().split(";")
                    if len(dados) == 5:
                        email, password, name, genero, created = dados
                        self.users[email] = (password, name, genero, created)
        except FileNotFoundError:
            
            open(self.filename, "w").close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    

    def validate(self, email, password):
        if email in self.users:
            return self.users[email][0] == password
        return False

    def add_user(self, email, password, name, genero):
        email = email.strip()
        if email not in self.users:
            date = DataBase.get_date()
            self.users[email] = (password.strip(), name.strip(), genero.strip(), date)
            self.save() 
            return 1
        return -1

    def save(self):
        with open(self.filename, "w") as f:
            for email in self.users:
                senha, nome, genero, data = self.users[email]
                f.write(f"{email};{senha};{nome};{genero};{data}\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]