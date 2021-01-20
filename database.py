import sqlite3
import plotly.graph_objects as go
from plotly.offline import plot
   
def printall():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM users")
    #return list(sum(c.fetchall(), ()))
    return c.fetchall()

def fetchemail(inputemail):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email = ? ", (inputemail,))
    
    try:
            return ''.join(c.fetchone())
    except:
        return False

def fetchfullname(rowid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT title, firstname, lastname FROM users WHERE rowid = ? ", (rowid,))
    
    try:
        fullname = c.fetchall()
        fullname = ' '.join(fullname[0])
        return fullname
    except:
        return False

def fetchpassword(inputemail):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT password FROM users WHERE email = ? ", (inputemail,))
        return ''.join(c.fetchone())
    except:
        return False

def fetchmedstaff(inputemail):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT medstaff FROM users WHERE email = ? ", (inputemail,))
        return c.fetchone()[0]
    except:
        return False

def fetchrowid(inputemail):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT rowid, * FROM users WHERE email = ? ", (inputemail,))
        return c.fetchone()[0]
    except:
        return False

def newentry(wbscore, symptom):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO howareyou VALUES (?,?,datetime('now', 'localtime'))", (wbscore, symptom))

    conn.commit()
    conn.close()

def newentrypatient(wbscore, symptom, uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()

    c.execute("INSERT INTO indwb VALUES (?,?,datetime('now', 'localtime'), ?)", (wbscore, symptom, uid))

    conn.commit()
    conn.close()

def newentrymed(patid, medstaffid, medname, medbrand, admroute, dose, indic, morning, noon, evening, night, addinfo):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO meds VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (patid, medstaffid, medname, medbrand, admroute, dose, indic, morning, noon, evening, night, addinfo))

    conn.commit()
    conn.close()

def newuser(email, password, remember, medstaff, title, firstname, lastname):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (None, email, title, firstname, lastname, password, remember, medstaff))

    conn.commit()
    conn.close()

def newappointment(apptime, loc, procedure, link, addinfo, patid, medstaffid):
    for i in (apptime, loc, procedure, link, addinfo, patid, medstaffid):
        print(i)
    
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO appointments VALUES (?,?,?,?,?,?,?,?)", (None, apptime, loc, procedure, link, addinfo, patid, medstaffid))

    conn.commit()
    conn.close()

