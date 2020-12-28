import plotly.graph_objects as go
from database import *
from plotly.offline import plot



fig = go.Figure(data=[go.Table(header=dict(values=['Procedure', 'Location', 'Appointment Time', 'Video', 'Additional Information', 'Recurring']),
                 cells=dict(values=[['Colonoscopy'], ['Department F'], ['2020-12-28 09:56:34'], ['https://www.youtube.com/watch?v=wK2imf6w8Pw'], ['Please make sure to drink the laxatives the evening before! Also no dinner tonight!'], ['No']]))
                     ])
fig.show()