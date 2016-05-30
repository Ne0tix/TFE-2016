from tkinter import *
from tkinter.messagebox import *
import sqlite3
import os.path
import TFE

dirBase = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(dirBase, "DataBase/UserData.db3")

class dropDown(object):
    def __init__(self, screen):
        self.screen = screen
        menu = Menu(self.screen)
        
        # Sous Menu Fichier
        fileMenu = Menu(MMmenu, tearoff=0)
        fileMenu.add_command(label="Main Menu", command= lambda: self.goToMainMenu())
        fileMenu.add_command(label="User Menu", command= lambda: self.goToUserMenu())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command= lambda: self.exit())
        
        menu.add_cascade(label="File", menu=fileMenu)
        
        # Sous Menu Edit
        editMenu = Menu(menu, tearoff=0)
        editMenu.add_command(label="Add User", command= lambda: self.goToAddUser())
        editMenu.add_command(label="Connection", command= lambda: self.goToConnection())
                
        menu.add_cascade(label="Edit", menu=editMenu)
        
        # Sous Menu About
        aboutMenu = Menu(menu, tearoff=0)
        aboutMenu.add_command(label="Ecole", command= lambda: self.goToEcole())
        aboutMenu.add_command(label="Createur", command= lambda: self.goToCreateur())
        
        menu.add_cascade(label="About", menu=aboutMenu)
        
        # Ajout a la fenetre
        screen.config(menu=menu)
    def childFrameDestroy(self):
        for child in self.screen.winfo_children():
            child.destroy()
        
    def goToMainMenu(self):
        self.childFrameDestroy()
        self.mainMenu = mainMenu(self.screen)
    
    def goToUserMenu(self):
        self.childFrameDestroy()
        self.userMenu = userMenu(self.screen)
            
    def goToGameMenu(self, userName):
        self.childFrameDestroy()
        self.gameMenu = gameMenu(self.screen, userName)
        
    def exit(self):
        self.screen.quit()
        self.screen.destroy()
    
    def goToAddUser(self):
        self.childFrameDestroy()        
        self.addUser = addUser(self.screen)
        self.backButton = Button(self.screen, text="Back", command= lambda: self.goToMainMenu())
        self.backButton.grid()
    
    def goToConnection(self):
        self.childFrameDestroy()        
        self.userConnection = userConnection(self.screen)
        self.backButton = Button(self.screen, text="Back", command= lambda: self.goToMainMenu())
        self.backButton.grid()
    
    def goToLoadSave(self, userName):
        self.childFrameDestroy()
        self.loadSave = loadSave(self.screen, userName)
        
    def goToEcole(self):
        pass
    
    def goToCreateur(self):
        pass
   
class mainMenu(dropDown):

    def __init__(self, screen):
        dropDown.__init__(self, screen)
        
        self.mainMenuFrame = Frame(screen, height="1024", width="640")
        self.mainMenuFrame.grid()
        # Titre
        self.labelMainTitle = Label(self.mainMenuFrame, text="Empires Of Wind")
        self.labelMainTitle.grid(row=0, column=0)
        
        # Bouton vers la fenetre user
        self.buttonSinglePlayer = Button(self.mainMenuFrame, text="Single Player", command= lambda: self.goToUserMenu())
        self.buttonSinglePlayer.grid(row=1, column=0)
        
        # Bouton pour sortir du jeu
        self.buttonExitGame = Button(self.mainMenuFrame, text="Exit Game", command= lambda: self.exit())
        self.buttonExitGame.grid(row=2, column=0)
        
class addUser(dropDown):
    def __init__(self, screen):           
        dropDown.__init__(self, screen)
        
        self.addUserFrame = LabelFrame(screen, text="Add User")
        self.addUserFrame.grid()

        self.userNameLabel = Label(self.addUserFrame, text="User Name:")
        self.userNameLabel.grid()
        
        self.userNameEntry = Entry(self.addUserFrame)
        self.userNameEntry.grid()
        
        self.userPasswordLabel = Label(self.addUserFrame, text="User Password:")
        self.userPasswordLabel.grid()
        
        self.userPasswordEntry = Entry(self.addUserFrame, show="*")
        self.userPasswordEntry.grid()
        
        self.userPasswordConfirmationLabel = Label(self.addUserFrame, text="User Password Confirmation:")
        self.userPasswordConfirmationLabel.grid()
        
        self.userPasswordConfirmationEntry = Entry(self.addUserFrame, show="*")
        self.userPasswordConfirmationEntry.grid()
        
        self.userValidationButton = Button(self.addUserFrame, text="Validate", command= lambda: self.userValidation())
        self.userValidationButton.grid()
        
    def userValidation(self):
        self.userName = self.userNameEntry.get()
        self.userPassword = self.userPasswordEntry.get()
        self.userPasswordConfirmation = self.userPasswordConfirmationEntry.get()
        self.userErrorList = ""
        
        if self.userName == "":
            self.userErrorList += "\n User name is empty !"
        if self.userPassword == "":
            self.userErrorList += "\n Password is empty !"
        if self.userPasswordConfirmation == "":
            self.userErrorList += "\nPassword confirmation is empty !"
            
        if self.userErrorList == "":
            if self.userPassword != self.userPasswordConfirmation:
                self.userErrorList += "\nPasswords doesn\'t match"
            if self.userName.find(" ") != -1:
                self.userErrorList += "\nNo space in user name"   
            if self.userPassword.find(" ") != -1:
                self.userErrorList += "\nNo space in user password"
        
        if self.userErrorList != "":
            showerror("Add User Error", self.userErrorList)
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT User from User where Name = ?", (self.userName,))
            self.user = c.fetchone()
            if self.user != None:
                showerror("Add User Error", "User name exist")
            else:
                c.execute("INSERT INTO User (Name, Password) VALUES (?,?);", (self.userName, self.userPassword))
                showinfo("Add User", "New user added")

            conn.commit()
            
            c.close()
            