def deletewbentry(delid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()

    c.execute("DELETE FROM indwb WHERE rowid LIKE ?", (delid,))

    conn.commit()
    conn.close()

def deletemedentry(delid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()

    c.execute("DELETE FROM meds WHERE rowid LIKE ?", (delid,))

    conn.commit()
    conn.close()

def deleteappointmententry(delid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()

    c.execute("DELETE FROM appointments WHERE rowid LIKE ?", (delid,))

    conn.commit()
    conn.close()

def fetchmeds(patid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM meds WHERE patid LIKE ?", (patid,))
    return c.fetchall()

def fetchhistory(uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM indwb WHERE userid LIKE ?", (uid,))
    return c.fetchall()

def fetchappointments(uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM appointments WHERE who LIKE ?", (uid,))
    return c.fetchall()

def fetchpatients():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM users WHERE medstaff LIKE 0")
    return c.fetchall()


def createappointmenttable(uid):

    apptime = []
    loc = []
    what =[]
    videolink = []
    additinfo = []
    medstaffids = []

    for i in fetchappointments(uid):
        apptime.append(i[2])
        loc.append(i[3])
        what.append(i[4])
        #videolink.append(i[4])
        videolink.append('<a href=' + "'" + str(i[5]) + "'" + '>Video Link</a>')
        additinfo.append(i[6])
        medstaffids.append(fetchfullname(i[8]))

        
    fig = go.Figure(data=[go.Table(header=dict(values=["Appointment Time", "Venue", "Name of Procedure", "Link to Video", "Addtional Info", "Prescribed by"]),
                 cells=dict(values=[apptime, loc, what, videolink, additinfo, medstaffids]))
                     ])

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

    # table = from_db_cursor(c)
    # return table

def createappointmenttablestaff(uid):

    rowids = []
    apptime = []
    loc = []
    what =[]
    videolink = []
    additinfo = []
    medstaffids = []

    for i in fetchappointments(uid):
        rowids.append(i[0])
        apptime.append(i[2])
        loc.append(i[3])
        what.append(i[4])
        #videolink.append(i[4])
        videolink.append('<a href=' + "'" + str(i[5]) + "'" + '>Video Link</a>')
        additinfo.append(i[6])
        medstaffids.append(fetchfullname(i[8]))

        
    fig = go.Figure(data=[go.Table(header=dict(values=["Appointment ID", "Appointment Time", "Venue", "Name of Procedure", "Link to Video", "Addtional Info", "Prescribed by"]),
                 cells=dict(values=[rowids, apptime, loc, what, videolink, additinfo, medstaffids]))
                     ])

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

    # table = from_db_cursor(c)
    # return table
    
def createmedtable(uid):
    
    medstaffids = []
    mednames = []
    medbrands = []
    admroutes  = []
    doses = []
    indics = []
    mornings = []
    noons = []
    evenings = []
    nights = []
    addinfos = []
    
    for i in fetchmeds(uid):
        medstaffids.append(fetchfullname(i[2]))
        mednames.append(i[3])
        medbrands.append(i[4])
        admroutes.append(i[5])
        doses.append(i[6])
        indics.append(i[7])
        mornings.append(i[8])
        noons.append(i[9])
        evenings.append(i[10])
        nights.append(i[11])
        addinfos.append(i[12])
    
    fig = go.Figure(data=[go.Table(header=dict(values=["Medication Name", "Brand", "Administer route", "Dose", "Indication", "Morning Dosage", "Noon Dosage", "Evening Dosage", "Night Dosage", "Additional Information", "Prescribed by"]),
                 cells=dict(values=[mednames, medbrands, admroutes, doses, indics, mornings, noons, evenings, nights, addinfos, medstaffids]))
                     ])
       
    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createmedtablestaff(uid):
    
    rowids = []
    medstaffids = []
    mednames = []
    medbrands = []
    admroutes  = []
    doses = []
    indics = []
    mornings = []
    noons = []
    evenings = []
    nights = []
    addinfos = []
    
    for i in fetchmeds(uid):
        rowids.append(i[0])
        medstaffids.append(fetchfullname(i[2]))
        mednames.append(i[3])
        medbrands.append(i[4])
        admroutes.append(i[5])
        doses.append(i[6])
        indics.append(i[7])
        mornings.append(i[8])
        noons.append(i[9])
        evenings.append(i[10])
        nights.append(i[11])
        addinfos.append(i[12])
    
    fig = go.Figure(data=[go.Table(header=dict(values=["Medication ID", "Medication Name", "Brand", "Administer route", "Dose", "Indication", "Morning Dosage", "Noon Dosage", "Evening Dosage", "Night Dosage", "Additional Information", "Prescribed by"]),
                 cells=dict(values=[rowids, mednames, medbrands, admroutes, doses, indics, mornings, noons, evenings, nights, addinfos, medstaffids]))
                     ])
       
    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createindhistory(patid):
    
    time = []
    wbscore = []
    symptoms = []
    
    for i in fetchhistory(patid):
        time.append(i[3])
        wbscore.append(i[1])
        symptoms.append(i[2])
    
    fig = go.Figure()

    # Create and style traces
    fig.add_trace(go.Scatter(x=time, y=wbscore, name='Wellbeing Score', mode='lines+markers', hovertext=symptoms))

    # Edit the layout
    fig.update_layout( xaxis_title='Time',
                    yaxis_title='Wellbeing Score',
                )
    fig.update_layout({"yaxis"+str(i+1): dict(range = [0, 10]) for i in range(4)})

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createindtable(patid):
    
    time = []
    wbscore = []
    symptoms = []
    
    for i in fetchhistory(patid):
        time.append(i[3])
        wbscore.append(i[1])
        symptoms.append(i[2])
    
    fig = go.Figure(data=[go.Table(header=dict(values=["Entry Date", "Score", "Symptoms/Observations"]),
                 cells=dict(values=[time, wbscore, symptoms]))
                     ])
       
    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createindhistorystafftable(patid):
    
    rowid = []
    time = []
    wbscore = []
    symptoms = []
    
    for i in fetchhistory(patid):
        rowid.append(i[0])
        time.append(i[3])
        wbscore.append(i[1])
        symptoms.append(i[2])
    
    fig = go.Figure(data=[go.Table(header=dict(values=["Entry ID", "Entry Date", "Score", "Symptoms/Observations"]),
                 cells=dict(values=[rowid, time, wbscore, symptoms]))
                     ])
       
    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createusertable():

    rowids = []
    firstnames = []
    lastnames = []

    for i in fetchpatients():
        rowids.append(i[0])
        firstnames.append(i[4])
        lastnames.append(i[5])
        
    fig = go.Figure(data=[go.Table(header=dict(values=["Patient ID", "First Name", "Last Name"]),
                 cells=dict(values=[rowids, firstnames, lastnames]))
                     ])

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

    # table = from_db_cursor(c)
    # return table

# def createappointmenttable():
#     fig = go.Figure(data=[go.Table(header=dict(values=['Procedure', 'Location', 'Appointment Time', 'Video', 'Additional Information', 'Recurring']),
#                cells=dict(values=[['Colonoscopy'], ['Department F'], ['2020-12-28 09:56:34'], ['<a href=\'https://www.youtube.com/watch?v=wK2imf6w8Pw\'> Colonoscopy Video</a>'], ['Please make sure to drink the laxatives the evening before! Also no dinner tonight!'], ['No']]))
#                      ])
#     fig.update_layout(title='Your Appointments')
                
#     return plot(fig, include_plotlyjs=False, output_type='div')



#dat = fetchsymptoms()

#print(dat)



#Connecting to database
conn = sqlite3.connect('patientdiary.db')

#Creating the cursor
c = conn.cursor()

# c.execute("""CREATE TABLE users (
#    patient_id integer PRIMARY KEY,
#    email text NOT NULL,
#    title text,
#    firstname text NOT NULL,
#    lastname text NOT NULL,
#    password text NOT NULL,
#    remember integer NOT NULL,
#    medstaff integer NOT NULL
#    )""")

# c.execute("""CREATE TABLE meds (
#    patid integer,
#    medstaffid integer,
#    medname text,
#    medbrand text,
#    admroute text,
#    dose text,
#    indic text,
#    morning real,
#    noon real,
#    evening real,
#    night real,
#    addinfo text
#    )""")

# c.execute("""CREATE TABLE appointments (
#    pid integer PRIMARY KEY,
#    apptime text NOT NULL,
#    loc text NOT NULL,
#    what text NOT NULL,
#    videolink text NOT NULL,
#    additinfo text NOT NULL,
#    who integer,
#    doc_id integer,
#    FOREIGN KEY (who) REFERENCES users (patient_id),
#    FOREIGN KEY (doc_id) REFERENCES users (patient_id)
#    )""")

# c.execute("""CREATE TABLE indwb (
#    wellbeing integer,
#    symptoms text,
#    time text,
#    userid int
#    )""")



#Creating a new entry
#c.execute("INSERT INTO howareyou VALUES ('2', 'fever', datetime('now', 'localtime'))")

#Querying the database
#c.execute("SELECT rowid, * FROM howareyou")

#print(c.fetchall())

# #Creating a Table
# c.execute("""CREATE TABLE indwb (
#    wellbeing integer,
#    symptoms text,
#    time text,
#    userid int
#    )""")


#Deleting a table
# c.execute("DROP TABLE users")

# #Create Users
# c.execute("""CREATE TABLE users (
#    patient_id integer PRIMARY KEY,
#    email text NOT NULL,
#    title text,
#    firstname text NOT NULL,
#    lastname text NOT NULL,
#    password text NOT NULL,
#    remember integer NOT NULL,
#    medstaff integer NOT NULL
#    )""")

#Committing command
conn.commit()

#Closing connection
conn.close()

print(printall())
#print(fetchrowid('a@b.de'))
#print(fetchmedstaff('a@b.de'))
#print(fetchhistory(11))


#createindhistory(11)
print(fetchfullname(1))
createusertable()