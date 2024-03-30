#Database Design
#Database product---->SQLite(easy to use,portable)
#Tables
#accounts
#acn_no int primary key auto increment
#acn_user text
#acn_pass text
#acn_type text
#acn_bal float
#acn_opendate text
#acn_email text
#acn_mob text
#txns
#txn_acn_no int
#txn_amt float
#txn_type text
#txn_update_bal float
#txn_date text


from tkinter import *
from tkinter.ttk import Combobox,Treeview,Style,Scrollbar
from tkinter import messagebox
import time
import sqlite3
import re

try:
    conobj=sqlite3.connect(database="banking.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table accounts(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_type text,acn_opendate)")
    curobj.execute("create table txns(acn_no int,txn_amt float,txn_type text,txn_updatebal float,txn_date text)")
    conobj.commit()
    print("tables created")
except:
    print("something went worng,might be table exists")
conobj.close()


win=Tk()
win.state('zoomed')
win.configure(bg='powder blue')
win.resizable(width=False,height=False)

title_lbl=Label(win,text="Banking Automation",font=('arial',60,'bold','underline'),bg='powder blue')
title_lbl.pack()
                
date_lbl=Label(win,text=time.strftime("%d %B,%y",time.localtime()),font=('arial',15,'bold'),bg='powder blue')
date_lbl.place(relx=.9,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def newclick():
        frm.destroy()
        openaccount_screen()

    def clear():
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        acn_entry.focus()

    def recover_click():
        frm.destroy()
        recoverpass_screen()

    def login_click():
        acn=acn_entry.get()
        pwd=pass_entry.get()

        if len(acn)==0 or len(acn)==0:
            messagebox.showerror("Validation","Empty filelds are not allowed!")
            return 
        elif not acn.isdigit():
            messagebox.showerror("Login","Incorrect ACN ")
            return 
        else:
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from accounts where acn_no=? and acn_pass=?",(acn,pwd))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Login","Invalid ACN/Pass !!")
            else:
                global uname,uacn
                uacn=tup[0]
                uname=tup[1]
                frm.destroy()
                welcome_screen()

    acn_lbl=Label(frm,text="ACN",font=('arial',20,'bold'),bg='pink',fg='blue')
    acn_lbl.place(relx=.35,rely=.1)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.45,rely=.1)
    acn_entry.focus()

    pass_lbl=Label(frm,text="PASS",font=('arial',20,'bold'),bg='pink',fg='blue')
    pass_lbl.place(relx=.35,rely=.2)

    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    pass_entry.place(relx=.45,rely=.2)

    btn_login=Button(frm,width=6,command=login_click,text='Login',font=('arial',18,'bold'),bd=5,bg='powder blue')
    btn_login.place(relx=.47,rely=.3)

    btn_clear=Button(frm,width=6,command=clear,text='Clear',font=('arial',18,'bold'),bd=5,bg='powder blue')
    btn_clear.place(relx=.58,rely=.3)

    btn_recoverpass=Button(frm,command=recover_click,width=20,text='Recover Password',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_recoverpass.place(relx=.47,rely=.4)

    btn_newacn=Button(frm,command=newclick,width=20,text='Open New Account',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_newacn.place(relx=.47,rely=.5)

def openaccount_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    btn_back=Button(frm,command=back,text='Back',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_back.place(relx=0,rely=0)
    
    name_lbl=Label(frm,text="Name",font=('arial',20,'bold'),bg='pink',fg='blue')
    name_lbl.place(relx=.35,rely=.1)

    name_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    name_entry.place(relx=.45,rely=.1)
    name_entry.focus()

    pass_lbl=Label(frm,text="Pass",font=('arial',20,'bold'),bg='pink',fg='blue')
    pass_lbl.place(relx=.35,rely=.2)

    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    pass_entry.place(relx=.45,rely=.2)

    email_lbl=Label(frm,text="Email",font=('arial',20,'bold'),bg='pink',fg='blue')
    email_lbl.place(relx=.35,rely=.3)

    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.45,rely=.3)

    mob_lbl=Label(frm,text="Mob",font=('arial',20,'bold'),bg='pink',fg='blue')
    mob_lbl.place(relx=.35,rely=.4)

    mob_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    mob_entry.place(relx=.45,rely=.4)

    cb_lbl=Label(frm,text="Type",font=('arial',20,'bold'),bg='pink',fg='blue')
    cb_lbl.place(relx=.35,rely=.5)

    cb_entry=Combobox(frm,font=('arial',20,'bold'),values=['Saving','Current','FD'])
    cb_entry.current(0)
    cb_entry.place(relx=.45,rely=.5)

    def newacn_db():
        name=name_entry.get()
        pwd=pass_entry.get()
        email=email_entry.get()
        mob=mob_entry.get()
        acntype=cb_entry.get()
        bal=0
        opendate=time.ctime()
        
        if len(name)==0 or len(pwd)==0 or len(email)==0 or len(mob)==0:
            messagebox.showerror("Open Account","Empty fields are not allowed")
            return
        elif not re.fullmatch("[a-zA-Z0-9._]+@[a-zA-Z]+[.][a-zA-Z]+",email):
            messagebox.showerror("Open Account","email is not correct")
            return 
        elif not re.fullmatch("[6-9][0-9]{9}",mob):
            messagebox.showerror("Open Account","Mobile no. is not correct")
            return
        
        import sqlite3
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into accounts(acn_name,acn_pass,acn_email,acn_mob,acn_bal,acn_type,acn_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,acntype,opendate))
        conobj.commit()
        curobj.close()
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from accounts")
        tup=curobj.fetchone()
        conobj.close()
        messagebox.showinfo("New Account",f"Your Account is Opened with ACN={tup[0]}")
        name_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        email_entry.delete(0,"end")
        mob_entry.delete(0,"end")
        name_entry.focus()

    btn_submit=Button(frm,command=newacn_db,text='Submit',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_submit.place(relx=.49,rely=.6)

    btn_clear=Button(frm,command=openaccount_screen,text='Clear',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_clear.place(relx=.59,rely=.6)


def recoverpass_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    def recoverpass_db():
        acn=acn_entry.get()
        email=email_entry.get()
        mob=mob_entry.get()
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from accounts where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Recover Pass","Account does not exist !!")
        else:
            messagebox.showinfo("Recover Pass",f"Your Password={tup[0]}")
        

    btn_back=Button(frm,command=back,text='Back',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_back.place(relx=0,rely=0)
    
    acn_lbl=Label(frm,text="ACN No.",font=('arial',20,'bold'),bg='pink',fg='blue')
    acn_lbl.place(relx=.35,rely=.1)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.45,rely=.1)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",font=('arial',20,'bold'),bg='pink',fg='blue')
    email_lbl.place(relx=.35,rely=.2)

    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.45,rely=.2)

    mob_lbl=Label(frm,text="Mob",font=('arial',20,'bold'),bg='pink',fg='blue')
    mob_lbl.place(relx=.35,rely=.3)

    mob_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    mob_entry.place(relx=.45,rely=.3)

    btn_recover=Button(frm,command=recoverpass_db,text='Recover',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_recover.place(relx=.49,rely=.5)

    btn_clear=Button(frm,command=recoverpass_screen,text='Clear',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_clear.place(relx=.59,rely=.5)


def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def logout():
        res=messagebox.askyesno("Logout","do you want to logout?")
        if res==True:
            frm.destroy()
            main_screen()

    def update_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        def update_db():
            name=name_entry.get()
            pwd=pass_entry.get()
            email=email_entry.get()
            mob=mob_entry.get()
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_no=?",(name,pwd,email,mob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Profile","Profile Updated")
            name_entry.delete(0,"end")
            pass_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            name_entry.focus()
            frm.destroy()
            global uname
            uname=name
            welcome_screen()
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn_no=?",(uacn,))
        tup=curobj.fetchone()
        
        title_lbl=Label(ifrm,text="This is Update Profile Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        name_lbl=Label(ifrm,text="Name",font=('arial',15,'bold'),bg='white',fg='blue')
        name_lbl.place(relx=.1,rely=.2)

        name_entry=Entry(ifrm,width="18",font=('arial',20,'bold'),bd=5)
        name_entry.place(relx=.2,rely=.2)
        name_entry.insert(0,tup[1])

        pass_lbl=Label(ifrm,text="Pass",font=('arial',15,'bold'),bg='white',fg='blue')
        pass_lbl.place(relx=.1,rely=.4)

        pass_entry=Entry(ifrm,width="18",font=('arial',20,'bold'),bd=5)
        pass_entry.place(relx=.2,rely=.4)
        pass_entry.insert(0,tup[2])

        email_lbl=Label(ifrm,text="Email",font=('arial',15,'bold'),bg='white',fg='blue')
        email_lbl.place(relx=.5,rely=.2)
        
        email_entry=Entry(ifrm,width="18",font=('arial',20,'bold'),bd=5)
        email_entry.place(relx=.6,rely=.2)
        email_entry.insert(0,tup[3])

        mob_lbl=Label(ifrm,text="Mob",font=('arial',15,'bold'),bg='white',fg='blue')
        mob_lbl.place(relx=.5,rely=.4)

        mob_entry=Entry(ifrm,width="18",font=('arial',20,'bold'),bd=5)
        mob_entry.place(relx=.6,rely=.4)
        mob_entry.insert(0,tup[4])
        
        btn_update=Button(ifrm,width=8,command=update_db,text='Update',font=('arial',15,'bold'),bd=5,bg='powder blue')
        btn_update.place(relx=.7,rely=.7)

        btn_clear=Button(ifrm,width=8,command=update_screen,text='Clear',font=('arial',15,'bold'),bd=5,bg='powder blue')
        btn_clear.place(relx=.55,rely=.7)

    def checkbal_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_no,acn_bal,acn_opendate from accounts where acn_no=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()


        title_lbl=Label(ifrm,text="This is Check Bal Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        account_lbl=Label(ifrm,text=f"Account No.\t {tup[0]}",font=('arial',15,'bold'),bg='white',fg='blue')
        account_lbl.place(relx=.1,rely=.2)

        availbal_lbl=Label(ifrm,text=f"Available Bal\t {tup[1]}",font=('arial',15,'bold'),bg='white',fg='blue')
        availbal_lbl.place(relx=.1,rely=.35)

        opendate_lbl=Label(ifrm,text=f"ACN Open Date\t {tup[2]}",font=('arial',15,'bold'),bg='white',fg='blue')
        opendate_lbl.place(relx=.1,rely=.50)

        
    def deposit_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        def deposit_db():
            amt=float(amt_entry.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from accounts where acn_no=?",(uacn,))
            tup=curobj.fetchone()
            bal=tup[0]
            curobj.close()
            curobj=conobj.cursor()
            curobj.execute("update accounts set acn_bal=acn_bal+? where acn_no=?",(amt,uacn))
            curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,"Cr",bal+amt,time.ctime()))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit Amt",f"{amt} deposited ")
            amt_entry.delete(0,"end")
            amt_entry.focus()
            
            

        title_lbl=Label(ifrm,text="This is Deposit Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amt",font=('arial',20,'bold'),bg='white',fg='blue')
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.place(relx=.4,rely=.2)

        btn_amt=Button(ifrm,command=deposit_db,text='Submit',font=('arial',15,'bold'),bd=5,bg='powder blue')
        btn_amt.place(relx=.5,rely=.4)

    def withdraw_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        def withdraw_db():
            amt=float(amt_entry.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from accounts where acn_no=?",(uacn,))
            tup=curobj.fetchone()
            bal=tup[0]
            curobj.close()
            if bal>=amt:
                curobj=conobj.cursor()
                curobj.execute("update accounts set acn_bal=acn_bal-? where acn_no=?",(amt,uacn))
                curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,"Db",bal-amt,time.ctime()))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw Amt",f"{amt} Withdraw ")
                amt_entry.delete(0,"end")
                amt_entry.focus()
            else:
                messagebox.showinfo("Withdraw Amt","Insufficient Bal")
                
        title_lbl=Label(ifrm,text="This is Withdraw Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amt",font=('arial',20,'bold'),bg='white',fg='blue')
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.place(relx=.4,rely=.2)

        btn_amt=Button(ifrm,command=withdraw_db,text='Submit',font=('arial',15,'bold'),bd=5,bg='powder blue')
        btn_amt.place(relx=.5,rely=.4)
   
    def transfer_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        def transfer_db():
            amt=float(amt_entry.get())
            toacn=to_entry.get()
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from accounts where acn_no=?",(uacn,))
            tup=curobj.fetchone()
            bal_frm=tup[0]
            curobj.close()

            curobj=conobj.cursor()
            curobj.execute("select acn_bal from accounts where acn_no=?",(toacn,))
            tup=curobj.fetchone()
            bal_to=tup[0]
            curobj.close()

            curobj=conobj.cursor()
            curobj.execute("select acn_no from accounts where acn_no=?",(toacn,))
            tup=curobj.fetchone()
            curobj.close()
            if tup==None:
                messagebox.showerror("Transfer",f"To ACN {toacn} does not exist !")

            else:
                if bal_frm>=amt:
                    curobj=conobj.cursor()
                    curobj.execute("update accounts set acn_bal=acn_bal-? where acn_no=?",(amt,uacn))
                    curobj.execute("update accounts set acn_bal=acn_bal+? where acn_no=?",(amt,toacn))
                    
                    curobj.execute("insert into txns values(?,?,?,?,?)",(uacn,amt,"Db",bal_frm-amt,time.ctime()))
                    curobj.execute("insert into txns values(?,?,?,?,?)",(toacn,amt,"Cr",bal_to+amt,time.ctime()))
                    
                    conobj.commit()
                    conobj.close()
    
                    messagebox.showinfo("Transfer Amt",f"{amt} transfered to ACN {toacn} ")
                    to_entry.delete(0,"end")
                    amt_entry.delete(0,"end")
                    to_entry.focus()
                else:
                    messagebox.showwarning("Withdraw Amt","Insufficient Bal")
                    
                    
        title_lbl=Label(ifrm,text="This is Transfer Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        to_lbl=Label(ifrm,text="To",font=('arial',20,'bold'),bg='white',fg='blue')
        to_lbl.place(relx=.3,rely=.2)

        to_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        to_entry.place(relx=.4,rely=.2)
        
        amt_lbl=Label(ifrm,text="Amt",font=('arial',20,'bold'),bg='white',fg='blue')
        amt_lbl.place(relx=.3,rely=.4)

        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.place(relx=.4,rely=.4)
        
        btn_amt=Button(ifrm,command=transfer_db,text='Submit',font=('arial',15,'bold'),bd=5,bg='powder blue')
        btn_amt.place(relx=.5,rely=.6)

    def txnhistory_screen():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground="black")
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.12,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Txnhistory Screen",font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()

        tv=Treeview(ifrm)
        tv.place(x=0,y=0,relheight=1,relwidth=1)

        style= Style()
        style.configure("Treeview.Heading",font=('Arial',15,'bold'),foreground='black')

        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.98,rely=0,relheight=1)

        tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')

        tv.column('Txn date',width=150,anchor='c')
        tv.column('Txn amount',width=100,anchor='c')
        tv.column('Txn type',width=100,anchor='c')
        tv.column('Updated bal',width=100,anchor='c')

        tv.heading('Txn date',text='Txn date')
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated bal',text='Updated bal')
        
        tv['show']='headings'

        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select txn_date,txn_amt,txn_type,txn_updatebal from txns where acn_no=? ",(uacn,))
        for row in cur:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3]))
            tv.tag_configure('ft',font=('',15))
        con.close()
        
    btn_logout=Button(frm,command=logout,text='Logout',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_logout.place(relx=.93,rely=0)

    wel_lbl=Label(frm,text=f"Welcome,{uname}",font=('arial',20,'bold'),bg='pink',fg='blue')
    wel_lbl.place(relx=0,rely=0)

    btn_update=Button(frm,command=update_screen,width=12,text='Update Profile',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_update.place(relx=0,rely=.1)

    btn_bal=Button(frm,command=checkbal_screen,width=12,text='Check Bal',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_bal.place(relx=0,rely=.2)

    btn_deposit=Button(frm,command=deposit_screen,width=12,text='Deposit',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_deposit.place(relx=0,rely=.3)

    btn_withdraw=Button(frm,command=withdraw_screen,width=12,text='Withdraw',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_withdraw.place(relx=0,rely=.4)

    btn_transfer=Button(frm,command=transfer_screen,width=12,text='Transfer',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_transfer.place(relx=0,rely=.5)

    btn_txnhistory=Button(frm,command=txnhistory_screen,width=12,text='Txnhistory',font=('arial',15,'bold'),bd=5,bg='powder blue')
    btn_txnhistory.place(relx=0,rely=.6)

main_screen()
win.mainloop()

