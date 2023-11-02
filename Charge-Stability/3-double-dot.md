---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Double Quantum Dots

Double quantum dots are a great educational example, so it is worth spending a while thinking about double-dot systems because general multi-dot systems follow quite naturally.

## Classical Model

It turns out to be quite relevant to be thinking about double quantum dots in the purely classical regime. In the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1) they present a classical model of a double quantum dot system shown in [figure 1](vdw-fig1).

```{figure} ./VDW-fig1.png
---
height: 150px
name: vdw-fig1
---
A classical model of a double quantum dot presented in the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1). The dots are coupled to sources, drains, and each other through a resistor and capacitor in parallel.
```

Obviously, this model simplifies things a _lot_, and is not entirely realistic to the devices that HRL uses [(see comparison)](hrl-vs-vdw), but is still a great way to discuss some of the tools used to understand the operation of these devices.

In the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1), they develop analytical expressions for the chemical potential $\mu$ of each dot in terms of the current electron populations, the gate voltages, and the cross capacitances. These equations are {eq}`mu_1` and {eq}`mu_2`, respectively.

```{math}
:label: mu_1
\mu_1 = \left(N_2-\frac{1}{2}\right)E_{C2} + N_1E_{Cm} - \frac{1}{|e|}\left(C_{g1}V_{g1}E_{Cm} + C_{g2}V_{g2}E_{Cm}\right)
```
```{math}
:label: mu_2
\mu_2 = \left(N_2-\frac{1}{2}\right)E_{C2} + N_1E_{Cm} - \frac{1}{|e|}\left(C_{g1}V_{g1}E_{Cm} + C_{g2}V_{g2}E_{Cm}\right)
```

Note that the energy $E_{C1}$ is the increase in the chemical potential dot 1 when an electron tunnels into it. Likewise, $E_{C2}$ is the increase in the chemical potential of dot 2 when an electron tunnels into it. Lastly, $E_{Cm}$ is the increase in the chemical potential of dot one dot when an electron tunnels into the other dot. By defining the chemical potential of the source and drain to be $\mu=0$, we can understand the behavior of the double dot system using equations {eq}`mu_1` and {eq}`mu_2`. Whenever $\mu_1 < -E_{C1}$, an electron can (and will) tunnel into dot 1 from the source, while whenever $\mu_2 < -E_{C2}$, an electron will tunnel into dot 2 from the drain. This will continue until $0<\mu_1<-E_{C1}$ and $0 < \mu_2 < E_{C2}$. Of course, the only control we have here are the gate voltages for either dot: $V_{g1}$ and $V_{g2}$, and by modulating these controls, we can affect the stable population of electrons in either dot.

## Stability Diagrams

There is a great way to visualize how the voltages $V_{g1}$ and $V_{g2}$ affect the stable populations of the dots: through **stability diagrams**. These diagrams can be a bit hard to interpret so we'll look at the first one together.

