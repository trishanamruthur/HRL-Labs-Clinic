# Measuring Charge in Quantum Dots

## Motivation

Now that we know that we *can* move electrons into quantum dots, we would like to know how many electrons our in our dots at a given time. In particular, the qubits in a SLEDGE device require three electrons each, usually distributed so one is in each dot. The device cannot be useful unless we know when this is the case. Furthermore, one of the easiest ways to measure the spin of the electrons in the dots is by setting up a situation where the electron in one dot will move to a different dot with an electron only when the electrons have opposite spins. These spin-to-charge mechanisms will be described in more detail later on (TODO: link), but the upshot for now is that these methods rely on being able to measure how many electrons are in a dot.

## Cross capacitances

As we saw in the animation on the previous page (TODO: link), varying the potential of one gate will affect the potential of nearby areas as well. In that example, varying the voltage of a barrier gate also changed the potential of the well and even (very slightly) the other barrier. These interactions are often modeled with a [lever-arm matrix](https://docs.nanoacademic.com/qtcad/theory/leverarm/) cataloguing how sensitive each dot is to each gate's voltage. In fact, not only do the other gates effect a dot's potential, but also the number of electrons in adjacent dots---more electrons means a lower potential. This makes it hard to vary the potential of a dot independently of others'; on the other hand, the phenomenon is extremely useful for measurement using a **dot charge sensor**. 

## Dot charge sensors

```{figure} eng_potential.png
:alt: Dodson Fig 2.6
:height: 250px
:align: center
:name: eng1

A rendering of the potential landscape of a triple dot with an integrated sensor dot. B1 and B2 are baths at slightly different voltages, causing a current to flow through sensor dot M1. The voltages of gates P1, P2, and P3, as well as any electrons in those dots, cause slight changes to the sensor dot's potential. Source: [](https://www.science.org/doi/full/10.1126/sciadv.1500214).
```

A dot charge sensor is a fancy name for a quantum dot placed nearby the quantum dots you want to measure. The sensor dot is hooked up to electrodes at different potentials so a current flows through it. When electrons load into the measured dot, it changes the potential of the sensor dot, and, as we saw on the previous page, the current flowing through the sensor dot is very sensitive to its potential.

```{figure} dodson_DCS.png
:alt: Dodson Fig 2.6
:height: 400px
:align: center
:name: dodson2-6

Source: [](https://arxiv.org/abs/2103.14702).
```

The above figure shows that the current through the measurement dot is affected by the voltage of the second plunger gate, decreasing as the potential rises. Note that it is plausible that the current increases as the potential rises instead, depending on the exact voltages involved (TODO: verify). But, the important thing is that the current jumps at certain places. When an electron loads into the dot under P2, it lowers the potential near it, causing the current to rise (or, in the case where current increases with rising P2 voltage, fall) in a discrete jump as the electron effectively cancels out a portion of the P2 gate's voltage. By counting each of the jumps, we can see how many electrons have been loaded into the dot. Another way to count the electrons is shown in graph (b), where the P2 voltage is varied at a specific frequency in addition to a steady increase. By measuring the current through M1, isolating that same frequency, and measuring its amplitutde, we can see how much the current varies due to changes in the P2 voltage. Mostly it will vary at a smooth and roughly constant rate. But, near voltages where an electron loading event occurs, the current will jump up and down as the electron pops into and out of the P2 dot, causing the spikes in the graph.

## Further Reading

[Fast and high-fidelity state preparation and measurement in triple-quantum-dot spin qubits](https://arxiv.org/abs/2112.09801).