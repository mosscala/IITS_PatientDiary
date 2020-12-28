import sqlite3
import plotly.graph_objects as go
from plotly.offline import plot

def printall():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM howareyou")
    return list(sum(c.fetchall(), ()))

def newentry(wbscore, symptom):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute(f"INSERT INTO howareyou VALUES (?,?,datetime('now', 'localtime'))", (wbscore, symptom))

    conn.commit()
    conn.close()

def newappointment(what, when, where, recurring, videolink, additinfo):
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    
    c.execute(f"INSERT INTO appointments VALUES (?,?,?,?,?,?)", (when, where, what, videolink, additinfo, recurring))

    conn.commit()
    conn.close()

def fetchtime():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT time FROM howareyou")
    return list(sum(c.fetchall(), ()))

def fetchwbscore():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT wellbeing FROM howareyou")
    return list(sum(c.fetchall(), ()))

def fetchsymptoms():
    conn = sqlite3.connect('patientdiary.db')
    c = conn.cursor()
    c.execute("SELECT symptoms FROM howareyou")
    return list(sum(c.fetchall(), ()))

def createhistory():
    time = fetchtime()
    wbscore = fetchwbscore()
    symptoms = fetchsymptoms()

    fig = go.Figure()

    # Create and style traces
    fig.add_trace(go.Scatter(x=time, y=wbscore, name='Wellbeing Score', mode='lines+markers', hovertext=symptoms))

    # Edit the layout
    fig.update_layout(title='Your Wellbeing',
                    xaxis_title='Time',
                    yaxis_title='Wellbeing Score',
                )
    return plot(fig, include_plotlyjs=False, output_type='div')

def createappointmenttable():

    fig = go.Figure(data=[go.Table(header=dict(values=['Procedure', 'Location', 'Appointment Time', 'Video', 'Additional Information', 'Recurring']),
                 cells=dict(values=[['Colonoscopy'], ['Department F'], ['2020-12-28 09:56:34'], ['https://www.youtube.com/watch?v=wK2imf6w8Pw'], ['Please make sure to drink the laxatives the evening before! Also no dinner tonight!'], ['No']]))
                     ])
                
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

# c.execute("""CREATE TABLE medication (
#    when text,
#    where text,
#    what text,
#    video text
#    )""")

#Creating a new entry
#c.execute("INSERT INTO howareyou VALUES ('2', 'fever', datetime('now', 'localtime'))")

#Querying the database
#c.execute("SELECT rowid, * FROM howareyou")

#print(c.fetchall())

#Committing command
#conn.commit()

#Closing connection
#conn.close()

#Creating a Table
#c.execute("""CREATE TABLE howareyou (
#    wellbeing integer,
#    symptoms text,
#    time text
#    )""")