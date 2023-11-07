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

### Charge Measurements

By placing the M dots (sensor dots) adjacent to the six P dots, any change in the charge occupation of the P dots will affect the [electro-chemical potential](gls:chempot-fermi-e) of the sensor dot. If we allow for a small (yet measureable) current to flow through each sensor dot, then loading and unloading events in the P dots will cause large changes in the current of the sensor dots, allowing us to infer the electron population of the P dots.

### Pairwise Stability Diagrams

We previously discussed stability diagrams in the context of double dots, and the _exact same principles_ apply to these multi-dot arrays as well. In cateloging the functionality of these devices pairwise stability diagrams (exactly like the ones we have shown for double dots) are a crucial tool. To generate these diagrams, two dots will be isolated and have their voltages swept while measuring changes in sensor dot current, which are then plotted on a heatmap with the dot plunger voltages on the axes.

```{figure} ./HA-fig4a.png
---
width: 500px
name: ha-fig4a
---
Figure 4 panel A from the [Ha Ha paper](../../../PDFs/HaHa.pdf). This figure shows how we can measure the gate voltages that yield a certain charge configuration for each dot thanks to our understanding of how to read these stability diagrams.
```

## Small animation


## Summary and Reference
We will include a summary of the topic as well as links to the sources referenced in the above sections, as well as other relevant research that can provide additional information for those who want to dig deeper into the topic. 