```{code-cell}
:tags: [hide-input]

import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, MultiLine
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.resources import CDN
from bokeh.embed import file_html
import IPython

ECHARGE = 1
CG1 = 1
CG2 = 1
CL = 1
CR = 1

CM = 1

C1 = CG1 + CL + CM
C2 = CG2 + CR + CM
EC1 = ECHARGE * ECHARGE / C1 / (1 - CM * CM / C1 / C2)
EC2 = ECHARGE * ECHARGE / C2 / (1 - CM * CM / C2 / C1)
ECM = ECHARGE * ECHARGE / CM / (C1 * C2 / CM / CM - 1)

XLIM = 4
YLIM = 4

v1t1 = []
v2t1 = []
v1t2 = []
v2t2 = []
hexx = []
hexy = []
x1start = ECHARGE * (EC2 / 2 + 0 * ECM - EC1 * EC2 / ECM * (0 + .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
y1start = ECHARGE * (EC1 / 2 + 0 * ECM - EC2 * EC1 / ECM * (0 + .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
x2start = ECHARGE * (-EC2 / 2 + 1 * ECM - EC1 * EC2 / ECM * (1 - .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
y2start = ECHARGE * (-EC1 / 2 + 1 * ECM - EC2 * EC1 / ECM * (1 - .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
deltax = (ECM * ECM - EC1 * EC2) / (ECM * CG1 * ECM - CG1 * EC1 * EC2)
deltay = (ECM * ECM - EC1 * EC2) / (ECM * CG2 * ECM - CG2 * EC1 * EC2)
y1start_save = y1start
y2start_save = y2start
while x1start < XLIM + deltax:
    while y1start < YLIM + deltay:
        v1t1.append(x1start)
        v2t1.append(y1start)
        v1t2.append(x2start)
        v2t2.append(y2start)
        hexx.append( [x1start, x2start, x1start, x2start-deltax, x1start-deltax, x2start-deltax, x1start] )
        hexy.append( [y1start, y2start-deltay, y1start-deltay, y2start-deltay, y1start, y2start, y1start] )
        y1start += deltay
        y2start += deltay
    x1start += deltax
    x2start += deltax
    y1start = y1start_save
    y2start = y2start_save

source = ColumnDataSource(data=dict(v1t1=v1t1, v2t1=v2t1, v1t2=v1t2, v2t2=v2t2, hexx=hexx, hexy=hexy))

plot = figure(y_range=(0, YLIM), x_range=(0, XLIM), width=400, height=400,
              x_axis_label=r"$$V_1\text{ (arbitrary units)}$$",
              y_axis_label=r"$$V_2\text{ (arbitrary units)}$$")

hexagons = MultiLine(xs='hexx', ys='hexy', line_color="black")
plot.add_glyph(source, hexagons)
plot.circle(x='v1t1', y='v2t1', color="blue", source=source)
plot.circle(x='v1t2', y='v2t2', color="red", source=source)

cg1_slider = Slider(start=0.4, end=2, value=1, step=.02, title=r"$$C_{g1}$$")
cg2_slider = Slider(start=0.4, end=2, value=1, step=.02, title=r"$$C_{g2}$$")

callback = CustomJS(args=dict(source=source, ECHARGE=ECHARGE, cg1=cg1_slider, cg2=cg2_slider,
                              cl=1, cr=1, cm=1, XLIM=XLIM, YLIM=YLIM),
                    code="""
    const CM = cm
    const CG1 = cg1.value
    const CG2 = cg2.value
    const CR = cr
    const CL = cl

    const C1 = CG1 + CL + CM
    const C2 = CG2 + CR + CM
    const EC1 = ECHARGE * ECHARGE / C1 / (1 - CM * CM / C1 / C2)
    const EC2 = ECHARGE * ECHARGE / C2 / (1 - CM * CM / C2 / C1)
    const ECM = ECHARGE * ECHARGE / CM / (C1 * C2 / CM / CM - 1)

    const v1t1 = []
    const v2t1 = []
    const v1t2 = []
    const v2t2 = []
    const hexx = []
    const hexy = []
    var x1start = ECHARGE * (EC2 / 2 + 0 * ECM - EC1 * EC2 / ECM * (0 + .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
    var y1start = ECHARGE * (EC1 / 2 + 0 * ECM - EC2 * EC1 / ECM * (0 + .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
    var x2start = ECHARGE * (-EC2 / 2 + 1 * ECM - EC1 * EC2 / ECM * (1 - .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
    var y2start = ECHARGE * (-EC1 / 2 + 1 * ECM - EC2 * EC1 / ECM * (1 - .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
    const deltax = (ECM * ECM - EC1 * EC2) / (ECM * CG1 * ECM - CG1 * EC1 * EC2)
    const deltay = (ECM * ECM - EC1 * EC2) / (ECM * CG2 * ECM - CG2 * EC1 * EC2)
    const y1start_save = y1start
    const y2start_save = y2start
    while (x1start < XLIM + deltax) {
        while (y1start < YLIM + deltay) {
            v1t1.push(x1start)
            v2t1.push(y1start)
            v1t2.push(x2start)
            v2t2.push(y2start)
            hexx.push( [x1start, x2start, x1start, x2start-deltax, x1start-deltax, x2start-deltax, x1start] )
            hexy.push( [y1start, y2start-deltay, y1start-deltay, y2start-deltay, y1start, y2start, y1start] )
            y1start += deltay
            y2start += deltay
        }
        x1start += deltax
        x2start += deltax
        y1start = y1start_save
        y2start = y2start_save
    }

    source.data = { v1t1, v2t1, v1t2, v2t2, hexx, hexy }
""")

cg1_slider.js_on_change('value', callback)
cg2_slider.js_on_change('value', callback)

html_repr = file_html(row(plot, column(cg1_slider, cg2_slider)), CDN)
IPython.display.HTML(html_repr)
```