class userConnection(dropDown):
    def __init__(self, screen):        
        dropDown.__init__(self, screen)
        
        self.userConnectionFrame = LabelFrame(screen, text="User connection")
        self.userConnectionFrame.grid()
        
        self.connectionNameLabel = Label(self.userConnectionFrame, text="User name:")
        self.connectionNameLabel.grid()
        
        self.connectionNameEntry = Entry(self.userConnectionFrame)
        self.connectionNameEntry.grid()
        
        self.connectionPasswordLabel = Label(self.userConnectionFrame, text="User password:")
        self.connectionPasswordLabel.grid()
        
        self.connectionPasswordEntry = Entry(self.userConnectionFrame, show="*")
        self.connectionPasswordEntry.grid()
        
        self.connectionButton = Button(self.userConnectionFrame, text="Connection", command= lambda: self.connection())
        self.connectionButton.grid()
        
    def connection(self):
        self.connectionName = self.connectionNameEntry.get()
        self.connectionPassword = self.connectionPasswordEntry.get()
        
        self.connectionErrorList = ""
        
        if self.connectionName == "":
            self.connectionErrorList += "\n User name is empty !"
        if self.connectionPassword == "":
            self.connectionErrorList += "\n Password is empty !"
                        
        if self.connectionErrorList == "":
            if self.connectionName.find(" ") != -1:
                self.connectionErrorList += "\nNo space in user name"   
            if self.connectionPassword.find(" ") != -1:
                self.connectionErrorList += "\nNo space in user password"
        
        if self.connectionErrorList != "":
            showerror("Connection Error", self.connectionErrorList)
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT Password from User where Name = ?", (self.connectionName,))
            self.userPasswordVerif = c.fetchone()
            conn.commit()
            
            c.close()
            if self.userPasswordVerif == None:
                showerror("Error connection", "Unknown user name !")
            else:
                if self.userPasswordVerif[0] != self.connectionPassword:
                    showerror("Error connection", "Wrong password !")
                else:
                    self.goToGameMenu(self.connectionName)
        

class userMenu(addUser, userConnection):
    def __init__(self, screen):
        addUser.__init__(self, screen)
        userConnection.__init__(self, screen)
        self.userMenuBackButton = Button(screen, text="Back", command= lambda: self.goToMainMenu())
        self.userMenuBackButton.grid()                

class gameMenu(dropDown):
    def __init__(self, screen, userName):
        dropDown.__init__(self, screen)
        self.userName = userName
        
        self.gameMenuFrame = LabelFrame(screen, text="Game")
        self.gameMenuFrame.grid()
        
        self.newGameButton = Button(self.gameMenuFrame, text="New Game", command= lambda: self.newGame())
        self.newGameButton.grid()
        
        self.loadGameButton = Button(self.gameMenuFrame, text="Load Game", command= lambda: self.goToLoadSave(self.userName))
        self.loadGameButton.grid()
        
        self.gameMenuBackButton = Button(self.gameMenuFrame, text="Back", command= lambda: self.goToUserMenu())
        self.gameMenuBackButton.grid()
        
    def newGame(self):
        self.screen.destroy()
        TFE.main(self.userName, False)

class loadSave(dropDown):
    def __init__(self, screen, userName):
        dropDown.__init__(self, screen)
        
        self.userName = userName
        
        self.loadSaveFrame = LabelFrame(screen, text="Load Save")
        self.loadSaveFrame.grid()
        
        self.saveListBox = Listbox(self.loadSaveFrame)
        
        conn = sqlite3.connect("DataBase/UserData.db3")
        c = conn.cursor()
        
        c.execute("SELECT Save from UserSave where UserID = (select ID from User where Name = (?))", ( self.userName,))
        for raw in c:
            self.saveListBox.insert(END, raw)
        conn.commit()
        c.close()
        
        self.saveListBox.grid()
        
        self.loadButton = Button(self.loadSaveFrame, text="Load", command= lambda: self.loadSaveGame(self.saveListBox.get(ACTIVE)))
        self.loadButton.grid()
        
        self.backButton = Button(self.loadSaveFrame, text="Back", command= lambda: self.goToGameMenu())
        self.backButton.grid()
        
    def loadSaveGame(self, save):
        self.screen.destroy()
        TFE.main(self.userName, True, save)
        
if __name__ == "__main__":
    master = Tk()
    menu = mainMenu(master)
    master.mainloop()
