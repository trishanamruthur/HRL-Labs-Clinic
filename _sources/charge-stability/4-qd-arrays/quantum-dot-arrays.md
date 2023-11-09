# Charge Sensing in Quantum Dot Arrays

Now that we understand the [basics of quantum dot operation](../1-load-unload/loading-and-unloading-single-dot.ipynb), [how we can use a 'sensing' dot to infer the presence of an electron in another dot](../2-sensing-dot/sensing-dot.ipynb), and [how multiple quantum dots interact when they are chained in series](../3-double-dot/double-dot.ipynb), we can look at the structure and function of the quantum-dot devices that are being used at HRL today.

## Device Structure

As we have mentioned before, 
```{figure} ./HA-fig1.png
---
height: 400px
name: qd-ha-fig1
---
Figure 1 from the [Ha Ha paper](../../../PDFs/HaHa.pdf) showing the layout of their SLEDGE device, very similar to the design of HRL's devices. Panel A shows the wiring for the gates; and B shows the structure of dots in the layer, the six P dots on the upper section being the actual dots while the X gates define the potential barriers electrons must cross to traverse between dots. Notice also in figure B that there are two M dots with adjacent Z gates - as we will describe here, these M dots enable measurement of charge in the P dots. See the attatched paper for more information on this figure.
```

The layout of the devices used at HRL is described and detailed in the above figure (as well as the accompanying paper) and there isn't a whole lot more to add to the description of it. Let's take a look at how our understanding of quantum dots thus far can be applied to this array of many quantum dots, and how the physical structure of components enables the device to isolate single electrons in the P quantum dots.

## Device Function

### Measuring Loading Events

By placing the sensor dots (M dots) adjacent to the six P dots, any change in the charge occupation of the P dots will affect the [electro-chemical potential](gls:chempot-fermi-e) of the sensor dot. If we allow for a small (yet measureable) current to flow through each sensor dot, then loading and unloading events in the P dots will cause large changes in the current of the sensor dots, as we saw in the [figure from Dodson's paper earlier](dodson2-6).

We won't delve into the specifics here, but in these multi-dot devices, the fact that the distance from each sensor dot to each quantum dot plays a key role in charge sensing. By cleverly modulating the gate voltages and precisely measuring the resulting current shifts in the measurement dots, you can distinguish loading and unloading events between different dots.

### Pairwise Stability Diagrams

We previously discussed stability diagrams in the context of double dots, and the _exact same principles_ apply to these multi-dot arrays as well. In cateloging the functionality of these devices pairwise stability diagrams (exactly like the ones we have shown for double dots) are a crucial tool. To generate these diagrams, two dots will be isolated, which you can imagine as setting the voltages for all of the dots and gates afterwards to match the drain bath voltage, and setting the voltage of all the previous dots and gates to match the source bath voltage. In this configuration, you are essentially just dealing with a [double dot device](../3-double-dot/double-dot.ipynb), and you can treat it in the exact same way. In particular, to classify the behavior of the gates and dots it is typical to make stability diagrams in which the dot voltages are swept while plotting current changes on a heat map. Below is a figure from the [Ha Ha Paper](../../../PDFs/HaHa.pdf) that shows stability diagrams for each pair of adjacent dots in their six quantum dot device.

```{figure} ./HA-fig4a.png
---
width: 500px
name: ha-fig4a
---
Figure 4 panel A from the [Ha Ha paper](../../../PDFs/HaHa.pdf). This figure shows how we can measure the gate voltages that yield a certain charge configuration for each dot thanks to our understanding of how to read these stability diagrams.
```

Notice in the figure above that no two stability diagrams are the same - which is precisely why creating these stability diagrams is so useful in the first place. Due to the inherent bounds on precision of manufacturing, the device will never behave _ideally_, so creating these stability diagrams can be a great way to benchmark the performance of these devices.