Above you will find a bit of an interactive stability diagram. On the stability diagram, each line corresponds to a configuration of $V_{g1}$ and $V_{g1}$ where an electron is equally likely to be either in or out of a particular dot. The region at $(0,0)$ bounded by two lines is where there is no electron in either dot. The line to right corresponds to a configuration where an electron we are just as likely to find an electron in dot 1 as we are to find no electron in dot 1. The line on the upper portion of the region corresponds to an equal likelihood of finding one or zero electrons in dot 2. The areas that are blocked out on this diagram then correspond to a certain configuration of electron populations in the dots.

```{figure} ./VDW-fig2b.png
---
height: 300px
name: vdw-fig2b
---
This diagram from figure 2b of the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1) illustrates how the areas bound by the stability diagram correspond to electron populations in each dot.
```

The sliders we have given you to play with in the above stability diagram correspond to the capacitive coupling between each dot and the gates $V_{g1}$ and $V_{g2}$. Increasing the coupling $C_{g1}$ makes it so that a change in $V_{g1}$ is felt more strongly by dot 1, hence the compression of the graph.

Below, we have a version of the same demonstration with more knobs to turn.

```{code-cell}
:tags: [hide-input]

import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, MultiLine
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.resources import CDN
from bokeh.embed import file_html
import IPython

ECHARGE = 1
CG1 = 1
CG2 = 1
CL = 1
CR = 1

CM = 1

C1 = CG1 + CL + CM
C2 = CG2 + CR + CM
EC1 = ECHARGE * ECHARGE / C1 / (1 - CM * CM / C1 / C2)
EC2 = ECHARGE * ECHARGE / C2 / (1 - CM * CM / C2 / C1)
ECM = ECHARGE * ECHARGE / CM / (C1 * C2 / CM / CM - 1)

XLIM = 4
YLIM = 4

v1t1 = []
v2t1 = []
v1t2 = []
v2t2 = []
hexx = []
hexy = []
x1start = ECHARGE * (EC2 / 2 + 0 * ECM - EC1 * EC2 / ECM * (0 + .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
y1start = ECHARGE * (EC1 / 2 + 0 * ECM - EC2 * EC1 / ECM * (0 + .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
x2start = ECHARGE * (-EC2 / 2 + 1 * ECM - EC1 * EC2 / ECM * (1 - .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
y2start = ECHARGE * (-EC1 / 2 + 1 * ECM - EC2 * EC1 / ECM * (1 - .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
deltax = (ECM * ECM - EC1 * EC2) / (ECM * CG1 * ECM - CG1 * EC1 * EC2)
deltay = (ECM * ECM - EC1 * EC2) / (ECM * CG2 * ECM - CG2 * EC1 * EC2)
y1start_save = y1start
y2start_save = y2start
while x1start < XLIM + deltax:
    while y1start < YLIM + deltay:
        v1t1.append(x1start)
        v2t1.append(y1start)
        v1t2.append(x2start)
        v2t2.append(y2start)
        hexx.append( [x1start, x2start, x1start, x2start-deltax, x1start-deltax, x2start-deltax, x1start] )
        hexy.append( [y1start, y2start-deltay, y1start-deltay, y2start-deltay, y1start, y2start, y1start] )
        y1start += deltay
        y2start += deltay
    x1start += deltax
    x2start += deltax
    y1start = y1start_save
    y2start = y2start_save

source = ColumnDataSource(data=dict(v1t1=v1t1, v2t1=v2t1, v1t2=v1t2, v2t2=v2t2, hexx=hexx, hexy=hexy))

plot = figure(y_range=(0, YLIM), x_range=(0, XLIM), width=400, height=400,
              x_axis_label=r"$$V_1\text{ (arbitrary units)}$$",
              y_axis_label=r"$$V_2\text{ (arbitrary units)}$$")

hexagons = MultiLine(xs='hexx', ys='hexy', line_color="black")
plot.add_glyph(source, hexagons)
plot.circle(x='v1t1', y='v2t1', color="blue", source=source)
plot.circle(x='v1t2', y='v2t2', color="red", source=source)

cm_slider = Slider(start=0.02, end=10, value=1, step=.02, title=r"$$C_M$$")
cg1_slider = Slider(start=0.4, end=2, value=1, step=.02, title=r"$$C_{g1}$$")
cg2_slider = Slider(start=0.4, end=2, value=1, step=.02, title=r"$$C_{g2}$$")
cl_slider = Slider(start=0.02, end=10, value=1, step=.02, title=r"$$C_L$$")
cr_slider = Slider(start=0.02, end=10, value=1, step=.02, title=r"$$C_R$$")

callback = CustomJS(args=dict(source=source, ECHARGE=ECHARGE, cg1=cg1_slider, cg2=cg2_slider,
                              cl=cl_slider, cr=cr_slider, cm=cm_slider, XLIM=XLIM, YLIM=YLIM),
                    code="""
    const CM = cm.value
    const CG1 = cg1.value
    const CG2 = cg2.value
    const CR = cr.value
    const CL = cl.value

    const C1 = CG1 + CL + CM
    const C2 = CG2 + CR + CM
    const EC1 = ECHARGE * ECHARGE / C1 / (1 - CM * CM / C1 / C2)
    const EC2 = ECHARGE * ECHARGE / C2 / (1 - CM * CM / C2 / C1)
    const ECM = ECHARGE * ECHARGE / CM / (C1 * C2 / CM / CM - 1)

    const v1t1 = []
    const v2t1 = []
    const v1t2 = []
    const v2t2 = []
    const hexx = []
    const hexy = []
    var x1start = ECHARGE * (EC2 / 2 + 0 * ECM - EC1 * EC2 / ECM * (0 + .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
    var y1start = ECHARGE * (EC1 / 2 + 0 * ECM - EC2 * EC1 / ECM * (0 + .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
    var x2start = ECHARGE * (-EC2 / 2 + 1 * ECM - EC1 * EC2 / ECM * (1 - .5)) / (CG1 * ECM - CG1 * EC1 * EC2 / ECM)
    var y2start = ECHARGE * (-EC1 / 2 + 1 * ECM - EC2 * EC1 / ECM * (1 - .5)) / (CG2 * ECM - CG2 * EC2 * EC1 / ECM)
    const deltax = (ECM * ECM - EC1 * EC2) / (ECM * CG1 * ECM - CG1 * EC1 * EC2)
    const deltay = (ECM * ECM - EC1 * EC2) / (ECM * CG2 * ECM - CG2 * EC1 * EC2)
    const y1start_save = y1start
    const y2start_save = y2start
    while (x1start < XLIM + deltax) {
        while (y1start < YLIM + deltay) {
            v1t1.push(x1start)
            v2t1.push(y1start)
            v1t2.push(x2start)
            v2t2.push(y2start)
            hexx.push( [x1start, x2start, x1start, x2start-deltax, x1start-deltax, x2start-deltax, x1start] )
            hexy.push( [y1start, y2start-deltay, y1start-deltay, y2start-deltay, y1start, y2start, y1start] )
            y1start += deltay
            y2start += deltay
        }
        x1start += deltax
        x2start += deltax
        y1start = y1start_save
        y2start = y2start_save
    }

    source.data = { v1t1, v2t1, v1t2, v2t2, hexx, hexy }
""")

cm_slider.js_on_change('value', callback)
cg1_slider.js_on_change('value', callback)
cg2_slider.js_on_change('value', callback)
cl_slider.js_on_change('value', callback)
cr_slider.js_on_change('value', callback)

html_repr = file_html(row(plot, column(cm_slider, cg1_slider, cg2_slider, cl_slider, cr_slider)), CDN)
IPython.display.HTML(html_repr)
```

