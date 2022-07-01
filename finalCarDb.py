from multiprocessing.sharedctypes import Value
import pandas as pd
import time
import mysql.connector
from datetime import datetime, date
from mysql.connector.constants import ClientFlag
mydb = mysql.connector.connect(host="localhost",
user="root",
password="Cooper71401",
auth_plugin='mysql_native_password',
database="CarBids",
client_flags=[ClientFlag.LOCAL_FILES])
mycursor = mydb.cursor(buffered = True)
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
import tkinter.ttk as ttk
import tkinter.messagebox

mycursor.execute("CREATE TABLE IF NOT EXISTS Buyer (BuyerID INT AUTO_INCREMENT PRIMARY KEY, UserName VARCHAR(200), password VARCHAR(40), Dob DATE, BuyerLoc VARCHAR(30));")
mycursor.execute("CREATE TABLE IF NOT EXISTS Seller (SellerID INT AUTO_INCREMENT PRIMARY KEY, UserName VARCHAR(200), password VARCHAR(40), Dob DATE, SellerLoc VARCHAR(30));")
mycursor.execute("CREATE TABLE IF NOT EXISTS Car (year INT, make VARCHAR(20), model VARCHAR(20), trim VARCHAR(50), body VARCHAR(20), transmission VARCHAR(20), vin VARCHAR(40) PRIMARY KEY, state VARCHAR(2), conditioning DECIMAL(2,1), odometer INT, color VARCHAR(20), interior VARCHAR(20), sellerID INT, mmr INT, sellingprice INT, saledate VARCHAR(70), FOREIGN KEY (sellerID) REFERENCES Seller (SellerID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS Sale (saleID INT AUTO_INCREMENT PRIMARY KEY, vin VARCHAR(40), sellerID INT, buyerID INT, price INT, FOREIGN KEY (vin) REFERENCES Car (vin), FOREIGN KEY (sellerID) REFERENCES Seller (sellerID), FOREIGN KEY (buyerID) REFERENCES Buyer (buyerID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS Bid (bidID INT AUTO_INCREMENT PRIMARY KEY, vin VARCHAR(40), sellerID INT, buyerID INT, price INT, dateTime DATETIME, FOREIGN KEY (sellerID) REFERENCES Seller (sellerID), FOREIGN KEY (buyerID) REFERENCES Buyer (buyerID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS CreditCard (cardNum BIGINT, cardHolderName VARCHAR(200), expDate VARCHAR(20), securityCode INT, billingZip INT, buyerID INT, FOREIGN KEY (buyerID) REFERENCES Buyer (BuyerID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS dbLogs(logDate DATETIME, ent VARCHAR(20), modifiedFrom VARCHAR(1000), modifiedTo VARCHAR(1000));")
mycursor.execute("ALTER TABLE Buyer AUTO_INCREMENT = 1000000;")

# Populate the database

# sql = "INSERT INTO Car (year,make,model,trim,body,transmission,vin,state,conditioning,odometer,color,interior,sellerID,mmr,sellingprice,saledate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# vals = [
#     (2015,'Kia','Sorento','LX','SUV','automatic','5xyktca69fg566472','ca',5,16639,'white','black',1,20500,21500,'Tue Dec 16 2014 12:30:00'),
#     (2015,'Kia','Sorento','LX','SUV','automatic','5xyktca69fg561319','ca',5,9393,'white','beige',1,20800,21500,'Tue Dec 16 2014 12:30:00'),
#     (2014,'BMW','3 Series','328i SULEV','Sedan','automatic','wba3c1c51ek116351','ca',4.5,1331,'gray','black',2,31900,30000,'Thu Jan 15 2015 04:30:00'),
#     (2015,'Volvo','S60','T5','Sedan','automatic','yv1612tb4f1310987','ca',4.1,14282,'white','black',3,27500,27750,'Thu Jan 29 2015 04:30:00'),
#     (2014,'BMW','6 Series Gran Coupe','650i','Sedan','automatic','wba6b2c57ed129731','ca',4.3,2641,'gray','black',2,66000,67000,'Thu Dec 18 2014 12:30:00'),
#     (2015,'Nissan','Altima','2.5 S','Sedan','automatic','1n4al3ap1fn326013','ca',1,5554,'gray','black',4,15350,10900,'Tue Dec 30 2014 12:00:00'),
#     (2014,'BMW','M5','Base','Sedan','automatic','wbsfv9c51ed593089','ca',3.4,14943,'black','black',5,69000,65000,'Wed Dec 17 2014 12:30:00'),
#     (2014,'Chevrolet','Cruze','1LT','Sedan','automatic','1g1pc5sb2e7128460','ca',2,28617,'black','black',4,11900,9800,'Tue Dec 16 2014 13:00:00'),
#     (2014,'Audi','A4','2.0T Premium Plus quattro','Sedan','automatic','wauffafl3en030343','ca',4.2,9557,'white','black',6,32100,32250,'Thu Dec 18 2014 12:00:00'),
#     (2014,'Chevrolet','Camaro','LT','Convertible','automatic','2g1fb3d37e9218789','ca',3,4809,'red','black',7,26300,17500,'Tue Jan 20 2015 04:00:00'),
#     (2014,'Audi','A6','3.0T Prestige quattro','Sedan','automatic','wauhgafc0en062916','ca',4.8,14414,'black','black',8,47300,49750,'Tue Dec 16 2014 12:30:00'),
#     (2015,'Kia','Optima','LX','Sedan','automatic','5xxgm4a73fg353538','ca',4.8,2034,'red','tan',9,15150,17700,'Tue Dec 16 2014 12:00:00'),
#     (2015,'Ford','Fusion','SE','Sedan','automatic','3fa6p0hdxfr145753','ca',2,5559,'white','beige',4,15350,12000,'Tue Jan 13 2015 12:00:00'),
#     (2015,'Kia','Sorento','LX','SUV','automatic','5xyktca66fg561407','ca',5,14634,'silver','black',1, 20600,21500,'Tue Dec 16 2014 12:30:00'),
#     (2014,'Chevrolet','Cruze','2LT','Sedan','automatic','1g1pe5sbxe7120097','ca',3,15686,'blue','black',10,13900,10600,'Tue Dec 16 2014 12:00:00'),
#     (2015,'Nissan','Altima','2.5 S','Sedan','automatic','1n4al3ap5fc124223','ca',2,11398,'black','black',4,14750,14100,'Tue Dec 23 2014 12:00:00'),
#     (2015,'Hyundai','Sonata','SE','Sedan','automatic','5npe24af4fh001562','ca',4,8311,'red','—',11,15200,4200,'Tue Dec 16 2014 13:00:00'),
#     (2014,'Audi','Q5','2.0T Premium Plus quattro','SUV','automatic','wa1lfafpxea085074','ca',4.9,7983,'white','black',12,37100,40000,'Thu Dec 18 2014 12:30:00'),
#     (2014,'Chevrolet','Camaro','LS','Coupe','automatic','2g1fa1e39e9134494','ca',1.7,13441,'black','black',14,17750,17000,'Tue Dec 30 2014 15:00:00'),
#     (2014,'BMW','6 Series','650i','Convertible','automatic','wbayp9c53ed169260','ca',3.4,8819,'black','black',5,68000,67200,'Wed Dec 17 2014 12:30:00'),
#     (2015,'Chevrolet','Impala','LTZ','Sedan','automatic','2g1165s30f9103921','ca',1.9,14538,'silver','black',4,24300,7200,'Tue Jul 07 2015 09:30:00'),
#     (2014,'BMW','5 Series','528i','Sedan','automatic','wba5a5c51ed501631','ca',2.9,25969,'black','black',2,34200,30000,'Tue Feb 03 2015 04:30:00'),
#     (2014,'Chevrolet','Camaro','LT','Convertible','automatic','2g1fb3d31e9134662','ca',3.5,33450,'black','black',10,20100,14700,'Tue Dec 16 2014 12:00:00'),
#     (2015,'Audi','A3','1.8 TFSI Premium','Sedan','automatic','wauacgff7f1002327','ca',4.9,5826,'gray','black',12,24000,23750,'Thu Dec 18 2014 12:30:00'),
#     (2014,'BMW','6 Series','650i','Convertible','automatic','wbayp9c57ed169262','ca',3.8,10736,'black','black',5,67000,65000,'Tue Jan 06 2015 12:30:00'),
#     (2015,'Hyundai','Sonata','SE','Sedan','automatic','5npe24af4fh038482','ca',3.5,9281,'silver','gray',4,15150,8500,'Tue Dec 16 2014 13:00:00'),
#     (2015,'Volvo','XC70','T6','Wagon','automatic','yv4902nb3f1198103','ca',4.2,16506,'brown','brown',3,32100,32500,'Thu Feb 26 2015 04:30:00'),
#     (2015,'Volvo','XC70','T6','Wagon','automatic','yv4902nb3f1196951','ca',4.8,12725,'beige','beige',3,32300,32500,'Thu Feb 12 2015 04:30:00'),
#     (2014,'BMW','X5','sDrive35i','SUV','automatic','5uxkr2c52e0h33130','ca',4.5,11278,'gray','black',10,50400,34000,'Tue Dec 16 2014 13:00:00'),
#     (2014,'Chevrolet','Camaro','LT','Coupe','automatic','2g1fb1e35e9238302','ca',4.2,11874,'gray','black',13,22200,19500,'Thu Dec 18 2014 12:00:00')]
#
# mycursor.executemany(sql, vals)

