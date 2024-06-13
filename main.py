from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox
import pickle


# Istifadeci klasi
class User:
    def __init__(self, name, surname, fatherName, email, login, password):
        self.__name = name
        self.__surname = surname
        self.__fatherName = fatherName
        self.__email = email
        self.__login = login
        self.__password = password

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_father_name(self):
        return self.__fatherName

    def get_email(self):
        return self.__email

    def get_login(self):
        return self.__login

    def get_password(self):
        return self.__password

    def validate_login(self, entered_login, entered_password):
        return self.__login == entered_login and self.__password == entered_password


# Məhsul klasi
class Product:
    def __init__(self, kategory, supplier, name, price, count):
        self.__kategory = kategory
        self.__supplier = supplier
        self.__name = name
        self.__price = price
        self.__count = count

    def get_kategory(self):
        return self.__kategory

    def get_supplier(self):
        return self.__supplier

    def get_name(self):
        return self.__name

    def get_price(self):
        return float(self.__price)

    def get_count(self):
        return int(self.__count)

    def set_kategory(self, kategory):
        self.__kategory = kategory

    def set_supplier(self, supplier):
        self.__supplier = supplier

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_count(self, count):
        self.__count = count


# Admin Panel klasi
class AdminPanel:
    def __init__(self):
        self.users_warehouse = []
        self.users_seller = []
        self.siyahiBack = []
        self.siyahiBack_basket = []

    def load_data(self):
        try:
            with open('users_warehouse.pkl', 'rb') as f:
                self.users_warehouse = pickle.load(f)
            with open('users_seller.pkl', 'rb') as f:
                self.users_seller = pickle.load(f)
            with open('mehsullar.pkl', 'rb') as file:
                self.siyahiBack = pickle.load(file)
        except (FileNotFoundError, EOFError) as e:

            self.users_warehouse = []
            self.users_seller = []
            self.siyahiBack = []

    def save_data(self):
        with open('users_warehouse.pkl', 'wb') as f:
            pickle.dump(self.users_warehouse, f)
        with open('users_seller.pkl', 'wb') as f:
            pickle.dump(self.users_seller, f)
        with open('mehsullar.pkl', 'wb') as file:
            pickle.dump(self.siyahiBack, file)


# Seller Panel klasi
class SellerPanel(AdminPanel):
    def __init__(self):
        super().__init__()
        self.toplamQiymet = 0

    def add_to_basket(self, product, count):
        self.siyahiBack_basket.append(product)
        self.toplamQiymet += product.get_price() * count
        product.set_count(product.get_count() - count)

    def delete_from_basket(self, product, count):
        if product in self.siyahiBack_basket:
            self.siyahiBack_basket.remove(product)
            self.toplamQiymet -= product.get_price() * count
            product.set_count(product.get_count() + count)


# Warehouse Panel klasi
class WarehousePanel(AdminPanel):
    def add_product(self, product):
        for p in self.siyahiBack:
            if (p.get_name() == product.get_name() and p.get_supplier() == product.get_supplier() and
                    p.get_kategory() == product.get_kategory() and p.get_price() == product.get_price()):
                return False
        self.siyahiBack.append(product)
        return True

    def delete_product(self, product):
        if product in self.siyahiBack:
            self.siyahiBack.remove(product)
            return True
        return False


