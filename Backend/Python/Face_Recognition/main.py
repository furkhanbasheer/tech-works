
##############################################################################Importer#######################################################################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import playsound
from playsound import playsound
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageTk
import glob

############################################################################# Emailer ######################################################################################################

def send_email_report(file_path, recipient_email):
    try:
        fromaddr = "furkhanbasheer001@gmail.com"  # ✅ Your Gmail here
        password = "zfiq bvil jvqw nhoz"     # ✅ Paste App Password here
        toaddr = "furkhanhtc1@gmail.com"           # ✅ Where to send (e.g., your college email)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Today's Attendance Report"

        # Attach CSV
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
            msg.attach(part)

        # SMTP Connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

        print("📩 Attendance report sent to", toaddr)
    except Exception as e:
        print("❌ Failed to send email:", str(e))

####################################################################### Directory Assurer ###################################################################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#################################Live Clock Updater ##############################################################################################################################################

def tick():
    time_string = time.strftime('%I:%M:%S %p')
    clock.config(text=time_string)
    clock.after(200,tick)

############################################################### Contact Info Popup ##################################################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'furkhanbasheer001@gmail.com' ")

#############################################################Haarcascade File Checker #####################################################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

#################################################################### Password Save & Update Handler ##############################################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################### Password Change UI Window ############################################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("560x160")## popup box 
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)##String
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=240,y=12)## 1st box
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=240, y=47)## 2nd box
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=240, y=82)## 3rd box
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=280, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#################################################################### Password Check for Save Profile (TrainImages) ########################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

############################################################# Entry Clear with Status Reset ###############################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

###################################################################### Face Data Capture & Save ####################################################################################################################
    
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    Id = (txt.get())
    name = (txt2.get())
    
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(1)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)

        # 🔊 Play custom voice after image is taken
        voice_path = f"AudioClips/{name}.wav"
        if os.path.exists(voice_path):
            playsound(voice_path)
        else:
            playsound("AudioClips/Unknown.wav")

        # ✅ Send attendance report after successful image capture
        report_path = f"Attendance/Attendance_{date}.csv"
        

    else:
        res = "Enter Correct name"
        message.configure(text=res)

########################################################### Model Training with Collected Images #########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

########################################################### Face Dataset Loader for Training ##############################################################################################

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

############################################################## Attendance Tracker & Reporter #############################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
                    
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

    # 📤 Send attendance report via email
    csv_path = f"Attendance/Attendance_{date}.csv"
    send_email_report(csv_path, "furkhanbasheer001@gmail.com")

def open_about():
    about_win = tk.Toplevel(window)
    about_win.title("About Us")
    about_win.geometry("400x200")
    about_win.configure(bg="#d9d9d9")

    tk.Label(about_win, text="Smart Attendance System", font=('comic', 14, 'bold'), bg="#d9d9d9").pack(pady=10)
    tk.Label(about_win, text="Developed by Zayan using Face Recognition & AI.", font=('comic', 11), bg="#d9d9d9").pack(pady=5)
    tk.Button(about_win, text="Close", command=about_win.destroy, font=('comic', 10, 'bold')).pack(pady=20)

def open_contact():
    contact_win = tk.Toplevel(window)
    contact_win.title("Contact Us")
    contact_win.geometry("520x470")
    contact_win.configure(bg="#f0f0f0")

    # Title
    tk.Label(contact_win, text="Meet the Developers", font=('comic', 16, 'bold'), bg="#f0f0f0", fg="#333").pack(pady=10)

    # Frame for images
    img_frame = tk.Frame(contact_win, bg="#f0f0f0")
    img_frame.pack(pady=5)

    image_files = glob.glob("ContactImages/*.jpg") + glob.glob("ContactImages/*.png")
    images = []

    for idx, img_path in enumerate(image_files):
        img = Image.open(img_path)
        img = img.resize((150, 150))
        photo = ImageTk.PhotoImage(img)
        images.append(photo)  # Keep reference to avoid garbage collection

        lbl = tk.Label(img_frame, image=photo, bg="#f0f0f0")
        lbl.grid(row=idx//4, column=idx%4, padx=10, pady=10)

    # Email Info
    tk.Label(contact_win, text="Email: akashanand2607@gmail.com", font=('comic', 11), bg="#f0f0f0", fg="#555").pack(pady=10)
    tk.Label(contact_win, text="Email: furkhanbasheer001@gmail.com", font=('comic', 11), bg="#f0f0f0", fg="#555").pack(pady=10)
    tk.Label(contact_win, text="Email: ggokulraj555@gmail.com", font=('comic', 11), bg="#f0f0f0", fg="#555").pack(pady=10)

    # Close Button
    tk.Button(contact_win, text="Close", command=contact_win.destroy, font=('comic', 10, 'bold')).pack(pady=10)

    contact_win.mainloop()
    
######################################## USED STUFFS ############################################################# Global Vars & Date Formatter ################################################################## 

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ######################################################################### GUI Layout & UI Setup ###################################

window = tk.Tk()
window.state('zoomed')
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#080707')

frame1 = tk.Frame(window, bg="#c79cff")
frame1.place(relx=0.09, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#c79cff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Smart Attendance System using Face Recognition in AI", 
                    fg="white", bg="#080707", font=('comic', 29, ' bold '))
message3.pack(pady=(10, 0))


frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.47, rely=0.10, relwidth=0.20, relheight=0.07)##time only ajust rely