# sqlS = "INSERT INTO Seller (UserName, password, Dob, SellerLoc) VALUES(%s,%s,%s,%s)"
# valsS = [('kia motors america, inc', 'kia', '2000-12-01', 'Orange, CA'),
# ('financial services remarketing (lease)', 'financial', '1999-12-01', 'Houston, TX'),
# ('volvo na rep/world omni', 'volvo', '1998-12-01', 'Boise, ID'),
# ('enterprise vehicle exchange / tra / rental / tulsa', 'enterprise', '1997-12-01', 'Tulsa, OK'),
# ('the hertz corporation', 'hertz', '1996-12-01', 'San Jose, CA'),
# ('audi mission viejo', 'audi', '1995-12-01', 'Mission Viejo, CA'),
# ('d/m auto sales inc', 'd/m', '1994-12-01', 'Laguna, CA'),
# ('desert auto trade', 'desert', '1993-12-01', 'Death Valley, CA'),
# ('kia motors finance', 'kia finance', '1992-12-01', 'San Antonio, TX'),
# ('avis rac/san leandro', 'leonardo', '1991-12-01', 'San Leonardo, CA'),
# ('avis tra', 'avis', '1990-12-01', 'Paris, CA'),
# ('audi north scottsdale', 'audi scott', '1989-12-01', 'Scottsdale, AZ'),
# ('midway hfc fleet/ars', 'midway', '1988-12-01', 'Encino, CA'),
# ('wells fargo dealer services', 'wells fargo', '1987-12-01', 'Newhall, CA')]
# mycursor.executemany(sqlS, valsS)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, NewUser, LogIn, Buyer, Seller, S1, S2, S3, S4, B5, B6, B7, B8, B9, S15, B16, Exists, Cards, Export, Commit): # ,Error
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Welcome to UsedCars.com",
        )
        self.title.pack(pady="50", side="top")
        button1 = tk.Button(self, text="Sign Up",
                            command=lambda: controller.show_frame("NewUser"))
        button2 = tk.Button(self, text="Log In",
                            command=lambda: controller.show_frame("LogIn"))
        button1.pack(side="top")
        button2.pack(side="top")

# Used when a new user wants to create an account
class NewUser(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas5 = tk.Canvas(self)
        self.canvas5.configure(background="#f3a3bf", height="400", width="400")
        self.canvas5.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label5 = ttk.Label(self)
        self.label5.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )
        self.label5.configure(text="New User Sign Up")
        self.label5.pack(pady="50", side="top")
        __tkvar = tk.StringVar(value="Select User Type")
        __values = ["Buyer", "Seller"]
        optionmenu2 = tk.OptionMenu(
            self, __tkvar, "Select User Type", *__values
        )
        optionmenu2.pack(side="top")
        entry11 = ttk.Entry(self)
        entry11.configure(justify="center")
        _text_ = """username"""
        entry11.delete("0", "end")
        entry11.insert("0", _text_)
        entry11.pack(pady="10", side="top")
        entry12 = ttk.Entry(self)
        entry12.configure(justify="center")
        _text_ = """password"""
        entry12.delete("0", "end")
        entry12.insert("0", _text_)
        entry12.pack(side="top")
        entry13 = ttk.Entry(self)
        entry13.configure(justify="center")
        _text_ = """date of birth (YYYY-MM-DD)"""
        entry13.delete("0", "end")
        entry13.insert("0", _text_)
        entry13.pack(pady="10", side="top")
        entry14 = ttk.Entry(self)
        entry14.configure(justify="center")
        _text_ = """location"""
        entry14.delete("0", "end")
        entry14.insert("0", _text_)
        entry14.pack(pady="10", side="top")

        #takes the user to the menu page according to their buyer or seller identity
        def nexts():
            choice = __tkvar.get()
            if choice == "Buyer":
                return "Buyer"
            elif choice == "Seller":
                return "Seller"
        #called when the "Create Account" button is clicked by the user
        def load():
            choice = __tkvar.get()
            user = entry11.get()
            # check if the new buyer or seller username already exists
            if choice == "Buyer":
                checkname = "SELECT * FROM Buyer WHERE UserName= %s "
            else:
                checkname = "SELECT * FROM Seller WHERE UserName= %s "
            users = (user,)
            mycursor.execute(checkname, users)
            if mycursor.rowcount != 0:
                tkinter.messagebox.showinfo('title',  "UserName already taken. Please enter another one!")
                return "NewUser"
            passw = entry12.get()
            #check if the new buyer or seller password already exists
            if choice == "Buyer":
                checkpass = "SELECT * FROM Buyer WHERE password= %s "
            else:
                checkpass = "SELECT * FROM Seller WHERE password= %s "
            passwo = (passw,)
            mycursor.execute(checkpass, passwo)
            if mycursor.rowcount != 0:
                tkinter.messagebox.showinfo('title',  "Password already taken. Please enter another one!")
                return "NewUser"
            dob= entry13.get()
            loc= entry14.get()
            #create the user
            if choice == "Buyer":
                mycursor.execute("INSERT INTO Buyer (UserName, password, Dob, BuyerLoc) VALUES (%s,%s,%s,%s);",(user,passw,dob,loc))
                mydb.commit()
                mycursor.execute("SELECT BuyerID from Buyer ORDER BY BuyerID DESC LIMIT 1;")
                myresult = mycursor.fetchall()
                texts = "Your id is : " + str(myresult[0][0])
                e=tk.Label(self, text=texts, justify = "center", bg ="#f6fa93")
                e.pack(pady="10", side="top")
                tkinter.messagebox.showinfo('title',  'Account created! Click "Next" to proceed. Record your ID, you will need it for each task you perform.')
                return "NewUser"
            else:
                mycursor.execute("INSERT INTO Seller (UserName, password, Dob, SellerLoc) VALUES (%s,%s,%s,%s);",(user,passw,dob,loc))
                mydb.commit()
                mycursor.execute("SELECT SellerID from Seller ORDER BY SellerID DESC LIMIT 1;")
                myresult = mycursor.fetchall()
                texts = "Your id is : " + str(myresult[0][0])
                e=tk.Label(self, text=texts, justify = "center", bg ="#f6fa93")
                e.pack(pady="10", side="top")
                tkinter.messagebox.showinfo('title',  'Account created! Click "Next" to proceed. Record your ID, you will need it for each task you perform.')
                return "NewUser"
        self.button15 = ttk.Button(self)
        self.button15.configure(text="Create Account", command=lambda: controller.show_frame(load()))
        self.button15.pack(side="top")
        self.button17 = ttk.Button(self)
        self.button17.configure(text="Next", command=lambda: controller.show_frame(nexts()))
        self.button17.pack(side="top")
        self.button16 = ttk.Button(self)
        self.button16.configure(text="Back", command=lambda: controller.show_frame("StartPage"))
        self.button16.pack(side="top")

