import prettytable as pt # pip install prettytable

# SQL Connection

import mysql.connector as ms
c1 = ms.connect(host="localhost", user="root", passwd="1234") # update here
cur = c1.cursor()
cur.execute("create database if not exists libmgm")
cur.execute("use libmgm")
cur.execute("create table if not exists books(ID int PRIMARY KEY,Name varchar(30), Author varchar(30), Status varchar(10) default 'Available')")
cur.execute("create table if not exists students(AdmnNo int primary key, Name varchar(30), Class int, password varchar(20))")
cur.execute("create table if not exists teachers(TID int primary key, Name varchar(30),Subject varchar(30), password varchar(20))")
cur.execute("create table if not exists issuedbooks(ID int, DOI date,DOR date, Fine int, StudentID int, TeacherID int, foreign key(ID) references books(ID), foreign key(StudentID) references Students(admnno), foreign key(TeacherID) references Teachers(TID))")
 
def login():
    print('''----------LOGIN/REGISTER----------
            1. Student Login
            2. Teacher Login
            3. Register
            4. Admin
            ''')
    ch = int(input("Enter your choice: "))
    if ch ==1:
        L_admnno = int(input("Enter Admission No: "))
        spass = input("Enter password: ")
        cur.execute("select name from students where admnno =%s and password = %s", (L_admnno,spass))
        res = cur.fetchone()
        print("Welcome,",res[0],"!")
        return "Student", L_admnno
    elif ch == 2:
        T_id = int(input("Enter Teacher ID:"))
        tpass = (input("Enter password: "))
        cur.execute("select name from teachers where TID = %s and password = %s",(T_id,tpass))
        tname = cur.fetchone()
        print("Welcome,",tname[0],"!")
        return "Teacher", T_id
    else:
        return "Other", ch
    
def searchbook():
    sch= int(input('''-----------SEARCH BOOKS-----------
                    1. Search By ID
                    2. Search By Name
                    3. Search By Author
                    Enter your choice: '''))
    if sch == 1:
            sbid = int(input("Enter Book ID: "))
            cur.execute("select * from books where ID=%s",(sbid,))
            search_result = pt.from_db_cursor(cur)
            print(search_result)
    elif sch ==2:
          sbname = (input("Enter Book Name: "))
          cur.execute("select * from books where Name=%s",(sbname,))
          search_result = pt.from_db_cursor(cur)
          print(search_result)
    elif sch ==3:
          sbauth = (input("Enter Author Name: "))
          cur.execute("select * from books where Author=%s",(sbauth,))
          search_result = pt.from_db_cursor(cur)
          print(search_result)

def viewbooks():
      cur.execute("select * from books")
      display=pt.from_db_cursor(cur)
      print(display)
          
def stissue(L_admnno):
    print('''Issue Book By:
        1. ID
        2. Name''')
    isch = int(input("Enter your choice: "))
    if isch == 1:
        isid = int(input("Enter Book ID: "))
        cur.execute("insert into issuedbooks(ID, DOI, StudentID) values(%s, CURRENT_DATE(), %s)", (isid,L_admnno))
        cur.execute("update books set status=\"Issued\" where ID = %s", (isid,))
        c1.commit()
    elif isch == 2:
        isname = input("Enter book name: ")
        cur.execute("select ID from books where Name = %s", (isname,))
        getid = cur.fetchone()
        cur.execute("insert into issuedbooks(ID,DOI, StudentID) values(%s, CURRENT_DATE(), %s)", (getid[0], L_admnno))
        cur.execute("update books set status=\"Issued\" where ID = %s", (getid[0],))
        c1.commit()
       
def tissue(TID):
    print('''Issue Book By:
        1. ID
        2. Name''')
    isch = int(input("Enter your choice: "))
    if isch == 1:
        isid = int(input("Enter Book ID: "))
        cur.execute("insert into issuedbooks(ID, DOI, TeacherID) values(%s, CURRENT_DATE(), %s)", (isid,TID))
        cur.execute("update books set status=\"Issued\" where ID = %s", (isid,))
        c1.commit()
    elif isch == 2:
        isname = input("Enter book name: ")
        cur.execute("select ID from books where Name = %s", (isname,))
        getid = cur.fetchone()
        cur.execute("insert into issuedbooks(ID,DOI, TeacherID) values(%s, CURRENT_DATE(), %s)", (getid[0], TID))
        cur.execute("update books set status=\"Issued\" where ID = %s", (getid,))
        c1.commit()

def breturn(bookid):
     cur.execute("update issuedbooks set DOR = CURRENT_DATE(), Fine = GREATEST(DATEDIFF(CURDATE(), DOI)-7, 0)*10 where ID = %s", (bookid,))
     c1.commit()
     
def pmsg(msg):
    print("=" * 90)
    print("{:^90}".format("++++++++++++++++++++++    %s    ++++++++++++++++++++++" % msg,))
    print("=" * 90)
    