# ========== LIBRARY MANAGEMENT SYSTEM ==========
# BY TANUJ SHARMA
import mysql.connector as ms # pip install mysql-connector-python
import libfunctions as lf 
import prettytable as pt  # pip install prettytable

#----------------------------------------------------------------------------------------------------
c1 = ms.connect(host="localhost", user="root", passwd="1234") #update password here as well as in libfunctions.py
cur = c1.cursor()
cur.execute("create database if not exists libmgm")
cur.execute("use libmgm")
cur.execute("create table if not exists books(ID int PRIMARY KEY,Name varchar(30), Author varchar(30), Status varchar(10) default 'Available')")
cur.execute("create table if not exists students(AdmnNo int primary key, Name varchar(30), Class int, password varchar(20))")
cur.execute("create table if not exists teachers(TID int primary key, Name varchar(30),Subject varchar(30), password varchar(20))")
cur.execute("create table if not exists issuedbooks(ID int, DOI date,DOR date, Fine int, StudentID int, TeacherID int, foreign key(ID) references books(ID), foreign key(StudentID) references Students(admnno), foreign key(TeacherID) references Teachers(TID))")
#----------------------------------------------------------------------------------------------------

#-------------------------------------LOGIN---------------------------------------------------
admnpass = "xyz123"
ch = lf.login()

if ch[1] ==3:
      print('''------------SELECT ACCOUNT TYPE--------------
            1. Student
            2. Teacher''')
      ch2 = int(input("Enter your choice[1/2]: "))
      if ch2==1:
            radmnno = int(input("Enter Admission No: "))
            rname = input("Enter Your Name: ")
            rclass = int(input("Enter your class: "))
            rpass = input("Enter Library Password: ")
            cur.execute("insert into students values(%s, %s, %s, %s)", (radmnno,rname,rclass,rpass))
            c1.commit()
            lf.pmsg("Registration Successfull")
            lf.login()
      elif ch2==2:
            rtid = int(input("Enter Teacher ID:"))
            rtname = input("Enter your name: ")
            rsubject = input("Enter your primary subject: ")
            rtpass = input("Enter Library Password: ")
            cur.execute("insert into teachers values(%s,%s,%s,%s)", (rtid,rtname,rsubject,rtpass))
            c1.commit()
            lf.pmsg("Registration Successfull")
            ch = lf.login()

#-------------------------------------LOGIN-------------------------------------------------

#-------------------------------------ADMIN-------------------------------------------------
if ch[1] == 4:
      TestPass = input("Enter admin password: ")
      if TestPass != admnpass:
            print("Wrong password!")
            exit()
      elif TestPass == admnpass:
            ADM_ans = 'y'
            while ADM_ans in 'yY':
                  print('''----------------ADMIN PANEL----------------
                        1. Search Book
                        2. View Books
                        3. Issued Books
                        4. Add Book Record
                        5. Delete Book Record
                        6. Update Book Record''')
                  ADM_ch = int(input("Enter your choice: "))
                  if ADM_ch == 1:
                        lf.searchbook()
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
                  elif ADM_ch ==2:
                        lf.viewbooks()
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
                  elif ADM_ch ==3:
                        cur.execute("select * from issuedbooks")
                        display = pt.from_db_cursor(cur)
                        print(display)
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
                  elif ADM_ch ==4:
                        bid = int(input("Enter Book ID: "))
                        bname = input("Enter Book Name: ")
                        bauth = input("Enter Author's Name: ")
                        cur.execute("insert into books(ID, Name, Author) values(%s,%s,%s)", (bid,bname,bauth))
                        c1.commit()
                        lf.pmsg("Book Added Successfully")
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
                  elif ADM_ch ==5:
                        dch= int(input('''-----------SEARCH BOOKS-----------
                              1. Delete By ID
                              2. Delete By Name
                              3. Delete By Author
                              Enter your choice: '''))
                        if dch == 1:
                              dbid = int(input("Enter Book ID: "))
                              cur.execute("delete from books where ID=%s",(dbid,))
                        elif dch ==2:
                              dbname = (input("Enter Book Name: "))
                              cur.execute("delete from books where Name=%s",(dbname,))
                        elif dch ==3:
                              dbauth = (input("Enter Author Name: "))
                              cur.execute("delete from books where Author=%s",(dbauth,))
                        lf.pmsg("Book Deleted Successfully!")
                        c1.commit()
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
                  elif ADM_ch==6:
                        uid = int(input("Enter Book ID: "))
                        uch = int(input('''What do you want to change?
                                    1. Book Name
                                    2. Book Author
                                    Enter your choice: '''))
                        if uch ==1:
                              newname = input("Enter updated book name: ")
                              cur.execute("update books set Name = %s where ID = %s", (newname,uid))
                              c1.commit()
                        elif uch == 2:
                              newauth = input("Enter updated author name: ")
                              cur.execute("update books set Author = %s where ID = %s", (newauth,uid))
                              c1.commit()
                        lf.pmsg("Book Updated Successfully!")
                        ADM_ans = input("Do you wish to continue?[y/n]: ")