#Used when an existing user logs in to their account
class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas6 = tk.Canvas(self)
        self.canvas6.configure(background="#f3a3bf", height="400", width="400")
        self.canvas6.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label6 = ttk.Label(self)
        self.label6.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )
        self.label6.configure(text="User Login")
        self.label6.pack(pady="50", side="top")
        entry14 = ttk.Entry(self)
        entry14.configure(justify="center")
        _text_ = """username"""
        entry14.delete("0", "end")
        entry14.insert("0", _text_)
        entry14.pack(pady="10", side="top")
        entry15 = ttk.Entry(self)
        entry15.configure(justify="center")
        _text_ = """password"""
        entry15.delete("0", "end")
        entry15.insert("0", _text_)
        entry15.pack(side="top")

        #called when the "Enter" button is clicked by the user, takes the user to the appropriate menu selection page
        def load():
            user = entry14.get()
            passw = entry15.get()
            mycursor.execute("SELECT BuyerID from Buyer WHERE UserName = %s AND password = %s UNION SELECT SellerID from Seller WHERE UserName = %s AND password = %s",(user, passw, user, passw))
            #checks that the user entered their log in correctly
            if mycursor.rowcount ==0:
                tkinter.messagebox.showinfo('No user found.',  "Incorrect username or password. Please try again.")
                return "LogIn"
            myresult = mycursor.fetchall()
            if myresult[0][0] >= 1000000:
                return "Buyer"
            elif myresult[0][0] < 1000000:
                return "Seller"
        self.button18 = ttk.Button(self)
        self.button18.configure(text="Enter", command=lambda: controller.show_frame(load()))
        self.button18.pack(pady="10", side="top")
        self.button19 = ttk.Button(self)
        self.button19.configure(text="Back", command=lambda: controller.show_frame("StartPage"))
        self.button19.pack(pady="10", side="top")

#Used when a buyer logs in to the system and provides menu options specific to the role of the buyer
class Buyer(tk.Frame):
    def __init__(self, parent, controller):

        def trans_option(choice):
            choice = self.__tkvar.get()
            if choice == "Shop Cars":
                controller.show_frame("B5")
            elif choice == "Make a bid":
                controller.show_frame("B6")
            elif choice == "View your bids":
                controller.show_frame("B7")
            elif choice == "Update your bids":
                controller.show_frame("B8")
            elif choice == "Cancel your bid":
                controller.show_frame("B9")
            elif choice == "View number of bids you have made on each car":
                controller.show_frame("B16")
            elif choice == "Export data":
                controller.show_frame("Export")
            elif choice == "Logout":
                controller.show_frame("StartPage")

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Buyer Options",
        )
        self.title.pack(pady="50", side="top")
        self.__tkvar = tk.StringVar(value="Select your option")
        __values = [
            "Shop Cars",
            "Make a bid",
            "View your bids",
            "Update your bids",
            "Cancel your bid",
            "Export data",
            "View number of bids you have made on each car",
            "Logout",
        ]
        self.optionmenu5 = tk.OptionMenu(
            self, self.__tkvar, "Select your option", *__values, command=trans_option
        )
        self.optionmenu5.pack(side="top")
        self.button20 = ttk.Button(self)
        self.button20.configure(text="Back", command=lambda: controller.show_frame("StartPage"))
        self.button20.pack(pady="10", side="top")

#Used when a seller logs in to the system and provides menu options specific to the seller
class Seller(tk.Frame):
    def __init__(self, parent, controller):
        def trans_option(choice):
            choice = self.__tkvar.get()
            if choice == "Show all of your cars currently on market":
                controller.show_frame("S1")
            elif choice == "Add a new car to market":
                controller.show_frame("S2")
            elif choice == "View all bids on certain car" :
                controller.show_frame("S3")
            elif choice == "Take a car off of the market" :
                controller.show_frame("S4")
            elif choice == "View average bid price of each of your cars":
                controller.show_frame("S15")
            elif choice == "Logout":
                controller.show_frame("StartPage")
            elif choice == "Export data":
                controller.show_frame("Export")

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Seller Options",
        )
        self.title.pack(pady="50", side="top")
        self.__tkvar = tk.StringVar(value="Select your option")
        __values = [
            "Show all of your cars currently on market",
            "Add a new car to market",
            "View all bids on certain car",
            "Take a car off of the market",
            "Export data",
            "View average bid price of each of your cars",
            "Logout"
        ]
        self.optionmenu6 = tk.OptionMenu(
            self, self.__tkvar, "Select your option", *__values, command=trans_option
        )
        self.optionmenu6.pack(side="top")
        self.button21 = ttk.Button(self)
        self.button21.configure(text="Back", command=lambda: controller.show_frame("StartPage"))
        self.button21.pack(pady="10", side="top")

