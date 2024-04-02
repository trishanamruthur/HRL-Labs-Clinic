# The Bloch Sphere and Triple Quantum Dot Qubits

As we have already discussed here, HRL's SLEDGE device holds three electrons in three different potential wells (quantum dots) which together encode a single qubit. In this section, we'll be discussing exactly how the spins of these three electrons map to the information of a single qubit.

```{warning}
Please read this section carefully. It is easy to get confused with the different types of qubits out there.
```

## Qubit Encoding

We will try our best not to get too into the weeds here (saving that for another section of this book), but as you hopefully know by now, all electrons have an intrinsic angular momentum known as _spin_. It is **very important to note** that the spin of any individual electron is **not what represents a qubit in our triple quantum dot system**. Instead, _the qubit is informationally encoded in the relative spins of the first two electrons_. Specifically, when the first two electrons are in the singlet state the system is encoding the $\ket{0}$ state, and when they are in the triplet state the system is encoding a $\ket{1}$ state.

````{admonition} But what are singlet and triplet states?
:class: note, dropdown

Most of the details here are beyond the scope of this text (see resources below) but essentially, there are four ways for electron spins to be combined in order to satisfy the spin-statistics theorem. These are
```{math}
\ket{\uparrow\uparrow} \\ \frac{1}{\sqrt{2}}\big(\ket{\uparrow\downarrow} + \ket{\downarrow\uparrow}\big) \\ \ket{\downarrow\downarrow} \\
\frac{1}{\sqrt{2}}\big(\ket{\uparrow\downarrow} - \ket{\downarrow\uparrow}\big)
```
The first three here are symmetric under exchange of particles, and collectively represent the triplet state:
```{math}
\ket{\psi_\text{triplet}} = c_1\ket{\uparrow\uparrow} + c_2\frac{1}{\sqrt{2}}\big(\ket{\uparrow\downarrow} + \ket{\downarrow\uparrow}\big) + c_3\ket{\downarrow\downarrow}
```
Where $c_1$, $c_2$, and $c_3$ satisfy the usual normalization conditions. While the last of these is anti-symmetric under particle exchange, and is the singlet state:
```{math}
\ket{\psi_\text{singlet}} = \frac{1}{\sqrt{2}}\big(\ket{\uparrow\downarrow} - \ket{\downarrow\uparrow}\big)
```

**Resources for further (general quantum mechanics) learning:**
- [Singlets, Triplets, and the Exchange Interaction](https://phys.libretexts.org/Bookshelves/Quantum_Mechanics/Essential_Graduate_Physics_-_Quantum_Mechanics_(Likharev)/08%3A_Multiparticle_Systems/8.02%3A_Singlets_Triplets_and_the_Exchange_Interaction)
- [Spin-statistics Theorem](https://en.wikipedia.org/wiki/Spin%E2%80%93statistics_theorem)
````

## The Bloch Sphere: A _Careful_ Introduction

Generally, a qubit is not in just the $\ket{0}$ or $\ket{1}$ state, but a superposition of the two. Generally, this superposition can be written as
```{math}
\ket{\psi} = \cos\theta\ket{0} + e^{i\phi}\sin\theta\ket{1}
```
Where $\theta$ ranges from $0$ to $\pi$ and $\phi$ from $0$ to $2\pi$. This expression alludes to a fairly clever way to represent any qubit as a vector on a unit sphere in three dimensional space, where $\theta$ is the polar angle and $\phi$ the azimuthal angle.

```{admonition} The Bloch sphere does not exist in physical space!
:class: important
The Bloch sphere is a tool for visualizing qubits and qubit operations, but just because it exists in $\mathbb{R}^3$ does not mean it is in any way connected to physical space.

Saying that a qubit pointing up on the bloch sphere corresponds to something pointing up in the real world is like saying that a stock price going up risks damaging the roof of your building. The Bloch sphere is just a graph; a visualization tool.
```

However, since the Bloch sphere does lie in $\mathbb{R}^3$, it is conventional to give the states on the axes special names. For instance, the states $\ket{+\textbf{z}}$ and $\ket{-\textbf{z}}$ correspond to $\ket{0}$ and $\ket{1}$, respectively (which you can check with the previous equation above). Likewise
```{math}
\ket{\pm\textbf{x}} = \frac{1}{\sqrt{2}}\big(\ket{0} \pm \ket{1}\big) \\
\ket{\pm\textbf{y}} = \frac{1}{\sqrt{2}}\big(\ket{0} \pm i\ket{1}\big)
```
We will however continue to use $\ket{0}$ and $\ket{1}$ instead of $\ket{\pm\textbf{z}}$ so as to remind you that none of these axes are physical in any way, they are just representing the state of the qubit.

## How the Bloch Sphere Helps Represent EOQC Operations

Perhaps the only reason for telling you about the Bloch sphere is how beautifully it represents the single-qubit exchange operations performed by HRL's devices. In particular, applying the exchange operation between the first and second electron is represented by a rotation around the positive $z$ axis, while applying the exchange operation between the second and third electron rotates the qubit around the $\textbf{n}$ axis, where $\textbf{n}$ is the vector
```{math}
\textbf{n} = \frac{\sqrt{3}}{2}\hat{\textbf{x}} + \frac{1}{2}\hat{\textbf{z}}
```

The animation below demonstrates the operations performed on a triple quantum dot qubit by the $P_1$ and $P_2$ gates, as discussed above.

<video src="../../bloch-sphere-animation.mp4" width="800" controls></video>

```{important}
Please remember that the Bloch sphere is not a physical representation of anything within HRL's devices. Nothing is actually "rotating" when we apply the exchange operations, besides the abstract representation of the qubit on the Bloch sphere.
```








