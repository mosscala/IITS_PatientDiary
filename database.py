import sqlite3
import plotly.graph_objects as go
from plotly.offline import plot
from prettytable import from_db_cursor

   
def printall():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM indwb")
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
    
    print(wbscore)
    print(symptom)
    print(uid)
    c.execute("INSERT INTO indwb VALUES (?,?,datetime('now', 'localtime'), ?)", (wbscore, symptom, uid))

    conn.commit()
    conn.close()

def newuser(email, password, remember, medstaff):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO users VALUES (?,?,?,?,?)", (None,email, password, remember, medstaff))

    conn.commit()
    conn.close()


def newappointment(who, what, apptime, loc, recurring, videolink, additinfo, doc_id):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO appointments VALUES (?,?,?,?,?,?,?,?,?)", (None, apptime, loc, what, videolink, additinfo, recurring, who, doc_id))

    conn.commit()
    conn.close()

def fetchhistory(uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM indwb WHERE userid LIKE ?", (uid,))
    return c.fetchall()

def fetchappoinment(who):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE who LIKE ?", (who,))
    return c.fetchall()

def getappointmnets(uid):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE who LIKE ?", (uid,))
    return c.fetchall()


def createplotlytable(uid):

    apptime = []
    loc = []
    what =[]
    videolink = []
    additinfo = []
    recurring = []

    for i in getappointmnets(uid):
        apptime.append(i[1])
        loc.append(i[2])
        what.append(i[3])
        videolink.append(i[4])
        additinfo.append(i[5])
        recurring.append(i[6])

        
    fig = go.Figure(data=[go.Table(header=dict(values=["Appointment Time", "Venue", "Name of Procedure", "Link to Video", "Addtional Info", "Is this Recurring?"]),
                 cells=dict(values=[apptime, loc, what, videolink, additinfo, recurring]))
                     ])

    #fig.show()            
    return plot(fig, include_plotlyjs=False, output_type='div')

    # table = from_db_cursor(c)
    # return table


def createindhistory(uid):
    
    time = []
    wbscore = []
    symptoms = []
    
    for i in fetchhistory(uid):
        time.append(i[2])
        wbscore.append(i[0])
        symptoms.append(i[1])
    
    fig = go.Figure()

    # Create and style traces
    fig.add_trace(go.Scatter(x=time, y=wbscore, name='Wellbeing Score', mode='lines+markers', hovertext=symptoms))

    # Edit the layout
    fig.update_layout(title='Your Wellbeing',
                    xaxis_title='Time',
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

# #Create Users
# c.execute("""CREATE TABLE users (
#    patient_id integer PRIMARY KEY,
#    email text NOT NULL,
#    password text NOT NULL,
#    remember integer NOT NULL,
#    medstaff integer NOT NULL
#    )""")

# #Create appointment 
# c.execute("""CREATE TABLE appointments (
#    pid integer PRIMARY KEY,
#    apptime text NOT NULL,
#    loc text NOT NULL,
#    what text NOT NULL,
#    videolink text NOT NULL,
#    additinfo text NOT NULL,
#    recurring integer,
#    who integer,
#    doc_id integer,
#    FOREIGN KEY (who) REFERENCES users (patient_id),
#    FOREIGN KEY (doc_id) REFERENCES users (patient_id)
#    )""")



#Creating a new entry
#c.execute("INSERT INTO howareyou VALUES ('2', 'fever', datetime('now', 'localtime'))")

#Querying the database
#c.execute("SELECT rowid, * FROM howareyou")

#print(c.fetchall())


# #Creating a Table
# c.execute("""CREATE TABLE howareyou (
#    wellbeing integer,
#    symptoms text,
#    time text
#    )""")

# #Creating a Table
# c.execute("""CREATE TABLE indwb (
#    wellbeing integer,
#    symptoms text,
#    time text,
#    userid int
#    )""")

#Committing command
conn.commit()

#Closing connection
conn.close()

#Deleting a table
#c.execute("DROP TABLE users")


#print(printall())
#print(fetchrowid('a@b.de'))
#print(fetchmedstaff('a@b.de'))
#print(fetchhistory(11))

#createindhistory(11)