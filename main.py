from urllib.request import urlopen
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.widgets.grids import Grid

URL = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT_CHARS = b'#:'

drawing = Drawing(400, 200)
data = []
for line in urlopen(URL).readlines():
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])
        

pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [row[0] + row[1]/12.0 for row in data]

lp = LinePlot()
lp.gridFirst = True
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [list(zip(times, pred)), list(zip(times, high)), list(zip(times, low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[0].symbol = makeMarker('FilledCircle', size=3)
lp.lines[0].name = 'Predict'
lp.lines[1].strokeColor = colors.red
lp.lines[1].symbol = makeMarker('FilledCircle', size=3)
lp.lines[1].name = 'High'
lp.lines[2].strokeColor = colors.green
lp.lines[2].symbol = makeMarker('FilledCircle', size=3)
lp.lines[2].name = 'Low'

drawing.add(Circle(320, 190, 3, fillColor=colors.blue))
lab = Label()
lab.setOrigin(350,190)
lab.boxAnchor = 'ne'
lab.dx = 5
lab.dy = 7
lab.setText(lp.lines[0].name)
drawing.add(lab)

drawing.add(Circle(320, 180, 3, fillColor=colors.red))
lab = Label()
lab.setOrigin(350,180)
lab.boxAnchor = 'ne'
lab.dx = 5
lab.dy = 7
lab.setText(lp.lines[1].name)
drawing.add(lab)

drawing.add(Circle(320, 170, 3, fillColor=colors.green))
lab = Label()
lab.setOrigin(350,170)
lab.boxAnchor = 'ne'
lab.dx = 5
lab.dy = 7
lab.setText(lp.lines[2].name)
drawing.add(lab)


drawing.add(lp)
drawing.add(String(200, 25, 'Sunspots', fontsize = 14, fillcolr = colors.red))

renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')
