# Quantum Graph Hash (QGH_256)

### _Using Classical Random Walks + Quantum Spectral Fingerprinting_

---

##  Concept Overview

The **Quantum Graph Hash (QGH_256)** is a novel **quantum cryptographic hash function** developed using:
 Classical Random Walks + Spectral Fingerprinting using Quantum Phase Estimation Algorithms

---

##  Methodology

### 1 Classical Random Walks
- A **message-induced 2D random walk** is performed on a **4×4 grid**.  
- Each move affects the **edge weights** and **node connectivity**, encoding message entropy.
- The final output is a **weighted directed graph**, representing the structural signature of the message.

---

### 2 Quantum Phase Estimation (QPE)
- The **graph Laplacian** (Hermitian) is **exponentiated** to form a **unitary operator**.  
- Using **Suzuki–Trotter decomposition**, the exponential is approximated efficiently.  
- **QPE** extracts the **eigenvalue spectrum**, which serves as the **spectral fingerprint** (hash vector).  
- The **spectral components** are then normalized to produce a **QGH_256 hash**.

for more information, kindly refer to the presentation ppt attached



##  Content 
This repository includes the following files:
1) main.py – The implementation of the .
2) QGH_256.ipynb – A Jupyter Notebook containing the main code, along with testing procedures and result analysis.
3) Presentation (QGH_256).pdf – A presentation providing an overview and conceptual explanation of the idea.
4) Video Explanation (QGH_256).mp4 – A video walkthrough of the concept and implementation.
     - Youtube link :- https://youtu.be/03S2Khxl8HE
6) LICENSE – The MIT License governing the usage and distribution of this project.

   

##  Installation

###  Requirements
Ensure you have **Python 3.9+** installed.

###  Install Dependencies

You can install all the necessary Python packages using pip:

```bash
pip install qiskit qiskit-aer qiskit-algorithms numpy networkx matplotlib scipy pandas
```


If you use this work, please cite:

Mohana Priya Thinesh Kumar, Pranavishvar Hariprakash,
Quantum Graph Hash (QGH_256),
IIT(ISM) Dhanbad, 2025.