frame4 = tk.Frame(window, bg="#c4c6ce")##relx = x axis ,  rely = y axis ,  relwidth = box x axix  ,  relheight = box y axis 
frame4.place(relx=0.27, rely=0.10, relwidth=0.23, relheight=0.07)## day ajustment only relx and rely

datef = tk.Label(
    frame4,
    text=day + " - " + mont[month] + " - " + year , ##day coreection
    fg="#ff61e5",
    bg="#080707",
    width=54,
    height=1,
    font=('comic', 22, ' bold ')
)

datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="#ff61e5",bg="#080707" ,width=55 ,height=1,font=('comic', 22, ' bold '))##time bg
clock.pack(fill='both',expand=1)

tick()



head2 = tk.Label(frame2, text="For New Registrations", fg="black", bg="#00fcca", 
                 font=('comic', 17, ' bold '), anchor="center")
head2.pack(fill='x')


head1 = tk.Label(frame1, text="                             For Already Registered                          ", fg="black",bg="#00fcca",font=('comic', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter Your Roll No",width=20  ,height=1  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold '))
lbl.place(x=190, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=150, y=100)

lbl2 = tk.Label(frame2, text="Enter Your Name",width=20  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold '))
lbl2.place(x=180, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=150, y=185)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#c79cff" ,fg="black"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=75, y=245)

message = tk.Label(frame2, text="" ,bg="#c79cff" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=40, y=470)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#c79cff"  ,height=1 ,font=('comic', 17, ' bold '), anchor="center")
lbl3.place(x=200, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

############################################ MENUBAR ###################################################### Menu Bar Setup (Help Menu) Menu Bar Setup (Help Menu) ###################################

menubar = tk.Menu(window, relief='ridge')

# 🔐 Help Menu
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label='Change Password', command=change_pass)
help_menu.add_separator()
help_menu.add_command(label='Contact Us', command=open_contact)
help_menu.add_separator()
help_menu.add_command(label='About Us', command=open_about)

# ➕ Add Help menu to menubar
menubar.add_cascade(label='Help', menu=help_menu)
window.configure(menu=menubar)

#################################### TREEVIEW ATTENDANCE TABLE ################################################## Treeview: Attendance Display Table ###################################

tv_frame = tk.Frame(frame1, bg="#c79cff")
tv_frame.pack(pady=165, padx=20, fill='x')

# ⬇️ Treeview
tv = ttk.Treeview(tv_frame, height=13, columns=('name','date','time'))
tv.column('#0', width=82, anchor='center')
tv.column('name', width=130, anchor='center')
tv.column('date', width=133, anchor='center')
tv.column('time', width=133, anchor='center')
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')
tv.pack(side='left', fill='both', expand=True)

######################################### SCROLLBAR #################################################################### Scrollbar for Attendance Table ###################################

scroll = ttk.Scrollbar(tv_frame, orient='vertical', command=tv.yview)
scroll.pack(side='right', fill='y')
tv.configure(yscrollcommand=scroll.set)

#scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
#scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
#tv.configure(yscrollcommand=scroll.set)
#scroll.pack(side='right', fill='y')

tv.configure(yscrollcommand=scroll.set)

############################################ BUTTONS ################################################## Core Action Buttons (Clear, Register, Attendance, Quit) ###################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ff7221"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=472, y=99)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ff7221"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=472, y=182)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=120, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=120, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="#3ffc00"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trackImg.place(x=115,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#eb4600"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=115, y=470)

##################### END ##################################################################################################################################################################################

window.configure(menu=menubar)
window.mainloop()

#########################################################################################################################################################################################################