# GUI klasi
class Application:
    def __init__(self, root):
        self.root = root
        self.admin_panel = AdminPanel()
        self.seller_panel = SellerPanel()
        self.warehouse_panel = WarehousePanel()
        self.admin_panel.load_data()
        self.setup_gui()
        self.my_listbox = None
        self.my_listbox_seller = None

    def setup_gui(self):
        self.root.geometry("600x500")
        self.root.title("Anbar və Satış Programı")
        self.root.iconbitmap("anbarlogo.ico")
        self.root.resizable(False, False)

        self.rootFrame = Frame(self.root, width=600, height=500)
        self.rootFrame.pack()

        self.btn_warehouse = Button(self.rootFrame, text="Anbardar", bg='#010c48', fg='white', cursor="hand2",
                                    activebackground="dark orange",
                                    command=self.warehouse_login, font=("", 12, "bold"))
        self.btn_warehouse.place(x=150, y=150, width=120, height=50)

        self.btn_seller = Button(self.rootFrame, text="Satıcı", bg='#010c48', fg='white',
                                 activebackground="dark orange", cursor="hand2",
                                 font=("", 12, "bold"), command=self.seller_login)
        self.btn_seller.place(x=330, y=150, width=120, height=50)

        self.menuLogo = Image.open("anbarsekil.png")
        self.menuLogo = self.menuLogo.resize((450, 500))
        self.menuLogo = ImageTk.PhotoImage(self.menuLogo)
        self.lbl_menulogo = Label(self.rootFrame, image=self.menuLogo)
        self.lbl_menulogo.place(x=240, y=250)

        self.icon_title = PhotoImage(file="anbartitlelogonew.png")
        self.title = Label(self.rootFrame, text="Anbar və Satış Programı", image=self.icon_title, compound=LEFT,
                           font=("times new roman", 28, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        self.title.place(x=0, y=0, width=600, height=70)

    def warehouse_login(self):
        self.rootFrame.pack_forget()
        self.warehouseFrame = Frame(self.root, width=600, height=500)
        self.warehouseFrame.pack()

        self.icon_title_Warehouse_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleWarehouseFrame = Label(self.warehouseFrame, text="Proqrama Giriş Edin!",
                                         image=self.icon_title_Warehouse_Frame, compound=LEFT,
                                         font=("times new roman", 30, "bold"), bg="#010c48", fg="white", anchor="w",
                                         padx=20)
        self.titleWarehouseFrame.place(x=0, y=0, width=600, height=70)

        self.warehousePhoto = Image.open("register.png")
        self.warehousePhoto = self.warehousePhoto.resize((450, 500))
        self.warehousePhoto = ImageTk.PhotoImage(self.warehousePhoto)
        self.warehousePhoto_lbl_menulogo = Label(self.warehouseFrame, image=self.warehousePhoto)
        self.warehousePhoto_lbl_menulogo.place(relx=0.4, rely=0.5)

        self.btn_register_warehouse = Button(self.warehouseFrame, text="Qeydiyyat", bg='#010c48', fg='white',
                                             activebackground="dark orange",
                                             font=("", 12, "bold"), command=self.warehouse_register)
        self.btn_register_warehouse.place(relx=0.28, rely=0.3, relwidth=0.2, relheight=0.1)

        self.btn3 = Button(self.warehouseFrame, text="< Geri", bg='red', fg='white', font=("", 12, "bold"),
                           command=self.back_to_root)
        self.btn3.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.btn_Warehouse_login = Button(self.warehouseFrame, text="Giriş", bg='#010c48', fg='white',
                                          activebackground="dark orange",
                                          font=("", 12, "bold"), command=self.warehouse_sign_in)
        self.btn_Warehouse_login.place(relx=0.53, rely=0.3, relwidth=0.2, relheight=0.1)

    def warehouse_register(self):
        self.warehouseFrame.pack_forget()
        self.warehouseRegisterFrame = Frame(self.root, width=600, height=500)
        self.warehouseRegisterFrame.pack()

        self.icon_title_Warehouse_Register_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleWarehouse_Register_Frame = Label(self.warehouseRegisterFrame, text="Məlumatları daxil edin",
                                                   image=self.icon_title_Warehouse_Register_Frame, compound=LEFT,
                                                   font=("times new roman", 30, "bold"), bg="#010c48", fg="white",
                                                   anchor="w", padx=20)
        self.titleWarehouse_Register_Frame.place(x=0, y=0, relwidth=1, height=70)

        self.back_btn_to_warehouse = Button(self.warehouseRegisterFrame, text="< Geri", bg='red', fg='white',
                                            activebackground="dark orange", font=("", 12, "bold"),
                                            command=self.back_to_warehouse_menu2)
        self.back_btn_to_warehouse.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.registerwarehousePhoto = Image.open("register_warehouse.png")
        self.registerwarehousePhoto = self.registerwarehousePhoto.resize((100, 100))
        self.registerwarehousePhoto = ImageTk.PhotoImage(self.registerwarehousePhoto)
        self.registerwarehousePhoto_lbl_menulogo = Label(self.warehouseRegisterFrame, image=self.registerwarehousePhoto)
        self.registerwarehousePhoto_lbl_menulogo.place(relx=0.45, rely=0.15)

        self.labelFrame = Frame(self.warehouseRegisterFrame, bg='#044F67')
        self.labelFrame.place(relx=0.2, rely=0.44, relwidth=0.6, relheight=0.42)

        self.lbl_name_warehouse = Label(self.labelFrame, text="Ad : ", bg='#044F67', fg='white',
                                        font=("goudy old style", 15))
        self.lbl_name_warehouse.place(relx=0.05, rely=0.05)
        self.en_name_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_name_warehouse.place(relx=0.3, rely=0.05, relwidth=0.62)

        self.lbl_surname_warehouse = Label(self.labelFrame, text="Soyad : ", bg='#044F67', fg='white',
                                           font=("goudy old style", 15))
        self.lbl_surname_warehouse.place(relx=0.05, rely=0.2)
        self.en_surname_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_surname_warehouse.place(relx=0.3, rely=0.2, relwidth=0.62)

        self.lbl_fatherName_warehouse = Label(self.labelFrame, text="Ata adı : ", bg='#044F67', fg='white',
                                              font=("goudy old style", 15))
        self.lbl_fatherName_warehouse.place(relx=0.05, rely=0.35)
        self.en_fatherName_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_fatherName_warehouse.place(relx=0.3, rely=0.35, relwidth=0.62)

        self.lbl_email_warehouse_warehouse = Label(self.labelFrame, text="Email ", bg='#044F67', fg='white',
                                                   font=("goudy old style", 15))
        self.lbl_email_warehouse_warehouse.place(relx=0.05, rely=0.5)
        self.en_email_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_email_warehouse.place(relx=0.3, rely=0.5, relwidth=0.62)

        self.lb_login_warehouse = Label(self.labelFrame, text="Login : ", bg='#044F67', fg='white',
                                        font=("goudy old style", 15))
        self.lb_login_warehouse.place(relx=0.05, rely=0.65)
        self.en_login_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_login_warehouse.place(relx=0.3, rely=0.65, relwidth=0.62)

        self.lb_password_warehouse = Label(self.labelFrame, text="Şifrə : ", bg='#044F67',
                                           activebackground="dark orange", fg='white', font=("goudy old style", 15))
        self.lb_password_warehouse.place(relx=0.05, rely=0.8)
        self.en_password_warehouse = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow", show="*")
        self.en_password_warehouse.place(relx=0.3, rely=0.8, relwidth=0.62)

        self.SubmitBtn = Button(self.warehouseRegisterFrame, text="Qeydiyyat ol", bg='#264348', fg='white',
                                activebackground="dark orange", command=self.register_warehouse_button)
        self.SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    def register_warehouse_button(self):
        name_warehouse = self.en_name_warehouse.get()
        surname_warehouse = self.en_surname_warehouse.get()
        father_name_warehouse = self.en_fatherName_warehouse.get()
        email_warehouse = self.en_email_warehouse.get()
        login_warehouse = self.en_login_warehouse.get()
        password_warehouse = self.en_password_warehouse.get()

        if not (
                name_warehouse and surname_warehouse and father_name_warehouse and email_warehouse and login_warehouse and password_warehouse):
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bütün xanaları doldurmalısınız!")
            return
        if len(name_warehouse) < 3:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Ad minimum 3 simvoldan az olmamalıdır!")
            return
        if len(surname_warehouse) < 5:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Soyad minimum 5 simvoldan az olmamalıdır!")
            return
        if not name_warehouse.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Ad yalnız hərflərdən ibarət olmalıdır!")
            return
        if not surname_warehouse.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Soyad yalnız hərflərdən ibarət olmalıdır!")
            return
        if not father_name_warehouse.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Ata adı yalnız hərflərdən ibarət olmalıdır!")
            return
        if '@' not in email_warehouse or '.' not in email_warehouse:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Doğru bir email daxil edin!")
            return
        if len(login_warehouse) < 8 or len(login_warehouse) > 16 or not login_warehouse.isalnum():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Login minimum 8, maksimum 16 simvoldan ibarət olmalıdır və yalnız hərf və rəqəmlərdən ibarət olmalıdır!")
            return
        if len(password_warehouse) < 8 or len(password_warehouse) > 16 or not password_warehouse.isalnum():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Şifrə minimum 8, maksimum 16 simvoldan ibarət olmalıdır və yalnız hərf və rəqəmlərdən ibarət olmalıdır!")
            return

        for user in self.admin_panel.users_warehouse:
            if user.get_login() == login_warehouse:
                tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bu adda Login artıq mövcuddur!")
                return
            if user.get_email() == email_warehouse:
                tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bu adda email artıq mövcuddur!")
                return

        user = User(name_warehouse, surname_warehouse, father_name_warehouse, email_warehouse, login_warehouse,
                    password_warehouse)
        self.admin_panel.users_warehouse.append(user)
        self.admin_panel.save_data()
        tkinter.messagebox.showinfo(title="Qeydiyyat", message="Siz müvəffəqiyətlə qeydiyyat keçdiniz!")
        self.back_to_warehouse_menu2()

    def back_to_warehouse_menu2(self):
        self.warehouseRegisterFrame.pack_forget()
        self.warehouseFrame.pack()

    def back_to_root(self):
        self.warehouseFrame.pack_forget()
        self.rootFrame.pack()

    def warehouse_sign_in(self):
        self.warehouseFrame.pack_forget()
        self.loginWarehouseFrame = Frame(self.root, width=600, height=500)
        self.loginWarehouseFrame.pack()

        self.icon_title_Warehouse_Login_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleWarehouse_Login_Frame = Label(self.loginWarehouseFrame, text="Məlumatları daxil edin",
                                                image=self.icon_title_Warehouse_Login_Frame, compound=LEFT,
                                                font=("times new roman", 30, "bold"), bg="#010c48", fg="white",
                                                anchor="w", padx=20)
        self.titleWarehouse_Login_Frame.place(x=0, y=0, relwidth=1, height=70)

        self.back_btn_to_warehouse = Button(self.loginWarehouseFrame, text="< Geri", bg='red', fg='white',
                                            activebackground="dark orange", font=("", 12, "bold"),
                                            command=self.back_to_warehouse_menu)
        self.back_btn_to_warehouse.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.loginwarehousePhoto = Image.open("register_warehouse.png")
        self.loginwarehousePhoto = self.loginwarehousePhoto.resize((100, 100))
        self.loginwarehousePhoto = ImageTk.PhotoImage(self.loginwarehousePhoto)
        self.loginwarehousePhoto_lbl_menulogo = Label(self.loginWarehouseFrame, image=self.loginwarehousePhoto)
        self.loginwarehousePhoto_lbl_menulogo.place(relx=0.45, rely=0.15)

        self.loginFrame = Frame(self.loginWarehouseFrame, bg='#044F67')
        self.loginFrame.place(relx=0.2, rely=0.44, relwidth=0.62, relheight=0.20)

        self.lbl_login_warehouse_sign = Label(self.loginFrame, font=("goudy old style", 15,), text="Login ID : ",
                                              bg='#044F67', fg='white')
        self.lbl_login_warehouse_sign.place(relx=0.05, rely=0.1)
        self.en_login_warehouse_sign = Entry(self.loginFrame, font=("goudy old style", 15,), bg="lightyellow")
        self.en_login_warehouse_sign.place(relx=0.3, rely=0.1, relwidth=0.62)

        self.lbl_warehouse_password_sign = Label(self.loginFrame, font=("goudy old style", 15,), text="Şifrə : ",
                                                 bg='#044F67', fg='white')
        self.lbl_warehouse_password_sign.place(relx=0.05, rely=0.5)
        self.en_warehouse_password_sign = Entry(self.loginFrame, font=("goudy old style", 15,), bg="lightyellow",
                                                show="*")
        self.en_warehouse_password_sign.place(relx=0.3, rely=0.5, relwidth=0.62)

        self.SubmitBtn_warehouse = Button(self.loginWarehouseFrame, text="Daxil ol", bg='#264348', fg='white',
                                          activebackground="dark orange", command=self.warehouse_menu)
        self.SubmitBtn_warehouse.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    def warehouse_menu(self):
        entered_login = self.en_login_warehouse_sign.get()
        entered_password = self.en_warehouse_password_sign.get()

        if not (entered_login and entered_password):
            tkinter.messagebox.showerror("Xəta", "Xanaları doldurun!")
            return

        login_successful = False
        for user in self.admin_panel.users_warehouse:
            if user.validate_login(entered_login, entered_password):
                login_successful = True
                break

        if login_successful:
            tkinter.messagebox.showinfo("Mesaj", "Siz Anbardar panelinə daxil oldunuz!")
            self.en_login_warehouse_sign.delete(0, tkinter.END)
            self.en_warehouse_password_sign.delete(0, tkinter.END)
            self.loginWarehouseFrame.pack_forget()
            self.wareMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
            self.wareMenuFrame.place(x=10, y=10, width=450, height=480)
            self.root.geometry("1100x500+0+0")
            self.root.config(bg="white")


            self.p_frame = Frame(self.root, bg="red", width=700, height=1350)
            self.p_frame.place(x=480, y=100)
            self.my_listbox = tkinter.Listbox(self.p_frame, width=100, height=24, bg="lightyellow")
            self.my_listbox.pack()

            self.searchFrame = LabelFrame(self.root, text="Məhsul Axtarışı", bg="white")
            self.searchFrame.place(x=480, y=10, width=600, height=80)

            self.lbl_search = tkinter.Label(self.searchFrame, text="Məhsulun adını\n daxil edin:",
                                            font=("goudy old style", 15), bg="white")
            self.lbl_search.place(x=15, y=2)
            self.entry_search = Entry(self.searchFrame, font=("goudy old style", 15), bg="lightyellow")
            self.entry_search.place(x=200, y=10)
            self.btn_search = Button(self.searchFrame, text="Axtar", font=("goudy old style", 15), bg="#4caf50",
                                     fg="white", cursor="hand2", command=self.search)
            self.btn_search.place(x=450, y=9, width=100, height=30)

            self.title = Label(self.wareMenuFrame, text="ANBAR PANELİ", font=("goudy old style", 18), bg="#0f4d7d",
                               fg="white")
            self.title.pack(side=TOP, fill=X)

            self.lbl_category_warehouse = Label(self.wareMenuFrame, text="Kateqoriya:", font=("goudy old style", 18),
                                                bg="white")
            self.lbl_category_warehouse.place(x=30, y=60)
            self.lbl_supplier_warehouse = Label(self.wareMenuFrame, text="Şirkət:", font=("goudy old style", 18),
                                                bg="white")
            self.lbl_supplier_warehouse.place(x=30, y=110)
            self.lbl_productName_warehouse = Label(self.wareMenuFrame, text="Ad:", font=("goudy old style", 18),
                                                   bg="white")
            self.lbl_productName_warehouse.place(x=30, y=160)
            self.lbl_price_warehouse = Label(self.wareMenuFrame, text="Qiymət:", font=("goudy old style", 18),
                                             bg="white")
            self.lbl_price_warehouse.place(x=30, y=210)
            self.lbl_quantity_warehouse = Label(self.wareMenuFrame, text="Miqdar:", font=("goudy old style", 18),
                                                bg="white")
            self.lbl_quantity_warehouse.place(x=30, y=260)

            self.en_kategory_warehouse = Entry(self.wareMenuFrame, font=("goudy old style", 15,), bg="lightyellow")
            self.en_kategory_warehouse.place(x=170, y=60, width=200)
            self.en_supplier_warehouse = Entry(self.wareMenuFrame, font=("goudy old style", 15,), bg="lightyellow")
            self.en_supplier_warehouse.place(x=170, y=110, width=200)
            self.en_productName_warehouse = Entry(self.wareMenuFrame, font=("goudy old style", 15,), bg="lightyellow")
            self.en_productName_warehouse.place(x=170, y=160, width=200)
            self.en_price_warehouse = Entry(self.wareMenuFrame, font=("goudy old style", 15,), bg="lightyellow")
            self.en_price_warehouse.place(x=170, y=210, width=200)
            self.en_count_warehouse = Entry(self.wareMenuFrame, font=("goudy old style", 15,), bg="lightyellow")
            self.en_count_warehouse.place(x=170, y=260, width=200)

            self.btn_add = Button(self.wareMenuFrame, text="Əlavə et", font=("goudy old style", 15), bg="#2196f3",
                                  fg="white", cursor="hand2", command=self.add_product)
            self.btn_add.place(x=10, y=400, width=100, height=40)
            self.btn_update = Button(self.wareMenuFrame, text="Dəyişdir", font=("goudy old style", 15), bg="#4caf50",
                                     fg="white", cursor="hand2", command=self.change)
            self.btn_update.place(x=120, y=400, width=100, height=40)
            self.btn_delete = Button(self.wareMenuFrame, text="Sil", font=("goudy old style", 15), bg="#f44336",
                                     fg="white", cursor="hand2", command=self.delete_product)
            self.btn_delete.place(x=230, y=400, width=100, height=40)
            self.btn_back_warehouse = Button(self.wareMenuFrame, text="Geri", font=("goudy old style", 15),
                                             bg="#607d8b", fg="white", cursor="hand2",
                                             command=self.back_to_from_warehouse_menu_to_login)
            self.btn_back_warehouse.place(x=340, y=400, width=100, height=40)

            for product in self.admin_panel.siyahiBack:
                frontItem = f"Kateqoriya: {product.get_kategory()}, Şirkət: {product.get_supplier()}, Məhsulun adı: {product.get_name()}, Qiymət: {product.get_price()} AZN, Say: {product.get_count()} ədəd"
                self.my_listbox.insert(tkinter.END, frontItem)
        else:
            tkinter.messagebox.showerror("Yanlis", "Siz login ve parolu yanlis girdiniz!")

    def back_to_warehouse_menu(self):
        self.loginWarehouseFrame.pack_forget()
        self.warehouseFrame.pack()

    def back_to_from_warehouse_menu_to_login(self):
        self.wareMenuFrame.place_forget()
        self.searchFrame.place_forget()
        self.p_frame.place_forget()
        self.root.geometry("600x500")
        self.loginWarehouseFrame.pack()

    def add_product(self):
        name = self.en_productName_warehouse.get()
        supplier = self.en_supplier_warehouse.get()
        kategory = self.en_kategory_warehouse.get()
        price = self.en_price_warehouse.get()
        count = self.en_count_warehouse.get()

        if not name or not supplier or not kategory or not price or not count:
            tkinter.messagebox.showerror(title="Xəta mesajı!", message="Bütün xanaları doldurun!")
            return

        try:
            price = float(price)
            count = int(count)
        except ValueError:
            tkinter.messagebox.showerror(title="Xəta mesajı!",
                                         message="Qiymət rəqəm olmalı və miqdar tam rəqəm olmalıdır!")
            return

        new_product = Product(kategory, supplier, name, price, count)

        for product in self.admin_panel.siyahiBack:
            if (product.get_name() == name and product.get_supplier() == supplier and
                    product.get_kategory() == kategory and product.get_price() == price):
                tkinter.messagebox.showerror(title="Xəta", message="Bu məhsul siyahıda var!")
                return

        self.admin_panel.siyahiBack.append(new_product)


        frontItem = f"Kateqoriya: {new_product.get_kategory()}, Şirkət: {new_product.get_supplier()}, Məhsulun adı: {new_product.get_name()}, Qiymət: {new_product.get_price()} AZN, Say: {new_product.get_count()} ədəd"
        self.my_listbox.insert(tkinter.END, frontItem)
        tkinter.messagebox.showinfo(message=f"{name} adlı məhsul siyahıya əlavə olundu", title="Info")

        self.admin_panel.save_data()
        self.clear_entries()

    def delete_product(self):
        selection_indices = self.my_listbox.curselection()
        if selection_indices:
            index = int(selection_indices[0])

            if 0 <= index < len(self.admin_panel.siyahiBack):
                deleted_item = self.admin_panel.siyahiBack.pop(index)

                self.my_listbox.delete(index)

                self.admin_panel.save_data()
                tkinter.messagebox.showinfo(title="Məlumat",
                                            message=f"'{deleted_item.get_name()}' adlı məhsul siyahıdan silindi!")
            else:
                tkinter.messagebox.showerror(title="Xəta mesajı", message="Seçili indeks listede mevcut değil!")
        else:
            tkinter.messagebox.showerror(title="Xəta mesajı", message="Silmək istədiyiniz məhsulu seçin!")

    def search(self):
        search_term = self.entry_search.get().lower()
        found = False
        for product in self.admin_panel.siyahiBack:
            if product.get_name().lower() == search_term:
                found = True
                tkinter.messagebox.showinfo(title="Axtarış",
                                            message=f"Məhsul Tapıldı: {product.get_name()}\nKateqoriya: {product.get_kategory()}\nŞirkət: {product.get_supplier()}\nQiymət: {product.get_price()} AZN\nSay: {product.get_count()} ədəd")
                break
        if not found:
            tkinter.messagebox.showinfo(title="Məhsul Tapılmadı", message=f"'{search_term}' adlı məhsul tapılmadı.")
        self.entry_search.delete(0, tkinter.END)

    def change(self):
        selection_indices = self.my_listbox.curselection()
        if selection_indices:
            index = int(selection_indices[0])
            old_product = self.admin_panel.siyahiBack[index]
            change_window = Toplevel(self.root)
            change_window.geometry("500x400")
            change_window.title("Məlumat dəyişikliyi")
            change_window.config(bg="white")
            self.root.iconbitmap("anbarlogo.ico")

            title_change = Label(change_window, text="Məlumat dəyişikliyi", font=("", 18), bg="#0f4d7d", fg="white")
            title_change.pack(side="top", fill="x")

            lbl_kategory_warehouse_change = Label(change_window, text="Yeni Kateqoriya", font=("goudy old style", 18),
                                                  bg="white")
            lbl_kategory_warehouse_change.place(x=30, y=60)
            lbl_supplier_warehouse_change = Label(change_window, text="Yeni Şirkət", font=("goudy old style", 18),
                                                  bg="white")
            lbl_supplier_warehouse_change.place(x=30, y=110)
            lbl_productName_warehouse_change = Label(change_window, text="Yeni Ad", font=("goudy old style", 18),
                                                     bg="white")
            lbl_productName_warehouse_change.place(x=30, y=160)
            lbl_price_warehouse_change = Label(change_window, text="Yeni Qiymət", font=("goudy old style", 18),
                                               bg="white")
            lbl_price_warehouse_change.place(x=30, y=210)
            lbl_quantity_warehouse_change = Label(change_window, text="Yeni Miqdar", font=("goudy old style", 18),
                                                  bg="white")
            lbl_quantity_warehouse_change.place(x=30, y=260)

            en_kategory_warehouse_change = Entry(change_window, font=("goudy old style", 15,), bg="lightyellow")
            en_kategory_warehouse_change.place(x=200, y=60, width=200)
            en_supplier_warehouse_change = Entry(change_window, font=("goudy old style", 15,), bg="lightyellow")
            en_supplier_warehouse_change.place(x=200, y=110, width=200)
            en_productName_warehouse_change = Entry(change_window, font=("goudy old style", 15,), bg="lightyellow")
            en_productName_warehouse_change.place(x=200, y=160, width=200)
            en_price_warehouse_change = Entry(change_window, font=("goudy old style", 15,), bg="lightyellow")
            en_price_warehouse_change.place(x=200, y=210, width=200)
            en_count_warehouse_change = Entry(change_window, font=("goudy old style", 15,), bg="lightyellow")
            en_count_warehouse_change.place(x=200, y=260, width=200)

            en_kategory_warehouse_change.insert(0, old_product.get_kategory())
            en_supplier_warehouse_change.insert(0, old_product.get_supplier())
            en_productName_warehouse_change.insert(0, old_product.get_name())
            en_price_warehouse_change.insert(0, old_product.get_price())
            en_count_warehouse_change.insert(0, old_product.get_count())

            def apply_changes():
                new_kategory = en_kategory_warehouse_change.get()
                new_supplier = en_supplier_warehouse_change.get()
                new_name = en_productName_warehouse_change.get()
                new_price = en_price_warehouse_change.get()
                new_count = en_count_warehouse_change.get()

                try:
                    new_price = float(new_price)
                    new_count = int(new_count)
                except ValueError:
                    tkinter.messagebox.showerror(title="Xəta",
                                                 message="Qiymət rəqəm olmalı və miqdar tam sayı olmalıdır!")
                    return

                new_product = Product(new_kategory, new_supplier, new_name, new_price, new_count)
                self.admin_panel.siyahiBack[index] = new_product

                front_item = f"Kateqoriya: {new_product.get_kategory()}, Şirkət: {new_product.get_supplier()}, Məhsulun adı: {new_product.get_name()}, Qiymət: {new_product.get_price()} AZN, Say: {new_product.get_count()} ədəd"
                self.my_listbox.delete(index)
                self.my_listbox.insert(index, front_item)
                tkinter.messagebox.showinfo(title="Məlumat dəyişikliyi", message="Uğurla dəyişdirildi!")
                self.admin_panel.save_data()
                change_window.destroy()

            btn_change = Button(change_window, text="Dəyişdir", font=("goudy old style", 15), bg="#4caf50", fg="white",
                                cursor="hand2", command=apply_changes)
            btn_change.place(x=120, y=350, width=100, height=40)
            btn_quit = Button(change_window, text="Çıxış", font=("goudy old style", 15), bg="#f44336", fg="white",
                              cursor="hand2", command=lambda: change_window.destroy())
            btn_quit.place(x=230, y=350, width=100, height=40)

        else:
            tkinter.messagebox.showwarning(title="Xəta", message="Dəyişdirmək istədiyiniz məhsulu seçin!")

    def clear_entries(self):
        self.en_productName_warehouse.delete(0, tkinter.END)
        self.en_supplier_warehouse.delete(0, tkinter.END)
        self.en_kategory_warehouse.delete(0, tkinter.END)
        self.en_price_warehouse.delete(0, tkinter.END)
        self.en_count_warehouse.delete(0, tkinter.END)

    def seller_login(self):
        self.rootFrame.pack_forget()
        self.sellerFrame = Frame(self.root, width=600, height=500)
        self.sellerFrame.pack()

        self.icon_title_Seller_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleSellerFrame = Label(self.sellerFrame, text="Proqrama Giriş Edin!", image=self.icon_title_Seller_Frame,
                                      compound=LEFT,
                                      font=("times new roman", 30, "bold"), bg="#010c48", fg="white", anchor="w",
                                      padx=20)
        self.titleSellerFrame.place(x=0, y=0, relwidth=1, height=70)

        self.sellerPhoto = Image.open("register.png")
        self.sellerPhoto = self.sellerPhoto.resize((450, 500))
        self.sellerPhoto = ImageTk.PhotoImage(self.sellerPhoto)
        self.sellerPhoto_lbl_menulogo = Label(self.sellerFrame, image=self.sellerPhoto)
        self.sellerPhoto_lbl_menulogo.place(relx=0.4, rely=0.5)

        self.btn_seller_register = Button(self.sellerFrame, text="Qeydiyyat", bg='#010c48', fg='white',
                                          activebackground="dark orange",
                                          font=("", 12, "bold"), command=self.seller_register)
        self.btn_seller_register.place(relx=0.28, rely=0.3, relwidth=0.2, relheight=0.1)

        self.btn_seller_back = Button(self.sellerFrame, text="< Geri", bg='red', fg='white', font=("", 12, "bold"),
                                      command=self.back_to_root_from_seller)
        self.btn_seller_back.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.btn_Login = Button(self.sellerFrame, text="Giriş", bg='#010c48', fg='white',
                                activebackground="dark orange", font=("", 12, "bold"), command=self.seller_sign_in)
        self.btn_Login.place(relx=0.53, rely=0.3, relwidth=0.2, relheight=0.1)

    def seller_register(self):
        self.sellerFrame.pack_forget()
        self.sellerRegisterFrame = Frame(self.root, width=600, height=500)
        self.sellerRegisterFrame.pack()

        self.icon_title_Seller_Register_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleSeller_Register_Frame = Label(self.sellerRegisterFrame, text="Məlumatları daxil edin",
                                                image=self.icon_title_Seller_Register_Frame, compound=LEFT,
                                                font=("times new roman", 30, "bold"), bg="#010c48", fg="white",
                                                anchor="w", padx=20)
        self.titleSeller_Register_Frame.place(x=0, y=0, relwidth=1, height=70)

        self.back_btn_to_seller = Button(self.sellerRegisterFrame, text="< Geri", bg='red', fg='white',
                                         activebackground="dark orange", font=("", 12, "bold"),
                                         command=self.back_to_seller_menu2)
        self.back_btn_to_seller.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.registersellerPhoto = Image.open("register_warehouse.png")
        self.registersellerPhoto = self.registersellerPhoto.resize((100, 100))
        self.registersellerPhoto = ImageTk.PhotoImage(self.registersellerPhoto)
        self.registersellerPhoto_lbl_menulogo = Label(self.sellerRegisterFrame, image=self.registersellerPhoto)
        self.registersellerPhoto_lbl_menulogo.place(relx=0.45, rely=0.15)

        self.labelFrame = Frame(self.sellerRegisterFrame, bg='#044F67')
        self.labelFrame.place(relx=0.2, rely=0.44, relwidth=0.6, relheight=0.42)

        self.name_lbl_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Ad : ", bg='#044F67',
                                     fg='white')
        self.name_lbl_seller.place(relx=0.05, rely=0.05)
        self.en_name_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_name_seller.place(relx=0.3, rely=0.05, relwidth=0.62)

        self.lbl_SurName_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Soyad : ", bg='#044F67',
                                        fg='white')
        self.lbl_SurName_seller.place(relx=0.05, rely=0.2)
        self.en_Surname_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_Surname_seller.place(relx=0.3, rely=0.2, relwidth=0.62)

        self.lbl_fatherName_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Ata adı : ",
                                           bg='#044F67', fg='white')
        self.lbl_fatherName_seller.place(relx=0.05, rely=0.35)
        self.en_fatherName_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_fatherName_seller.place(relx=0.3, rely=0.35, relwidth=0.62)

        self.lbl_login_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Login : ", bg='#044F67',
                                      fg='white')
        self.lbl_login_seller.place(relx=0.05, rely=0.5)
        self.en_login_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_login_seller.place(relx=0.3, rely=0.5, relwidth=0.62)

        self.lbl_email_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Email : ", bg='#044F67',
                                      fg='white')
        self.lbl_email_seller.place(relx=0.05, rely=0.65)
        self.en_email_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_email_seller.place(relx=0.3, rely=0.65, relwidth=0.62)

        self.lbl_password_seller = Label(self.labelFrame, font=("goudy old style", 15), text="Şifrə : ", bg='#044F67',
                                         fg='white')
        self.lbl_password_seller.place(relx=0.05, rely=0.8)
        self.en_password_seller = Entry(self.labelFrame, font=("goudy old style", 15), bg="lightyellow", show="*")
        self.en_password_seller.place(relx=0.3, rely=0.8, relwidth=0.62)

        self.registerBtn = Button(self.sellerRegisterFrame, text="Qeydiyyat ol", activebackground="dark orange",
                                  bg='#264348', fg='white', command=self.register_button_seller)
        self.registerBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    def register_button_seller(self):
        name_seller = self.en_name_seller.get()
        surname_seller = self.en_Surname_seller.get()
        father_name_seller = self.en_fatherName_seller.get()
        email_seller = self.en_email_seller.get()
        login_seller = self.en_login_seller.get()
        password_seller = self.en_password_seller.get()

        if not (
                name_seller and surname_seller and father_name_seller and email_seller and login_seller and password_seller):
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bütün xanaları doldurmalısınız!")
            return
        if len(name_seller) < 3:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Ad minimum 3 simvoldan az olmamalıdır!")
            return
        if len(surname_seller) < 5:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Soyad minimum 5 simvoldan az olmamalıdır!")
            return
        if not name_seller.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Ad yalnız hərflərdən ibarət olmalıdır!")
            return
        if not surname_seller.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Soyad yalnız hərflərdən ibarət olmalıdır!")
            return
        if not father_name_seller.isalpha():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Ata adı yalnız hərflərdən ibarət olmalıdır!")
            return
        if '@' not in email_seller or '.' not in email_seller:
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Doğru bir email daxil edin!")
            return
        if len(login_seller) < 8 or len(login_seller) > 16 or not login_seller.isalnum():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Login minimum 8, maksimum 16 simvoldan ibarət olmalıdır və yalnız hərf və rəqəmlərdən ibarət olmalıdır!")
            return
        if len(password_seller) < 8 or len(password_seller) > 16 or not password_seller.isalnum():
            tkinter.messagebox.showerror(title="Qeydiyyat Xətası",
                                         message="Şifrə minimum 8, maksimum 16 simvoldan ibarət olmalıdır və yalnız hərf və rəqəmlərdən ibarət olmalıdır!")
            return

        for user in self.admin_panel.users_seller:
            if user.get_login() == login_seller:
                tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bu adda Login artıq mövcuddur!")
                return
            if user.get_email() == email_seller:
                tkinter.messagebox.showerror(title="Qeydiyyat Xətası", message="Bu adda email artıq mövcuddur!")
                return

        user = User(name_seller, surname_seller, father_name_seller, email_seller, login_seller, password_seller)
        self.admin_panel.users_seller.append(user)
        self.admin_panel.save_data()
        tkinter.messagebox.showinfo(title="Qeydiyyat", message="Siz müvəffəqiyətlə qeydiyyat keçdiniz!")
        self.back_to_seller_menu2()

    def back_to_seller_menu2(self):
        self.sellerRegisterFrame.pack_forget()
        self.sellerFrame.pack()

    def back_to_root_from_seller(self):
        self.sellerFrame.pack_forget()
        self.rootFrame.pack()

    def seller_sign_in(self):
        self.sellerFrame.pack_forget()
        self.loginSellerFrame = Frame(self.root, width=600, height=500)
        self.loginSellerFrame.pack()

        self.icon_title_Seller_Login_Frame = PhotoImage(file="anbartitlelogonew.png")
        self.titleSeller_Login_Frame = Label(self.loginSellerFrame, text="Məlumatları daxil edin",
                                             image=self.icon_title_Seller_Login_Frame, compound=LEFT,
                                             font=("times new roman", 30, "bold"), bg="#010c48", fg="white", anchor="w",
                                             padx=20)
        self.titleSeller_Login_Frame.place(x=0, y=0, relwidth=1, height=70)

        self.back_btn_to_seller = Button(self.loginSellerFrame, text="< Geri", bg='red', fg='white',
                                         activebackground="dark orange", font=("", 12, "bold"),
                                         command=self.back_to_seller_menu)
        self.back_btn_to_seller.place(relx=0.87, rely=0.03, relwidth=0.10, relheight=0.08)

        self.loginsellerPhoto = Image.open("register_warehouse.png")
        self.loginsellerPhoto = self.loginsellerPhoto.resize((100, 100))
        self.loginsellerPhoto = ImageTk.PhotoImage(self.loginsellerPhoto)
        self.loginsellerPhoto_lbl_menulogo = Label(self.loginSellerFrame, image=self.loginsellerPhoto)
        self.loginsellerPhoto_lbl_menulogo.place(relx=0.45, rely=0.15)

        self.loginFrame = Frame(self.loginSellerFrame, bg='#044F67')
        self.loginFrame.place(relx=0.2, rely=0.44, relwidth=0.62, relheight=0.20)

        self.lbl_login_singIn = Label(self.loginFrame, font=("goudy old style", 15), text="Login : ", bg='#044F67',
                                      fg='white')
        self.lbl_login_singIn.place(relx=0.05, rely=0.1)
        self.en_login_singIn = Entry(self.loginFrame, font=("goudy old style", 15), bg="lightyellow")
        self.en_login_singIn.place(relx=0.3, rely=0.1, relwidth=0.62)

        self.lbl_password_seller_signIN = Label(self.loginFrame, font=("goudy old style", 15), text="Şifrə : ",
                                                bg='#044F67', fg='white')
        self.lbl_password_seller_signIN.place(relx=0.05, rely=0.5)
        self.en_password_seller_signIN = Entry(self.loginFrame, font=("goudy old style", 15), bg="lightyellow",
                                               show="*")
        self.en_password_seller_signIN.place(relx=0.3, rely=0.5, relwidth=0.62)

        self.signIN_buttol_seller = Button(self.loginSellerFrame, text="Daxil ol", bg='#264348', fg='white',
                                           activebackground="dark orange", command=self.seller_menu)
        self.signIN_buttol_seller.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    def seller_menu(self):
        entered_login = self.en_login_singIn.get()
        entered_password = self.en_password_seller_signIN.get()

        if not (entered_login and entered_password):
            tkinter.messagebox.showerror("Xəta", "Xanaları doldurun!")
            return

        login_successful = False
        for user in self.admin_panel.users_seller:
            if user.validate_login(entered_login, entered_password):
                login_successful = True
                break

        if login_successful:
            tkinter.messagebox.showinfo("Mesaj", "Siz Satıcı panelinə daxil oldunuz!")
            self.en_login_singIn.delete(0, tkinter.END)
            self.en_password_seller_signIN.delete(0, tkinter.END)
            self.loginSellerFrame.pack_forget()
            self.sellerMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
            self.sellerMenuFrame.place(x=10, y=10, width=450, height=480)
            self.root.geometry("1100x500+0+0")
            self.root.config(bg="white")

            self.p_frame_seller = Frame(self.root, bg="red", width=700, height=1350)
            self.p_frame_seller.place(x=480, y=100)
            self.my_listbox_seller = tkinter.Listbox(self.p_frame_seller, width=100, height=24, bg="lightyellow")
            self.my_listbox_seller.pack()

            self.searchFrame_seller = LabelFrame(self.root, text="Miqdar", bg="white")
            self.searchFrame_seller.place(x=480, y=10, width=600, height=80)

            self.lbl_search_seller = tkinter.Label(self.searchFrame_seller, text="Məhsulun miqdarını\n daxil edin:",
                                                   font=("goudy old style", 15), bg="white")
            self.lbl_search_seller.place(x=15, y=2)
            self.entry_count_seller = Entry(self.searchFrame_seller, font=("goudy old style", 15), bg="lightyellow")
            self.entry_count_seller.place(x=200, y=10)
            self.btn_counter_seller = Button(self.searchFrame_seller, text="Səbətə At", font=("goudy old style", 15),
                                             bg="#4caf50", fg="white", cursor="hand2", command=self.add_to_basket)
            self.btn_counter_seller.place(x=410, y=9, width=150, height=30)

            self.seller_title = Label(self.sellerMenuFrame, text="SATICI PANELİ", font=("goudy old style", 18),
                                      bg="#0f4d7d", fg="white")
            self.seller_title.pack(side=TOP, fill=X)

            self.basket_label = tkinter.Label(self.sellerMenuFrame, text="SƏBƏTİM", font=("", 18,), fg="black",
                                              bg="white")
            self.basket_label.place(x=125, y=55)
            self.basket_photo = Image.open("sellersebet.png")
            self.basket_logo = ImageTk.PhotoImage(self.basket_photo)
            self.basket_label_logo = tkinter.Label(self.sellerMenuFrame, text="", font=("", 20), image=self.basket_logo,
                                                   bg="white")
            self.basket_label_logo.place(x=80, y=47)

            self.basket_listbox = tkinter.Listbox(self.sellerMenuFrame, width=70, height=14, bg="lightyellow")
            self.basket_listbox.place(x=5, y=100)
            self.total_sum = tkinter.Label(self.sellerMenuFrame, text="Toplam Qiymət:", font=("", 12), bg="white")
            self.total_sum.place(x=110, y=340)

            self.btn_basket = Button(self.sellerMenuFrame, text="Geri", font=("goudy old style", 14), bg="red",
                                     fg="white", cursor="hand2", width=20,
                                     command=self.back_to_from_seller_menu_to_login)
            self.btn_basket.place(x=10, y=400, width=100, height=40)

            self.refresh_btn = Button(self.sellerMenuFrame, text="Yenilə", font=("goudy old style", 14), bg="#2196f3",
                                      fg="white", cursor="hand2", width=20, command=self.refresh_page)
            self.refresh_btn.place(x=120, y=400, width=100, height=40)

            self.btn_delete_seller = Button(self.sellerMenuFrame, text="Sil", font=("goudy old style", 14),
                                            bg="#2196f3", fg="white", cursor="hand2", width=20,
                                            command=self.delete_from_basket)
            self.btn_delete_seller.place(x=230, y=400, width=100, height=40)

            self.btn_buy = Button(self.sellerMenuFrame, text="Satın Al", font=("goudy old style", 14), bg="green",
                                  fg="white", cursor="hand2", width=20, command=self.buy_product)
            self.btn_buy.config(state="disabled")
            self.btn_buy.place(x=340, y=400, width=100, height=40)

            for product in self.admin_panel.siyahiBack:
                frontItem = f"Kateqoriya: {product.get_kategory()}, Şirkət: {product.get_supplier()}, Məhsulun adı: {product.get_name()}, Qiymət: {product.get_price()} AZN, Say: {product.get_count()} ədəd"
                self.my_listbox_seller.insert(tkinter.END, frontItem)
        else:
            tkinter.messagebox.showerror("Yanlis", "Siz login ve şifrəni yanlış daxil etdiniz!")

    def back_to_seller_menu(self):
        self.loginSellerFrame.pack_forget()
        self.sellerFrame.pack()

    def back_to_from_seller_menu_to_login(self):
        self.sellerMenuFrame.place_forget()
        self.searchFrame_seller.place_forget()
        self.p_frame_seller.place_forget()
        self.root.geometry("600x500")
        self.loginSellerFrame.pack()

    def add_to_basket(self):
        selected_indices = self.my_listbox_seller.curselection()
        if selected_indices:
            index_product_seller = int(selected_indices[0])
            count_product = self.entry_count_seller.get()
            try:
                count_product = int(count_product)
            except ValueError:
                tkinter.messagebox.showerror(title="Xəta!", message="Yalnız tam ədəd daxil edin!")
                return
            if count_product <= 0:
                tkinter.messagebox.showerror(title="Xəta!", message="Ədəd 0-dan böyük olmalıdır!")
                return
            product = self.admin_panel.siyahiBack[index_product_seller]
            product_count = int(product.get_count())  # Ensure product_count is an int
            if count_product > product_count:
                tkinter.messagebox.showerror(title="Xəta!", message="Stokda kifayət qədər məhsul yoxdur!")
                return
            self.seller_panel.add_to_basket(product, count_product)
            self.basket_listbox.insert(tkinter.END,
                                       f"Məhsulun adı: {product.get_name()}, Qiyməti: {product.get_price()} AZN, Sayı: {count_product} ədəd")
            self.basket_label.config(text=f"SƏBƏTDƏ ({self.basket_listbox.size()}) məhsul var!")
            self.total_sum.config(text=f"Toplam Qiymət: {self.seller_panel.toplamQiymet} AZN")
            self.entry_count_seller.delete(0, tkinter.END)
            self.refresh_btn.config(state="disabled")
            self.btn_buy.config(state="normal")
        else:
            tkinter.messagebox.showerror(title="Xəta!", message="Səbətə atmaq istədiyiniz\nməhsulu siyahıdan seçin!")

    def delete_from_basket(self):
        selection_indices_basket = self.basket_listbox.curselection()
        if selection_indices_basket:
            index_basket = int(selection_indices_basket[0])
            item_text = self.basket_listbox.get(index_basket)
            count_in_basket = int(item_text.split()[-2])
            product = self.seller_panel.siyahiBack_basket[index_basket]
            self.seller_panel.delete_from_basket(product, count_in_basket)
            self.basket_listbox.delete(index_basket)
            self.basket_label.config(text=f"SƏBƏTDƏ ({self.basket_listbox.size()}) məhsul var!")
            self.total_sum.config(text=f"Toplam Qiymət: {self.seller_panel.toplamQiymet} AZN")
            if self.basket_listbox.size() == 0:
                self.basket_label.config(text="SƏBƏTİM")
                self.total_sum.config(text=f"Toplam Qiymət: {0} AZN")
            else:
                self.basket_label.config(text=f"SƏBƏTDƏ ({self.basket_listbox.size()}) məhsul var!")

    def buy_product(self):
        message = "Satılan məhsullar:\n"
        for product in self.seller_panel.siyahiBack_basket:
            message += f"{product.get_name()} - {product.get_price()} AZN\n"
        message += f"\nToplam Qiymət: {self.seller_panel.toplamQiymet} AZN"
        tkinter.messagebox.showinfo("Satış", message)
        self.admin_panel.save_data()
        self.basket_listbox.delete(0, tkinter.END)
        self.refresh_btn.config(state="normal")
        self.btn_buy.config(state="disabled")
        self.basket_label.config(text=f"SƏBƏTDƏ ({self.basket_listbox.size()}) məhsul var!")
        self.seller_panel.toplamQiymet = 0
        self.total_sum.config(text=f"Toplam Qiymət: {self.seller_panel.toplamQiymet} AZN")

    def refresh_page(self):
        if self.my_listbox:
            self.my_listbox.delete(0, tkinter.END)
        if self.my_listbox_seller:
            self.my_listbox_seller.delete(0, tkinter.END)

        self.admin_panel.load_data()

        if not self.admin_panel.siyahiBack:
            tkinter.messagebox.showerror(title="Xəta", message="Ürünler yüklenemedi. Lütfen tekrar deneyin.")
            return

        for product in self.admin_panel.siyahiBack:
            frontItem = f"Kateqoriya: {product.get_kategory()}, Şirkət: {product.get_supplier()}, Məhsulun adı: {product.get_name()}, Qiymət: {product.get_price()} AZN, Say: {product.get_count()} ədəd"
            if self.my_listbox:
                self.my_listbox.insert(tkinter.END, frontItem)
            if self.my_listbox_seller:
                self.my_listbox_seller.insert(tkinter.END, frontItem)

        tkinter.messagebox.showinfo(title="Məlumat", message="Məhsul siyahısı yeniləndi!")


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
