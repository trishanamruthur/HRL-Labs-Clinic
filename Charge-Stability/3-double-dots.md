# Double Quantum Dots

This page will introduce this section which will be all about double quantum dots. Double quantum dots will be an important step in learning about charge sensing and stability in multi-dot systems as they give us the chance to look at the basic principles that govern the exchange of electrons into and out of dots without overwhelming someone who is just learning about this subject. 

## Linear Theory and Model

Our explaination of double quantum dots will focus on the **linear transport regime** as laid out in the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1). This model, essentially an RC circuit, will hopefully feel approachable to electrical engineers and hardware designers who are the target audience for much of this section.

Here we will introduce the model we are working with (figure 1 from [the paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1)) and explain some of the equations that govern the motion of charges in this model, in particular those for the chemical potential of each dot:

```{math}
:label: mu_1
\mu_1 = \left(N_2-\frac{1}{2}\right)E_{C2} + N_1E_{Cm} - \frac{1}{|e|}\left(C_{g1}V_{g1}E_{Cm} + C_{g2}V_{g2}E_{Cm}\right)
```
```{math}
:label: mu_2
\mu_2 = \left(N_2-\frac{1}{2}\right)E_{C2} + N_1E_{Cm} - \frac{1}{|e|}\left(C_{g1}V_{g1}E_{Cm} + C_{g2}V_{g2}E_{Cm}\right)
```

NOTE: these equations can be linked to later on like this: {eq}`mu_1` or {eq}`mu_2`.

## Stability Diagrams

This section will begin to explain what stability diagrams are (in terms of the number of dots in each dot, $N_1$ and $N_2$) _without_ getting into the weeds of how one would go about measuring these. It will also show some examples of what stability diagrams look like (perhaps from figure 2 in the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1)).

### Stability Diagram Demo

This section will include an interactive demo in which you are able to mess with the capacitances in the network (to modify coupling between dots) and see how these changes affect the stability diagram.

This will likely involve linking to a Jupyter Hub being run on the same server as the Book to get the full interactive experience that we are after.

## Quantum Regime

Here we will introduce the quantum regime in which dots have discretized energy levels and discuss how this affects the mechanics of the system as we have discribed them above. This too will rely heavily on the discussion from the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1).

### Discretized Energy Levels Demo

Here we will incorperate a demo that will be a lot like an interactive version of figure 4 from the [Van Der Wiel paper](https://journals.aps.org/rmp/pdf/10.1103/RevModPhys.75.1), allowing users to understand how the quantization of energy levels inside of the dot affects the circumstances in which current is allowed to pass through the dot.

## Summary and Further Resources

Lastly, we will wrap up this section and summarize the key points that will be necessary for the sections going forward.

We will also include resources to learn more about the topics covered in this section at the end.