#seller option 1: "Show all of your cars currently on the market"
class S1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Cars",
        )

        #called when the "Enter" button is chosen by the user, populates the grid
        def populate():
            try:
                id = int(entry11.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "S1"
            mycursor.execute("SELECT * FROM Car WHERE SellerID = %s", (id,))
            mydb.commit()
            r_set = mycursor.fetchall()
            i=3
            for bid in r_set:
                for j in range(len(bid)):
                    w = 10
                    if j == 3 or j == 6 or j == 15:
                        w=20
                    if j == 0 or j == 7 or j == 8 or j == 12:
                        w=5
                    if j == 6:
                        e = tk.Button(self, width= w, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                        e.grid(row=i, column=j)
                    else:
                        e = tk.Label(self, width= w, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                        e.grid(row=i, column=j)
                i=i+1

        self.title.grid(row=0, column=3)
        entry11 = ttk.Entry(self)
        entry11.configure(justify="center")
        _text_ = """enter id"""
        entry11.delete("0", "end")
        entry11.insert("0", _text_)
        entry11.grid(row = 1, column = 2)
        button21 = ttk.Button(self)
        button21.configure(text="Enter", command=lambda: populate())
        button21.grid(row =1, column = 4)
        button19 = ttk.Button(self)
        button19.configure(text="Back", command=lambda: controller.show_frame("Seller"))
        button19.grid(row=1,column=5)

        #creates the grid to display a table of cars on the market, owned by the current seller
        e=tk.Label(self,width=5,text='Year',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=0)
        e=tk.Label(self,width=10,text='Make',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=1)
        e=tk.Label(self,width=10,text='Model',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=2)
        e=tk.Label(self,width=20,text='Trim',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=3)
        e=tk.Label(self,width=10,text='Body',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=4)
        e=tk.Label(self,width=10,text='Transmission',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=5)
        e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=6)
        e=tk.Label(self,width=5,text='State',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=7)
        e=tk.Label(self,width=5,text='Condition',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=8)
        e=tk.Label(self,width=10,text='Odometer',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=9)
        e=tk.Label(self,width=10,text='Color',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=10)
        e=tk.Label(self,width=10,text='Interior',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=11)
        e=tk.Label(self,width=5,text='SellerId',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=12)
        e=tk.Label(self,width=10,text='mmr',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=13)
        e=tk.Label(self,width=10,text='Sale Price',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=14)
        e=tk.Label(self,width=20,text='Sale Date',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=15)

#Seller option 2: "Add a new car to the market"
class S2(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        #called when the "Enter" button is selected by the user, handles error checking for the information entered for the current car
        def load():
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "S2"
            try:
                y= int(entry4.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a valid calendar year.")
                return "S2"
            mk = entry5.get()
            mdl = entry6.get()
            trm = entry7.get()
            bdy = entry8.get()
            tran = entry9.get()
            vin = entry10.get()
            st = entry16.get()
            try:
                cndt = float(entry17.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a condition rating in the form of a decimal.")
                return ("S2")
            try:
                odo = int(entry18.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a whole number for the odometer reading.")
                return ("S2")
            clr = entry19.get()
            inte = entry20.get()
            try:
                mmr = int(entry21.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a valid whole number for the mmr value.")
                return ("S2")
            try:
                sp = int(entry22.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a whole number for the selling price.")
                return ("S2")
            sd = entry23.get()
            mycursor.execute("INSERT INTO Car (year,make,model,trim,body,transmission,vin,state,conditioning,odometer,color,interior,sellerID,mmr,sellingprice,saledate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" , (y,mk,mdl,trm, bdy,tran, vin, st, cndt, odo, clr, inte, id, mmr, sp, sd ))
            # "Commit" is extra option to ensure the seller wants to enter this car into the database
            return "Commit"

        #Takes in the necessary information to populate the entity "Car"
        self.label2.configure(text="Enter Car Detatils")
        self.label2.pack(pady="10", side="top")
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.pack(pady="10", side="top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """year"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady="10", side="top")
        entry5 = ttk.Entry(self)
        entry5.configure(justify="center")
        _text_ = """make"""
        entry5.delete("0", "end")
        entry5.insert("0", _text_)
        entry5.pack(side="top")
        entry6 = ttk.Entry(self)
        entry6.configure(justify="center")
        _text_ = """model"""
        entry6.delete("0", "end")
        entry6.insert("0", _text_)
        entry6.pack(pady="10", side="top")
        entry7 = ttk.Entry(self)
        entry7.configure(justify="center")
        _text_ = """trim"""
        entry7.delete("0", "end")
        entry7.insert("0", _text_)
        entry7.pack(side="top")
        entry8 = ttk.Entry(self)
        entry8.configure(justify="center")
        _text_ = """body"""
        entry8.delete("0", "end")
        entry8.insert("0", _text_)
        entry8.pack(pady="10", side="top")
        entry9 = ttk.Entry(self)
        entry9.configure(justify="center")
        _text_ = """transmission"""
        entry9.delete("0", "end")
        entry9.insert("0", _text_)
        entry9.pack(pady="0", side="top")
        entry10 = ttk.Entry(self)
        entry10.configure(justify="center")
        _text_ = """vin"""
        entry10.delete("0", "end")
        entry10.insert("0", _text_)
        entry10.pack(pady="10", side="top")
        entry16 = ttk.Entry(self)
        entry16.configure(justify="center")
        _text_ = """state"""
        entry16.delete("0", "end")
        entry16.insert("0", _text_)
        entry16.pack(pady="0", side="top")
        entry17 = ttk.Entry(self)
        entry17.configure(justify="center")
        _text_ = """condition"""
        entry17.delete("0", "end")
        entry17.insert("0", _text_)
        entry17.pack(pady="10", side="top")
        entry18 = ttk.Entry(self)
        entry18.configure(justify="center")
        _text_ = """odometer"""
        entry18.delete("0", "end")
        entry18.insert("0", _text_)
        entry18.pack(side="top")
        entry19 = ttk.Entry(self)
        entry19.configure(justify="center")
        _text_ = """exterior color"""
        entry19.delete("0", "end")
        entry19.insert("0", _text_)
        entry19.pack(pady="10", side="top")
        entry20 = ttk.Entry(self)
        entry20.configure(justify="center")
        _text_ = """interior  color"""
        entry20.delete("0", "end")
        entry20.insert("0", _text_)
        entry20.pack(pady="0", side="top")
        entry21 = ttk.Entry(self)
        entry21.configure(justify="center")
        _text_ = """mmr"""
        entry21.delete("0", "end")
        entry21.insert("0", _text_)
        entry21.pack(pady="10", side="top")
        entry22 = ttk.Entry(self)
        entry22.configure(justify="center")
        _text_ = """starting price"""
        entry22.delete("0", "end")
        entry22.insert("0", _text_)
        entry22.pack(pady="0", side="top")
        entry23 = ttk.Entry(self)
        entry23.configure(justify="center")
        _text_ = """expiration date for bid"""
        entry23.delete("0", "end")
        entry23.insert("0", _text_)
        entry23.pack(pady="10", side="top")

        self.button15 = ttk.Button(self)
        self.button15.configure(text="Enter", command=lambda: controller.show_frame(load()))
        self.button15.pack(side="top")
        self.button16 = ttk.Button(self)
        self.button16.configure(text="Back", command=lambda: controller.show_frame("Seller"))
        self.button16.pack(side="top")

# Seller option 3: "View all bids on a certain car"
class S3(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )

        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        # function to convert the current row of an entity into a string that can be saved to dbLogs entity
        def convertTuple(tup):
            my_str = ""
            for item in tup:
                item = str(item)
                my_str = my_str + item + " "
            return my_str

        #function called when "Enter" button is selected by the user, allows seller to accept or reject any bid
        def load():
            vinny = entry4.get()
            mycursor.execute("SELECT MAX(price) FROM Bid where vin = %s", (vinny,))
            maxBid = mycursor.fetchall()[0][0]
            mycursor.execute("SELECT UserName FROM Buyer INNER JOIN Bid ON Buyer.BuyerID = Bid.buyerID;")
            user = mycursor.fetchall()[0][0]
            here = "Your highest bid is $" + str(maxBid) + " from buyer @" + user +"."
            e = tk.Label(self, justify = "center", text = here)
            e.pack(pady="10", side="top")
            button15 = ttk.Button(self)
            button15.configure(text="Accept Offer", command=lambda: accept())
            button15.pack(side="top")
            def accept():
                mycursor.execute("SELECT sellerID FROM Bid WHERE vin = %s", (vinny,))
                seller = mycursor.fetchall()[0][0]
                mycursor.execute("SELECT buyerID FROM Bid WHERE vin = %s", (vinny,))
                buyer = mycursor.fetchall()[0][0]
                mycursor.execute("SELECT * FROM Bid WHERE vin = %s", (vinny,))
                myBidRes = mycursor.fetchall()
                mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Bid", convertTuple(myBidRes), "NULL"))
                mycursor.execute("SELECT * FROM Car WHERE vin = %s", (vinny,))
                myCarRes = mycursor.fetchall()
                mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Car", convertTuple(myCarRes), "NULL"))
                mycursor.execute("DELETE FROM Bid WHERE vin = %s", (vinny,))
                mycursor.execute("DELETE FROM Car WHERE vin = %s", (vinny,))
                mycursor.execute("INSERT INTO Sale (vin, sellerID, buyerID, price) VALUES(%s, %s, %s, %s)", (vinny, seller, buyer, maxBid))
                mycursor.execute("SELECT * FROM Sale WHERE vin = %s", (vinny,))
                mySaleRes = mycursor.fetchall()
                mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Sale", "NULL", convertTuple(mySaleRes)))
                tkinter.messagebox.showinfo('Invalid ID.',  "Offer has been accepted! Funds will be transferred by our third party crediting service. Please wait to be re-directed to the home page.")
                mydb.commit()
                return "Seller"

        self.label2.configure(text="Viewing bids")
        self.label2.pack(pady="10", side="top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady="10", side="top")
        self.button17 = ttk.Button(self)
        self.button17.configure(text="Enter", command=lambda: load())
        self.button17.pack(side="top")
        self.button18 = ttk.Button(self)
        self.button18.configure(text="Back", command=lambda: controller.show_frame("Seller"))
        self.button18.pack(side="top")

#Seller option 4: "Take a car off the market"
class S4(tk.Frame):
    def __init__(self, parent, controller):

        def convertTuple(tup):
            my_str = ""
            for item in tup:
                item = str(item)
                my_str = my_str + item + " "
            return my_str

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        #called when the "Enter" button is selected by the user, removes the current car from the database
        def load():
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "S4"
            vinny = entry4.get()
            mycursor.execute("SELECT * FROM Car WHERE vin = %s", (vinny,))
            myCar = mycursor.fetchall()
            mycursor.execute("SELECT * FROM Bid WHERE vin = %s", (vinny,))
            myBid = mycursor.fetchall()
            mycursor.execute("DELETE FROM Car WHERE vin = %s", (vinny,))
            mycursor.execute("DELETE FROM Bid WHERE vin = %s", (vinny,))
            mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Car", convertTuple(myCar), "NULL"))
            mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Bid", convertTuple(myBid), "NULL"))
            mydb.commit()
            tkinter.messagebox.showinfo('Invalid ID.',  "This car has been successfully removed from the market.")
            return "Seller"

        self.label2.configure(text="Pull Car")
        self.label2.pack(pady="10", side="top")
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.pack(pady="10", side="top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady="10", side="top")
        button15 = ttk.Button(self)
        button15.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button15.pack(pady="10",side="top")
        button16 = ttk.Button(self)
        button16.configure(text="Back", command=lambda: controller.show_frame("Seller"))
        button16.pack(pady="10",side="top")

#Seller option 5: "View average bid price of each of your cars"
class S15(tk.Frame):
     def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        #called when the "Enter" button is selected by the user, aggregates the average bid price of each car based on the vin that this seller owns
        def load():
            try:
                id = int(entry4.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "S15"
            e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=2,column=0)
            e=tk.Label(self,width=20,text='avg price',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=2,column=1)
            mycursor.execute("SELECT vin, (SELECT AVG(price) FROM Bid) AS avgBidPrice FROM Bid WHERE sellerID = {} GROUP BY vin".format(id))
            mydb.commit()
            r_set = mycursor.fetchall()
            # display the results
            i=3
            for bid in r_set:
                for j in range(len(bid)):
                    e = tk.Label(self, width= 20, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                    e.grid(row=i, column=j)
                i=i+1
            return "S15"

        self.label2.configure(text="Average Bid Price")
        self.label2.grid(row = 0, column = 2)
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """id"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.grid(row = 1, column = 1)
        button17 = ttk.Button(self)
        button17.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button17.grid(row = 1, column = 2)
        button17 = ttk.Button(self)
        button17.configure(text="Back", command=lambda: controller.show_frame("Seller"))
        button17.grid(row = 1, column = 3)

#Buyer option 1: "Shop cars"
class B5(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Cars",
        )

        #Called when buyer selects "Enter" button, handles error checking and yields result set
        def populate():
            try:
                year = int(entry11.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a valid calendar year.")
                return "B5"
            make = str(entry12.get())
            model = str(entry13.get())
            try:
                price = int(entry14.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a whole number for the price.")
                return "B5"
            mycursor.execute("SELECT * FROM Car WHERE year >= %s AND UPPER(make) = UPPER(%s) AND UPPER(model) = UPPER(%s) AND sellingprice <= %s", (year, make, model, price))
            r_set = mycursor.fetchall()
            print(r_set)
            i=3
            for bid in r_set:
                for j in range(len(bid)):
                    w = 10
                    if j == 3 or j == 6 or j == 15:
                        w=20
                    if j == 0 or j == 7 or j == 8 or j == 12:
                        w=5
                    if j == 6:
                        e = tk.Button(self, width= w, borderwidth=2,relief='ridge', justify = "center", text = bid[j],command=lambda: [controller.show_frame("B6")])
                        e.grid(row=i, column=j)
                    else:
                        e = tk.Label(self, width= w, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                        e.grid(row=i, column=j)
                i=i+1
            return("B5")

        # Create the grid to display records from the "Car" entity
        self.title.grid(row=0, column=3)
        e=tk.Label(self,width=5,text='Year',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=0)
        e=tk.Label(self,width=10,text='Make',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=1)
        e=tk.Label(self,width=10,text='Model',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=2)
        e=tk.Label(self,width=20,text='Trim',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=3)
        e=tk.Label(self,width=10,text='Body',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=4)
        e=tk.Label(self,width=10,text='Transmission',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=5)
        e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=6)
        e=tk.Label(self,width=5,text='State',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=7)
        e=tk.Label(self,width=5,text='Condition',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=8)
        e=tk.Label(self,width=10,text='Odometer',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=9)
        e=tk.Label(self,width=10,text='Color',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=10)
        e=tk.Label(self,width=10,text='Interior',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=11)
        e=tk.Label(self,width=5,text='SellerId',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=12)
        e=tk.Label(self,width=10,text='mmr',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=13)
        e=tk.Label(self,width=10,text='Sale Price',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=14)
        e=tk.Label(self,width=20,text='Sale Date',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=15)
        entry11 = ttk.Entry(self)
        entry11.configure(justify="center", width = 10)
        _text_ = """lowest year"""
        entry11.delete("0", "end")
        entry11.insert("0", _text_)
        entry11.grid(row = 1, column = 2)
        entry12 = ttk.Entry(self)
        entry12.configure(justify="center" , width = 20)
        _text_ = """make"""
        entry12.delete("0", "end")
        entry12.insert("0", _text_)
        entry12.grid(row = 1, column = 3)
        entry13 = ttk.Entry(self)
        entry13.configure(justify="center", width = 10)
        _text_ = """model"""
        entry13.delete("0", "end")
        entry13.insert("0", _text_)
        entry13.grid(row = 1, column = 4)
        entry14 = ttk.Entry(self)
        entry14.configure(justify="center", width = 10)
        _text_ = """max price"""
        entry14.delete("0", "end")
        entry14.insert("0", _text_)
        entry14.grid(row = 1, column = 5)
        button21 = ttk.Button(self)
        button21.configure(text="Enter", command=lambda: controller.show_frame(populate()) , width = 20)
        button21.grid(row =1, column = 6)
        button19 = ttk.Button(self)
        button19.configure(text="Back", command=lambda: controller.show_frame("Buyer") , width = 5)
        button19.grid(row=1,column=7)

# Buyer option 2: "Make a bid"
class B6(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Make Bids",
        )

        # takes a record from an entity and converts it to a string to be stored in dbLogs entity
        def convertTuple(tup):
            my_str = ""
            for item in tup:
                item = str(item)
                my_str = my_str + item + " "
            return my_str

        # called when buyer selects "Search" button, displays the max bid of the car they want to bid on
        def load():
            vinny = entry4.get()
            mycursor.execute("SELECT MAX(price) FROM Bid WHERE vin = %s", (vinny,))
            price = mycursor.fetchall()[0][0]
            text2 = "The highest bid on car "+ vinny+ " is $" + str(price) +  "."
            e = tk.Label(self, justify = "center", text = text2)
            e.pack(pady = "10", side = "top")
            return "B6"

        #Called when buyer selects the "Enter" button, handles errors and commits new bid to DB
        def insert():
            try:
                money = int(entry5.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "Please enter a whole number for the price.")
                return "B6"
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "B6"
            vinny = entry4.get()
            mycursor.execute("SELECT sellerID FROM Car WHERE vin = %s", (vinny,))
            seller = mycursor.fetchall()[0][0]
            mycursor.execute("INSERT INTO Bid (vin, sellerID, buyerID, price, dateTime) VALUES(%s, %s, %s, %s, %s)", (vinny, seller, id, money, date.today()))
            mydb.commit()
            mycursor.execute("SELECT * FROM Bid WHERE vin = %s", (vinny,))
            myBidRes = mycursor.fetchall()
            #mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Bid", "NULL", convertTuple(myBidRes)))
            return "Cards"

        #Called when buyer selects the "Back" button, does not commit new bid to DB and undoes any recent changes related to the current transaction
        def rolling():
            mydb.rollback()
            return "Buyer"

        self.title.pack(pady = "10", side = "top")
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.pack(pady = "10", side = "top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady = "10", side = "top")
        button19 = ttk.Button(self)
        button19.configure(text="Search", command=lambda: controller.show_frame(load()))
        button19.pack(pady = "10", side = "top")

        entry5 = ttk.Entry(self)
        entry5.configure(justify="center")
        _text_ = """new bid amount"""
        entry5.delete("0", "end")
        entry5.insert("0", _text_)
        entry5.pack(pady = "10", side = "top")
        button17 = ttk.Button(self)
        button17.configure(text="Enter", command=lambda: controller.show_frame(insert()))
        button17.pack(pady = "10", side = "top")
        button22 = ttk.Button(self)
        button22.configure(text="Back", command=lambda: controller.show_frame(rolling()))
        button22.pack(pady = "10", side = "top")

# Buyer option 3: "View your bids"
class B7(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Your Bids",
        )

        #Called when buyer selects "Enter" button, displays result set of all bids made by current buyer using their id
        def load():
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "B7"
            mycursor.execute("SELECT * FROM Bid WHERE buyerID = %s", (id,))
            r_set = mycursor.fetchall()
            #create a grid to display the results
            i=3
            for bid in r_set:
                for j in range(len(bid)):
                    e = tk.Label(self, width=20, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                    e.grid(row=i, column=j)
                i=i+1
            return "B7"

        self.title.grid(row=0, column=3)
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.grid(row = 1, column = 3)
        button19 = ttk.Button(self)
        button19.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button19.grid(row = 1, column = 4)
        button18 = ttk.Button(self)
        button18.configure(text="Back", command=lambda: controller.show_frame("Buyer"))
        button18.grid(row=1,column=5)
        e=tk.Label(self,width=20,text='BidID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=0)
        e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=1)
        e=tk.Label(self,width=20,text='SellerID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=2)
        e=tk.Label(self,width=20,text='BuyerID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=3)
        e=tk.Label(self,width=20,text='Price',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=4)
        e=tk.Label(self,width=20,text='Time',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
        e.grid(row=2,column=5)

#Buyer option 4: "Update your bids"
class B8(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Bids",
        )

        #converts records to a string to be stored in dbLogs
        def convertTuple(tup):
            my_str = ""
            for item in tup:
                item = str(item)
                my_str = my_str + item + " "
            return my_str

        #Called when buyer selects "Search" button, creates grid to display results of current bid on a specific car
        def search():
            e=tk.Label(self,width=20,text='BidID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=0)
            e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=1)
            e=tk.Label(self,width=20,text='SellerID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=2)
            e=tk.Label(self,width=20,text='BuyerID',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=3)
            e=tk.Label(self,width=20,text='Price',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=4)
            e=tk.Label(self,width=20,text='Time',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=3,column=5)
            vinny = entry4.get()
            mycursor.execute("SELECT * FROM Bid WHERE vin = %s", (vinny,))
            r_set = mycursor.fetchall()
            i=4
            for bid in r_set:
                for j in range(len(bid)):
                    e = tk.Label(self, width=20, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                    e.grid(row=i, column=j)
                i=i+1
            return "B8"

        #Called when buyer selects "Enter" button, updates the current bid in the database with a new price
        def load():
            try:
                money = int(entry5.get())
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number or price you have entered is incorrect. Please try again.")
                return"B8"
            vinny = entry4.get()
            mycursor.execute("SELECT * FROM Bid WHERE price = %s AND vin = %s AND buyerID = %s", (money,vinny,id))
            myresult = mycursor.fetchall()
            mycursor.execute("SELECT * FROM Bid WHERE price = %s AND vin = %s AND buyerID = %s", (money,vinny,id))
            myresult2 = mycursor.fetchall()
            mycursor.execute("DROP TRIGGER bid_update2;")
            mycursor.execute("CREATE TRIGGER bid_update2 BEFORE UPDATE ON Bid FOR EACH ROW INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Bid", convertTuple(myresult), convertTuple(myresult2)))
            mycursor.execute("UPDATE Bid SET price = %s WHERE vin = %s AND buyerID = %s ", (money,vinny,id))
            mydb.commit()
            tkinter.messagebox.showinfo('Your bid has been updated!',  "Bid updated! Click back to go to homepage or update another bid.")
            return "B8"

        self.title.grid(row = 0, column = 2)
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.grid(row = 1, column = 1)
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin to update"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.grid(row = 1, column = 2)
        button20 = ttk.Button(self)
        button20.configure(text="Search", command=lambda: controller.show_frame(search()))
        button20.grid(row = 1, column = 3)

        entry5 = ttk.Entry(self)
        entry5.configure(justify="center")
        _text_ = """new bid amount"""
        entry5.delete("0", "end")
        entry5.insert("0", _text_)
        entry5.grid(row = 2, column = 1)
        button19 = ttk.Button(self)
        button19.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button19.grid(row = 2, column = 2)
        button21 = ttk.Button(self)
        button21.configure(text="Back", command=lambda: controller.show_frame("Buyer"))
        button21.grid(row = 2, column = 3)

#Buyer option 5: "Cancel your bid"
class B9(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Bids",
        )

        #Converts a record into a string for insertion into dbLogs entity
        def convertTuple(tup):
            my_str = ""
            for item in tup:
                item = str(item)
                my_str = my_str + item + " "
            return my_str

        #Called when buyer selects "Enter" button, handles errors and removes a bid from the db
        def load():
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return"B9"
            vinny = entry4.get()
            mycursor.execute("SELECT * FROM Bid WHERE vin = %s AND buyerID = %s", (vinny,id))
            myBid = mycursor.fetchall()
            mycursor.execute("DELETE FROM Bid WHERE vin = %s AND buyerID = %s", (vinny,id))
            mycursor.execute("INSERT INTO dbLogs (logDate, ent, modifiedFrom, modifiedTo) Values(%s,%s,%s,%s)", (date.today(), "Bid", convertTuple(myBid), "NULL"))
            mydb.commit()
            tkinter.messagebox.showinfo('Your bid has been cancelled!',  "Bid cancelled! Click back to go to homepage or cancel another bid.")
            return "B9"

        self.title.grid(row = 0, column = 2)
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.grid(row = 1, column = 1)
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin to cancel"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.grid(row = 1, column = 2)
        button19 = ttk.Button(self)
        button19.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button19.grid(row = 1, column = 3)
        button21 = ttk.Button(self)
        button21.configure(text="Back", command=lambda: controller.show_frame("Buyer"))
        button21.grid(row = 1, column = 4)

#Buyer option 8: "View number of bids you have made on each car"
class B16(tk.Frame):
     def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        #Called when buyer selects "Enter" button, handels error checking, shows aggregate result set, sets up grid for result set
        def load():
            try:
                id = int(entry4.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "B16"
            e=tk.Label(self,width=20,text='number bids',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=2,column=0)
            e=tk.Label(self,width=20,text='vin',borderwidth=2, relief='ridge', justify = "center", bg ="#f6fa93")
            e.grid(row=2,column=1)
            mycursor.execute("SELECT COUNT(*) AS numBids, vin FROM Bid WHERE BuyerID = {} GROUP BY vin".format(id))
            mydb.commit()
            r_set = mycursor.fetchall()
            i=3
            for bid in r_set:
                for j in range(len(bid)):
                    e = tk.Label(self, width= 20, borderwidth=2,relief='ridge', justify = "center", text = bid[j])
                    e.grid(row=i, column=j)
                i=i+1
            return "B16"

        self.label2.configure(text="Bids per Car")
        self.label2.grid(row = 0, column = 2)
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """id"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.grid(row = 1, column = 1)
        button17 = ttk.Button(self)
        button17.configure(text="Enter", command=lambda: controller.show_frame(load()))
        button17.grid(row = 1, column = 2)
        button24 = ttk.Button(self)
        button24.configure(text="Back", command=lambda: controller.show_frame("Buyer"))
        button24.grid(row = 1, column = 3)

# Used when buyer makes a bid, handles actions if buyer wants to use a card on file to make a bid
class Exists(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
                anchor="nw",
                height="400",
                relheight="1.0",
                relwidth="1.0",
                width="400",
                x="0",
                y="0",
            )
        self.label2 = ttk.Label(self)
        self.label2.configure(
                background="#8884dc",
                compound="bottom",
                font="{Futura} 20 {}",
                justify="center",
        )

        #Called when buyer selects a card in result set of all their cards on file, takes payment handling to a third party credit service
        def transaction():
            tkinter.messagebox.showinfo('title',  "Now the actions of the third party credit service would be handled.")

        #Called when buyer selects "Search" button, checks for and displays existing credit cards for the buyer
        def load():
            try:
                id = int(entry4.get())
            except ValueError:
                return "Error"
            mycursor.execute("SELECT cardNum FROM CreditCard WHERE buyerID = {}".format(id))
            myresult = mycursor.fetchall()
            print(myresult)
            if mycursor.rowcount == 0:
                tkinter.messagebox.showinfo('title',  "No credit card found. Please return to the previous page for a new card entry.")
                mydb.rollback()
                return "Cards"
            else:
                i=3
                for bid in myresult:
                    for j in range(len(bid)):
                        card = tk.Button(self, width= 20, borderwidth=2,relief='ridge', justify = "center", text = myresult[j], command=lambda: controller.show_frame(transaction()))
                        card.grid(row=i, column=3)
                        i = i+1
                return "Exists"

        self.label2.configure(text="Payment Options")
        self.label2.grid(row = 0, column = 2)
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """id"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.grid(row = 1, column = 1)
        button17 = ttk.Button(self)
        button17.configure(text="Search", command=lambda: controller.show_frame(load()))
        button17.grid(row = 1, column = 2)
        button24 = ttk.Button(self)
        button24.configure(text="Back", command=lambda: controller.show_frame("Cards"))
        button24.grid(row = 1, column = 3)
        mydb.commit()

#Starts payment process when buyer makes a bid
class Cards(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas3 = tk.Canvas(self)
        self.canvas3.configure(background="#f3a3bf", height="400", width="400")
        self.canvas3.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.label2 = ttk.Label(self)
        self.label2.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
        )

        #function to validate credit card number, taken from here: https://gist.githubusercontent.com/Allwin12/42e10cc21e66b1ff764a18058c74a244/raw/06996722c3c7edcc4c103fe07f4c33372eed2f46/luhn.py
        def luhn_checksum(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = 0
            checksum += sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10

        #Called when buyer selects "Enter" button, saves a new credit card to the db
        def load():
            try:
                id = int(entry2.get())
                cardno = int(entry3.get())
                secCode = entry6.get()
                billZip = entry7.get()
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The card information you have entered is incorrect. Please try again.")
                return ("Cards")
            isValid = luhn_checksum(cardno)
            if isValid !=0:
                tkinter.messagebox.showinfo('Invalid ID.',  "The card number you have entered is incorrect. Please try again.")
                return ("Cards")
            cardHldrName = entry4.get()
            expire = entry5.get()
            mycursor.execute("INSERT INTO CreditCard (cardNum, cardHolderName, expDate, securityCode, billingZip, buyerID) VALUES(%s, %s, %s, %s, %s, %s)", (cardno, cardHldrName, expire, secCode, billZip, id))
            mydb.commit()
            return "Buyer"

        #Called when buyer selects "Back" button, goes back to main menu and undoes any relevant transactions
        def rolling():
            mydb.rollback()
            return "Buyer"

        #Called when buyer selects "Use existing card" button, takes buyer to a page where they can select a card on file to use for the current bid
        def exist():
            return "Exists"

        #takes the buyers credit card if not already on file
        self.label2.configure(text="Enter Card Detatils")
        self.label2.pack(pady="10", side="top")
        entry2 = ttk.Entry(self)
        entry2.configure(justify="center")
        _text_ = """id"""
        entry2.delete("0", "end")
        entry2.insert("0", _text_)
        entry2.pack(pady="10", side="top")
        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """card number"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.pack(pady="10", side="top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """card holder name"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady="10", side="top")
        entry5 = ttk.Entry(self)
        entry5.configure(justify="center")
        _text_ = """expiration (MM/YY)"""
        entry5.delete("0", "end")
        entry5.insert("0", _text_)
        entry5.pack(side="top")
        entry6 = ttk.Entry(self)
        entry6.configure(justify="center")
        _text_ = """security code"""
        entry6.delete("0", "end")
        entry6.insert("0", _text_)
        entry6.pack(pady="10", side="top")
        entry7 = ttk.Entry(self)
        entry7.configure(justify="center")
        _text_ = """billing zip"""
        entry7.delete("0", "end")
        entry7.insert("0", _text_)
        entry7.pack(side="top")

        self.button0 = ttk.Button(self)
        self.button0.configure(text="Use existing card", command=lambda: controller.show_frame(exist()))
        self.button0.pack(side="top")
        self.button15 = ttk.Button(self)
        self.button15.configure(text="Enter", command=lambda: controller.show_frame(load()))
        self.button15.pack(side="top")
        self.button16 = ttk.Button(self)
        self.button16.configure(text="Back", command=lambda: controller.show_frame(rolling()))
        self.button16.pack(side="top")

# Buyer option 6, Seller option 5: "Export data"
class Export(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )

        #Called when user selects "Back" button, returns to appropriate menu
        def returns():
            if id < 1000000:
                return "Seller"
            else:
                return "Buyer"

        #Called when user selects "Enter", queries appropriate record and writes it to a file
        def exports():
            global id
            try:
                id = int(entry3.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return ("Export")
            vinny = entry4.get()
            if id < 1000000: #Seller
                #satisfying joins accross three tables
                mycursor.execute("SELECT Bid.*, Car.make, Car.model, Buyer.UserName, Buyer.BuyerLoc FROM Car INNER JOIN Bid ON Car.vin = Bid.vin INNER JOIN Buyer on Buyer.BuyerID = Bid.buyerID WHERE Car.vin = %s", (vinny,))
                myresult = mycursor.fetchall()
            else: #Buyer
                #satisfying joins accross three tables
                mycursor.execute("SELECT Bid.*, Car.make, Car.model, Seller.UserName, Seller.SellerLoc FROM Car INNER JOIN Bid ON Car.vin = Bid.vin INNER JOIN Seller on Seller.SellerID = Bid.sellerID WHERE Car.vin = %s", (vinny,))
                myresult = mycursor.fetchall()
            f = open("csvCar.txt", "w")
            for x in myresult:
                for i in range(10):
                    f.write(str(x[i]) + ",")
                f.write("\n")
            f.close()
            self.title = ttk.Label(self)
            self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Data Exported to csvCar.txt",
            )
            self.title.pack(pady="50", side="top")
            return("Export")

        entry3 = ttk.Entry(self)
        entry3.configure(justify="center")
        _text_ = """your id"""
        entry3.delete("0", "end")
        entry3.insert("0", _text_)
        entry3.pack(pady="10", side="top")
        entry4 = ttk.Entry(self)
        entry4.configure(justify="center")
        _text_ = """vin"""
        entry4.delete("0", "end")
        entry4.insert("0", _text_)
        entry4.pack(pady="10", side="top")

        button1 = tk.Button(self, text="Enter",command=lambda: controller.show_frame(exports()))
        button1.pack(side="top",pady="10")
        button2 = tk.Button(self, text="Back",command=lambda: controller.show_frame(returns()))
        button2.pack(side="top",pady="10")

# class Error(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.canvas2 = tk.Canvas(self)
#         self.canvas2.configure(background="#f3a3bf", height="400", width="400")
#         self.canvas2.place(
#             anchor="nw",
#             height="400",
#             relheight="1.0",
#             relwidth="1.0",
#             width="400",
#             x="0",
#             y="0",
#         )
#         self.title = ttk.Label(self)
#         self.title.configure(
#             background="#8884dc",
#             compound="bottom",
#             font="{Futura} 20 {}",
#             justify="center",
#             text="Bad Input",
#         )
#         self.title.pack(pady="50", side="top")
#
#         button2 = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
#         button2.pack(side="top")

#Used to double check that a seller wants to put the current car on the market
class Commit(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas2 = tk.Canvas(self)
        self.canvas2.configure(background="#f3a3bf", height="400", width="400")
        self.canvas2.place(
            anchor="nw",
            height="400",
            relheight="1.0",
            relwidth="1.0",
            width="400",
            x="0",
            y="0",
        )
        self.title = ttk.Label(self)
        self.title.configure(
            background="#8884dc",
            compound="bottom",
            font="{Futura} 20 {}",
            justify="center",
            text="Are you sure?",
        )

        #Called when seller selects the "Yes" button, commits the new car to the db
        def committing():
            try:
                id = int(entry12.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "Commit"
            mydb.commit()
            if id < 1000000:
                return "Seller"
            else:
                return "Buyer"

        #Called when seller selects the "No" button, does not commit new car to the db and rolls back all relevant transactions
        def rolling():
            try:
                id = int(entry12.get())
            except ValueError:
                tkinter.messagebox.showinfo('Invalid ID.',  "The ID number you have entered is incorrect. Please try again.")
                return "Commit"
            mydb.rollback()
            if id < 1000000:
                return "Seller"
            else:
                return "Buyer"

        self.title.pack(pady= "10", side = "top")
        entry12 = ttk.Entry(self)
        entry12.configure(justify="center" , width = 20)
        _text_ = """id"""
        entry12.delete("0", "end")
        entry12.insert("0", _text_)
        entry12.pack(side="top")
        button2 = tk.Button(self, text="Yes", command=lambda: controller.show_frame(committing()))
        button2.pack(side="top")
        button2 = tk.Button(self, text="No", command=lambda: controller.show_frame(rolling()))
        button2.pack(side="top")

if __name__ == "__main__":
    app = SampleApp()
    app.title("KellyPinkBook.com")
    app.mainloop()