### Guiding Questions

```{dropdown} What happens when $\; C_m >> C_{L}, C_{R}$?
In this limit, the distinction between the dots begins to blur. With strongly coupled dots, any change to $V_{g1}$ will be felt by dot 1 just as much as it will be felt by dot 2. It becomes almost pointless to consider a distinction between the (0,1) and the (1,0) configurations, or the (3,0) and the (1,2) configurations. When this case appears in the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1), the lines between such configurations are dashed
```{figure} ./VDW-fig2c.png
---
height: 300px
name: vdw-fig2c
---
This diagram is from figure 2c of the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1).
```


```{dropdown} What happens as $\; C_m\rightarrow 0$?
In this limit, effectively act as individual dots that are not coupled to each other in any way. The lack of diagonal lines on the stability diagram indicates that $V_{g1}$ and $V_{g2}$ are affecting only dot 1 and 2 (respectively), and there is no cross capacitance at all between the dots.
```{figure} ./VDW-fig2a.png
---
height: 300px
name: vdw-fig2a
---
This diagram is from figure 2a of the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1).
```

```{dropdown} What happens as $\;C_R/C_L\rightarrow 0$? Or $\;C_L/C_R\rightarrow 0$?
[TODO: ADD EXPLAINATION]
```

+++

## Quantum Effects

