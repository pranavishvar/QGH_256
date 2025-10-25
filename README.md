# 🧠 Quantum Graph Hash (QGH_256)

### _Using Classical Random Walks + Quantum Spectral Fingerprinting_

---

## 📘 Concept Overview

The **Quantum Graph Hash (QGH_256)** is a novel **quantum-inspired cryptographic hash function** developed using:
- **Classical Random Walks**
- **Spectral Fingerprinting**
- **Quantum Phase Estimation (QPE)** algorithms

This approach merges graph theory with quantum computation principles to generate robust and collision-resistant hash signatures.

---

## 🔬 Methodology

### 🧩 Conceptual Process Flow

The QGH process is built as a **three-stage pipeline**:

1. **Message → Classical Random Walker**  
   → Produces a **weighted graph** (4x4 grid, 16 nodes)
2. **Weighted Graph → Laplacian Matrix**  
   → Converted into a **Hermitian operator**
3. **Hermitian Operator → Spectral Fingerprint**  
   → Extracted using **Quantum Phase Estimation (QPE)**  
   → Resulting spectrum is used as the **hash**

---

### 1️⃣ Classical Random Walks
- A **message-induced 2D random walk** is performed on a **4×4 grid**.  
- Each move affects the **edge weights** and **node connectivity**, encoding message entropy.
- The final output is a **weighted directed graph**, representing the structural signature of the message.

---

### 2️⃣ Quantum Phase Estimation (QPE)
- The **graph Laplacian** (Hermitian) is **exponentiated** to form a **unitary operator**.  
- Using **Suzuki–Trotter decomposition**, the exponential is approximated efficiently.  
- **QPE** extracts the **eigenvalue spectrum**, which serves as the **spectral fingerprint** (hash vector).  
- The **spectral components** are then normalized to produce a **QGH_256 hash**.

---

## 🧮 Mathematical Foundation

Given the Laplacian \( L \) of the message-induced graph:
\[
U = e^{-iLt}
\]
QPE estimates the **phase** \( \phi \) corresponding to each eigenvalue \( \lambda \):
\[
U|\psi\rangle = e^{2\pi i \phi}|\psi\rangle
\]
\[
\lambda = 2\pi \phi
\]
These eigenvalues form the **spectral fingerprint**:
\[
\text{QGH}(M) = \text{normalize}(\text{eig}(L))
\]

---

## ⚙️ Installation

### 🧰 Requirements
Ensure you have **Python 3.9+** installed.

### 📦 Install Dependencies

You can install all the necessary Python packages using pip:

```bash
pip install qiskit qiskit-aer qiskit-algorithms numpy networkx matplotlib scipy pandas

If you use this work, please cite:

Mohana Priya Thinesh Kumar, Pranavishvar Hariprakash,
Quantum Graph Hash (QGH_256): Spectral Fingerprinting via Quantum Phase Estimation,
IIT(ISM) Dhanbad, 2025.