#-------------------------------------ADMIN-------------------------------------------------     

#---------------------------------STUDENTS-------------------------------------------------
if ch[0] == "Student":
      ST_ans = 'y'
      while ST_ans in 'Yy':
            print('''---------------------STUDENT PANEL---------------------
                  1. View Books
                  2. Search Book
                  3. Issue A Book
                  4. Return Book
                  5. My Issued Books
                  6. View Fine''')
            stch = int(input("Enter your choice: "))
            if stch == 1:
                  lf.viewbooks()
                  ST_ans = input("Do you wish to continue?[y/n]: ")
            elif stch == 2:
                  lf.searchbook()
                  ST_ans = input("Do you wish to continue?[y/n]: ")
            elif stch == 3:
                  lf.stissue(ch[1])
                  lf.pmsg("Book Issued Successfully!")
                  ST_ans = input("Do you wish to continue?[y/n]: ")
            elif stch == 4:
                  bookid = int(input("Enter Book ID: ")) #Assuming Book IDs are mentioned on the book.
                  lf.breturn(bookid)
                  lf.pmsg("Book Returned Successfully!")
                  ST_ans = input("Do you wish to continue?[y/n]: ")
            elif stch == 5:
                  cur.execute("select * from issuedbooks where StudentID = %s", (ch[1],))
                  print(pt.from_db_cursor(cur))                
                  ST_ans = input("Do you wish to continue?[y/n]: ") 
            elif stch == 6:
                  cur.execute("select Fine from issuedbooks where StudentID = %s", (ch[1],))
                  fine = cur.fetchall()
                  totalfine = 0
                  for x in fine:
                        if type(x[0]) == int:
                              totalfine+=x[0]
                  print("Fine Due is - ",totalfine)
                  ST_ans = input("Do you wish to continue?[y/n]: ")
#---------------------------------STUDENTS-------------------------------------------------         

#---------------------------------TEACHERS-------------------------------------------------        
if ch[0] == "Teacher":
      T_ans = 'y'
      while T_ans in 'Yy':
            print('''---------------------TEACHER PANEL---------------------
                  1. View Books
                  2. Search Book
                  3. Issue A Book
                  4. Return Book
                  5. My Issued Books
                  6. View Fine''')
            tch = int(input("Enter your choice: "))
            if tch == 1:
                  lf.viewbooks()
                  T_ans = input("Do you wish to continue?[y/n]: ")
            elif tch == 2:
                  lf.searchbook()
                  T_ans = input("Do you wish to continue?[y/n]: ")
            elif tch == 3:
                  lf.tissue(ch[1])
                  lf.pmsg("Book Issued Successfully")
                  T_ans = input("Do you wish to continue?[y/n]: ")
            elif tch == 4:
                  lf.breturn()
                  lf.pmsg("Book Returned Successfully!")
                  T_ans = input("Do you wish to continue?[y/n]: ")
            elif tch == 5:
                  cur.execute("select * from issuedbooks where TeacherID = %s", (ch[1],))
                  print(pt.from_db_cursor(cur))
                  T_ans = input("Do you wish to continue?[y/n]: ")
            elif tch == 6:
                  cur.execute("select Fine from issuedbooks where TeacherID = %s", (ch[1],))
                  fine = cur.fetchall()
                  totalfine = 0
                  for x in fine:
                        if type(x[0]) == int:
                              totalfine+=x[0]
                  print("Fine Due is - ",totalfine)
                  T_ans = input("Do you wish to continue?[y/n]: ")


print("====================================================================================")
print("++++++++++++++++++++++    Thank You For Using Our Service     ++++++++++++++++++++++")
print("====================================================================================")
