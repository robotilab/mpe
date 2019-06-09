from IPython.core.display import display, HTML, Markdown, clear_output
import json
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

# Defining Widgets: 
equation = widgets.Text(
            value='seno(X*Y)+coseno(X+Y)',
            placeholder='Escribe la ecuación que quieras visualizar',
            description='Ecuación:')
range_ = widgets.FloatRangeSlider(
    value=[-5, 5],
    min=-100,
    step=0.1,
    description='Rango:',
    orientation='horizontal',
    readout=True,
    readout_format='d',)
points = widgets.IntText(
    value=50,
    description='Detalle:')

# DEFINING FUNCTIONS
def plot2D(x_points):
    # I find where the letter X is in my equation text and replace by placeholders {}
    
    number_of_placeholders = equation.value.count('X')
    decomposed_equation = equation.value.replace('X', '{}')
    y = []
    for point in x_points:
        dicti = {i: point for i in range(number_of_placeholders)}
        decomposed_eq = decomposed_equation.format(*dicti.values())   
        # WARNING: couldn't figure out any other way, let me know if you know
        exec("""global res
res = {}""".format(decomposed_eq))
        y.append(res)
    plt.plot(x_points, y)
    plt.show()

def plot3D(X, Y, Z):
    options = {
        "width": "100%",
        "style": "surface",
        "showPerspective": True,
        "showGrid": True,
        "showShadow": True,
        "keepAspectRatio": False,
        "height": "600px"}
     # LOADING DATA
    data = [ {"x": X[y,x], 
              "y": Y[y,x], 
              "z": Z[y,x]} for y in range(Y.shape[0]) for x in range(Y.shape[1]) ]  
    visual_code = r"""
       <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" type="text/css" rel="stylesheet" />
       <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
       <div id="pos" style="top:0px;left:0px;position:absolute;"></div>
       <div id="visualization"></div>      
       <script type="text/javascript">
        var data = new vis.DataSet();
        data.add(""" + json.dumps(data) + """);
        var options = """ + json.dumps(options) + """;
        var container = document.getElementById("visualization");
        var graph3d = new vis.Graph3d(container, data, options);
        // setting the camera position initial
        graph3d.setCameraPosition({horizontal:0.8197963, vertical:0.945, distance:1.988})
        graph3d.on("cameraPositionChange", function(evt)
        {
            elem = document.getElementById("pos");
            elem.innerHTML = "Horizontal: " + evt.horizontal + "<br>Vertical: " + evt.vertical + "<br>Distancia de la cámara: " + evt.distance;
        });
       </script>
    """
    html= "<iframe srcdoc='"+visual_code+"' width='75%' height='600px' style='border:10;' scrolling='no'> </iframe>"
    display(HTML(html))
    
# CREATING BUTTON
# if X and Y are inside equation.value we run plot3D
# otherwise we run plot2D
button = widgets.Button(description='Muestra gráfica')
out = widgets.Output()
def on_button_clicked(b):
    global X, Y
    with out:
        clear_output()    
        # computing the x points to evaluate our function
        x_points = np.linspace(range_.value[0], 
            range_.value[1], points.value)
        X, Y = np.meshgrid(x_points, x_points)
        # WARNING: couldn't figure out any other way, let me know if you know
        exec("""global Z
Z = {}
""".format(equation.value))
        if 'Y' in equation.value and 'X' in equation.value:
            plot3D(X,Y,Z)
        elif 'Y' in equation.value:
            equation.value = equation.value.replace('Y', 'X')
            plot2D(x_points)
        else:
            plot2D(x_points)    
button.on_click(on_button_clicked)
info = Markdown("""# Gráficas en 2D/3D 
- Escribe la ecuación que quieras visualizar. 
- Si sólo se define $X$ o $Y$ se mostrará el gráfico en 2D.
- Si se define $Y$ y $X$ se mostrará el gráfico en 3D.
""")

gráfica = widgets.VBox([equation, button, out])
conf=widgets.VBox([points, range_])
children = [gráfica, conf]
# initializing a tab
aplic = widgets.Tab()
# setting the tab windows 
aplic.children = children
# changing the title of the first and second window
aplic.set_title(0, 'Gráficas en 2D y 3D')
aplic.set_title(1, 'Configuración')


def seno(a):
    return np.sin(a)

def coseno(a):
    return np.cos(a)