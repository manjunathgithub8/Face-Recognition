import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import stream,dash_app
from datetime import date
from datetime import datetime
import threading

# initializations 
cred = credentials.Certificate('face-recognition-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


 
 
#adding first data
def init_db():
    global collectiondb
    collectiondb = db.collection('companies')


def init_company(email):
    global company
    global deptnames,depts,dept   
    deptnames=[]
    print(email)
    query = collectiondb.where('email', '==', email ).get()
    for q in query:
        print(q.id)
        cname=q.id
    company=collectiondb.document(cname)
    global employee,face_data,all_encodings
    employee=company.collection('employees')
    dept=company.collection('department')
    depts=dept.get()
    deptnames=printdept(depts)
    face_data=company.collection('face_data')
    all_encodings = face_data.stream()
    org_face_data(all_encodings)
    generateday()

def generateday():
    global attendance,today,tlist
    tlist={}
    attendance = company.collection('attendance')
    currdate=date.today()
    today=attendance.document(str(currdate))
    print('Today database created')

def printdept(depts):
    deptnamestemp=[]
    for i in depts:
        tempdict=i.to_dict()
        #print(tempdict)
        deptnamestemp.append(tempdict['name'])
    return deptnamestemp

def retdeptlist():
    #print(deptnames)
    return deptnames

def generatempid(deptname):
    deptdict=dept.document(deptname)
    deptdictemp=deptdict.get().to_dict()
    depttot=int(deptdictemp['total'])+1
    deptcode=deptdictemp['code']
    empid=deptcode+'21'+str(depttot)
    #print(empid,type(deptdictemp))
    deptdictemp['total']=depttot
    #print(deptdictemp)
    deptdict.set(deptdictemp)
    return empid

def add_employee(name,role,deptname):
    global employee
    new_emp={
        'name':name,
        'role':role,
        'department':deptname
    }
    empid=generatempid(deptname)
    doc=employee.document(empid)
    doc.set(new_emp)
    return empid


def add_face(uid,jsdoc):
    global face_data    
    face_data.document(uid).set(jsdoc)
    return True
    

def org_face_data(all_encodings):
    names=[]
    facestr=[]
    for doc in all_encodings:
       currdoc=doc.to_dict()
       names.append(currdoc['name'])
       facestr.append(currdoc['face'])
    stream.get_data(names,facestr)
    
def todaylist(currempid,currtime):
    today.set({currempid:currtime }, merge=True)
    print('updated attendance',currempid,currtime)

def get_today_list_db():
    global tlist
    if not tlist:
        print('getting todays list from db')
        tlist=today.get()
        tlist=tlist.to_dict()
    return tlist

def fetch_all_attendance():
    allatt=attendance.stream()
    attend_data={}
    for doc in allatt:
        attend_data[doc.id]=doc.to_dict()
        #print(f'{doc.id} => {doc.to_dict()}')
    return attend_data

def dash_thread():
    attend_data=fetch_all_attendance()
    dash_app.start_dash(attend_data)

def send_dash():
    t2 = threading.Thread(target=dash_thread)
    t2.daemon = True
    t2.start()




print('success')