The confinement of electrons into quantum dots means that in reality, and electron cannot just jump into a dot whenever it has enough energy to do so. Quantum dots have a discrete spectrum of allowed energy levels, and so in order for an electron to hop into the dot, it must both have enough energy _and_ there must be an available energy level in the dot for the electron to jump into.

Fortunately, the effect of having discrete energy levels like this within the dot does not affect most of the understanding of stability diagrams that we have been building. These effects mostly appear in the **smoothing out** of the hexagons particularly around the diagonal intersections between $(n,m)$ and $(n+1,m+1)$ configurations, as well as the fuzziness of those diagonal connections in general. These effects are most apparent with a [TODO: LARGER/SMALLER ???] number of electrons in the dots.

```{figure} ./HA-fig4-0.png
---
height: 350px
name: HA-fig4-0
---
Experimental stability diagram from figure 4 in the [Ha Ha paper](https://pubs.acs.org/doi/10.1021/acs.nanolett.1c03026?ref=pdf). Notice the smoothing out of the lines - the areas enclosed are no longer perfect hexagons. Also, notice how the diagonal lines between the $(n,m)$ area and the $(n+1,m+1)$ area are almost non-existent.
```

[TODO: better explain why the lines between $(n,m)$ and $(n+1,m+1)$ are non-existent].

To learn more about these effects, check out the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1) on page 5, section 2 _Quantized States_.

+++

(hrl-vs-vdw)=
## Comparing HRL's Devices to the Van Der Wiel Model

Unlike the model shown in [figure 1](vdw-fig1), HRL's devices _do not use  resistors between dots_. Instead, electrons trying to pass from one dot to the next must overcome a _potential barrier_ which can be raised or lowered by a seperate gate voltage. Furthermore, HRL's devices have more quantum dots in series with each other as well as dots in parallel to those to allow for readout, this process is detailed on the next page [TODO: HOW DOES READOUT HAPPEN].

```{figure} ./HA-fig1.png
---
height: 500px
name: HA-fig1
---
Diagram of the SLEDGE device from figure 1 in the [Ha Ha paper](https://pubs.acs.org/doi/10.1021/acs.nanolett.1c03026?ref=pdf). This diagram is perhaps a bit overly complicated for the point being made, but the key thing to notice is that there are not microscopic resistors seperating the dots (labeled "P" in panel B), but rather smaller dots (labeled "X" in panel B), whose potentials can be raised/lowered to mediate the transport of electrons between dots. See the paper for more information about this diagram.
```

+++

## Cross Capacitances

There is however, a large physical inaccuracy in the Van Der Weil model: each components is only modeled as being capacitively coupled to _adjacent components_. In reality, every electrode on the device will have some capacitance between itself and every other part of the device. In the schematic shown in [figure 1](vdw-fig1), we might imagine adding capacitors between $V_{g2}$ and $N_2$; $V_{g1}$ and $N_1$; $S$ and $N_2$; and $N_1$ and $D$. The notion of every electrical component having some capacitance with every other electrical component is what is referred to by **cross capacitance**. You can imagine how complicated these cross capacitances get when dealing with the number of electrodes shown in [figure 4](HA-fig1).

To demonstrate the effect of these cross capacitances, we have visualized some of the effects in an animation below. We show a device much like the one in [figure 4](HA-fig1) but with only a two dots ($P0$ and $P1$), mediated from the source and the drain by three gates ($X0$, $X1$, and $X2$). We then plot on the $z$-axis the electric potential at every point in the semiconductor layer where electrons live and traverse the device. Then, we show the effects as we wiggle some of the gate voltages. This is not a quantatiative plot, but rather a qualitative demonstration of how small changes in any one of the gate voltages really do affect the potential at every single point in the device. [TODO: more explainations about complications (cross capacitance between the electrodes themselves?)]

```{code-cell}
:tags: [hide-input]

from IPython.display import Video
Video("./gatepot.mp4", embed=True, width=800)
```

## Summary and Further Resources
TODO
