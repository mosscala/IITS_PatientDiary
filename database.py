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

def newuser(email, password, remember, medstaff):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO users VALUES (?,?,?,?)", (email, password, remember, medstaff))

    conn.commit()
    conn.close()


def newappointment(what, when, where, recurring, videolink, additinfo):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO appointments VALUES (?,?,?,?,?,?)", (when, where, what, videolink, additinfo, recurring))

    conn.commit()
    conn.close()

def fetchmeds(patid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM meds WHERE patid LIKE ?", (patid,))
    return c.fetchall()

def fetchhistory(uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM indwb WHERE userid LIKE ?", (uid,))
    return c.fetchall()

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
        medstaffids.append(i[1])
        mednames.append(i[2])
        medbrands.append(i[3])
        admroutes.append(i[4])
        doses.append(i[5])
        indics.append(i[6])
        mornings.append(i[7])
        noons.append(i[8])
        evenings.append(i[9])
        nights.append(i[10])
        addinfos.append(i[11])
    
    fig = go.Figure(data=[go.Table(header=dict(values=["Medication Name", "Brand", "Administer route", "Dose", "Indication", "Morning Dosage", "Noon Dosage", "Evening Dosage", "Night Dosage", "Additional Information", "Prescribed by"]),
                 cells=dict(values=[mednames, medbrands, admroutes, doses, indics, mornings, noons, evenings, nights, addinfos, medstaffids]))
                     ])
       
    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createindhistory(patid):
    
    time = []
    wbscore = []
    symptoms = []
    
    for i in fetchhistory(patid):
        time.append(i[2])
        wbscore.append(i[0])
        symptoms.append(i[1])
    
    fig = go.Figure()

    # Create and style traces
    fig.add_trace(go.Scatter(x=time, y=wbscore, name='Wellbeing Score', mode='lines+markers', hovertext=symptoms))

    # Edit the layout
    fig.update_layout( xaxis_title='Time',
                    yaxis_title='Wellbeing Score',
                )

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

def createappointmenttable():
    fig = go.Figure(data=[go.Table(header=dict(values=['Procedure', 'Location', 'Appointment Time', 'Video', 'Additional Information', 'Recurring']),
                 cells=dict(values=[['Colonoscopy'], ['Department F'], ['2020-12-28 09:56:34'], ['<a href=\'https://www.youtube.com/watch?v=wK2imf6w8Pw\'> Colonoscopy Video</a>'], ['Please make sure to drink the laxatives the evening before! Also no dinner tonight!'], ['No']]))
                     ])
    fig.update_layout(title='Your Appointments')
                
    return plot(fig, include_plotlyjs=False, output_type='div')

#dat = fetchsymptoms()

#print(dat)


#Connecting to database
conn = sqlite3.connect('patientdiary.db')

#Creating the cursor
c = conn.cursor()

#Creating a Table
# c.execute("""CREATE TABLE appointments (
#    aptime text,
#    loc text,
#    proc text,
#    video text,
#    additional text,
#    recurring integer
#    )""")

#Creating a Table
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


# c.execute("""CREATE TABLE users (
#    email text,
#    password text,
#    remember integer,
#    medstaff integer
#    )""")

#Creating a new entry
#c.execute("INSERT INTO howareyou VALUES ('2', 'fever', datetime('now', 'localtime'))")

#Querying the database
#c.execute("SELECT rowid, * FROM howareyou")

#print(c.fetchall())


#Creating a Table
#c.execute("""CREATE TABLE howareyou (
#    wellbeing integer,
#    symptoms text,
#    time text
#    )""")

#Creating a Table
# c.execute("""CREATE TABLE indwb (
#    wellbeing integer,
#    symptoms text,
#    time text,
#    userid int
#    )""")


#Deleting a table
# c.execute("DROP TABLE meds")

#Committing command
conn.commit()

#Closing connection
conn.close()

print(printall())
#print(fetchrowid('a@b.de'))
#print(fetchmedstaff('a@b.de'))
#print(fetchhistory(11))

#createindhistory(11)
