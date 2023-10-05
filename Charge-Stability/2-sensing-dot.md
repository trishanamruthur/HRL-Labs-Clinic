# Measuring Charge in Quantum Dots

## Motivation

We will explain how charge sensing is useful, such making sure each dot
in a qubit has the desired number of electrons when initializing and measuring
spin states. (mention that the spin-to-charge stuff will be elaborated on
later. possibly link to it, depending on how linear vs. weblike we want to be)

## Cross capacitances

Note how each gate's potential effects all the other gates---annoying when you
want to be able to vary each dot's potential independently, but useful for
measurement. Take a look at the appendix of van der Wiel 2003, and derive
similar equations for a single quantum dot with a single measurement dot.
Link to https://docs.nanoacademic.com/qtcad/theory/leverarm/ to discuss
lever arm matrix for a different approach to how the potentials are linked.

## Dot charge sensors

Briefly mention alternative measurement techniques. (e.g. quantum point 
contacts).

Discuss general structure of the dot charge sensor. Show Eng 2015 rendering of
the potential of a qubit with integrated measurement dot. Show image of SLEDGE
device with labeled measurement dot, source, drain, and barriers.

## Current through the measurement dot

Dot is small enough and temperature low enough that Coulomb blockade is a 
factor, so small potential changes cause noticeable differences in current.

Show and explain the discrete jumps Dodson figure 2.6a (still unclear why
current *decreases* with increasing P_2 voltage over most of the given range).

Figure 2.6b: if you wiggle P_2 voltage and focus on that frequency with a
lock-in amplifier on the current, you can see how the current through the
measurement dot varies with the P_2 voltage. Spikes correspond to jumps in
the previous graph. Possibly refer back to animation from section 1, with
potential or current from a measurement dot added?

## Physical examples

Refer to Blumoff 2022. Discuss Figure 1 and why the source voltage is
modulated. Possibly go over the section on SNR. That requires
discussion of nonlinear transport which is more section 3 or even a
separate section, though.