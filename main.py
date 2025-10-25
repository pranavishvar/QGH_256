from qiskit import *
from qiskit_aer import Aer
import numpy as np
import networkx as nx
from math import ceil
from qiskit.circuit.library import PauliEvolutionGate, UnitaryGate
from qiskit.quantum_info import Operator, SparsePauliOp
from qiskit_algorithms import PhaseEstimation
from qiskit_aer.primitives import SamplerV2 as Sampler
from collections import Counter
from qiskit.synthesis import SuzukiTrotter

class QGH_256():
    def __init__(self, msg):
        self.msg = msg

    def preprocessing(self, message: str, block_size: int):
        # Convert message into binary blocks of given size
        message_bytes = message.encode("utf-8")
        binary_str = ''.join(format(byte, '08b') for byte in message_bytes)
        blocks = [binary_str[i:i + block_size] for i in range(0, len(binary_str), block_size)]
        if len(blocks[-1]) < block_size:
            blocks[-1] = blocks[-1].ljust(block_size, '0')
        return blocks

    def move_walker(self, pos, direction, grid_size=4):
        # Move walker in toroidal (wrap-around) 4x4 grid
        x, y = pos
        if direction == '00':      # down
            y = (y - 1) % grid_size
        elif direction == '01':    # up
            y = (y + 1) % grid_size
        elif direction == '10':    # right
            x = (x + 1) % grid_size
        elif direction == '11':    # left
            x = (x - 1) % grid_size
        return (x, y)

    def walk(self, message: str):
        # Perform quantum-style walk over 8x8 grid using binary-encoded message.
        grid_size = 4
        block_size = 2
        blocks = self.preprocessing(message, block_size)

        # Build toroidal grid
        G = nx.grid_2d_graph(grid_size, grid_size, periodic=True)
        nx.set_edge_attributes(G, 0, "weight")

        pos = (grid_size // 2, grid_size // 2)  # start center
        path = [pos]

        for block in blocks:
            new_pos = self.move_walker(pos, block, grid_size)
            if G.has_edge(pos, new_pos):
                G[pos][new_pos]['weight'] += 1
            path.append(new_pos)
            pos = new_pos

        return G, path
    
    def extract_phases(self, counts, num_ancilla, t):
        phase_counts = Counter()
        for bitstring, count in counts.items():
            phase_bits = bitstring[:6]
            decimal = int(phase_bits, 2)
            phase = decimal / (2 ** num_ancilla)
            phase = 2*np.pi*phase/t
            phase_counts[phase] += count
        return phase_counts
    
    def spectral_fingerprint(self):
        G, path = self.walk(self.msg)

        heat_vectors = {}
        spectrum_collection = []
        n = len(G.nodes())

        A = nx.to_numpy_array(G)

        degrees = dict(G.degree())
        D = np.diag([degrees[node] for node in G.nodes()])
        L = D - A 

        # Padding to next power of 2
        n_laplacian = L.shape[0]
        n_qubits = ceil(np.log2(n_laplacian))
        L_padded = np.zeros((2**n_qubits, 2**n_qubits), dtype=complex)
        L_padded[:n_laplacian, :n_laplacian] = L

        # Normalize to [0, 1]
        L_min, L_max = L_padded.min(), L_padded.max()
        L_padded = (L_padded - L_min) / (L_max - L_min)



        pauli_op = SparsePauliOp.from_operator(Operator(L_padded).data)

        # Define times
        times = np.array(range(1, 5))*np.pi/5  # t1, t2, t3 t4

        # Generate Trotterized circuits
        trotter_circuits = {}
        unitary_gates = {}
        for t in times:
            evo_gate = PauliEvolutionGate(pauli_op, time=t, synthesis=SuzukiTrotter(order=2, reps=3))
            trotter_circuits[t] = evo_gate
            unitary_gates[t] = UnitaryGate(Operator(evo_gate).data, label=f"U({t})")
        # Creating equal superposition state
        superposition_state = np.zeros(2**n_qubits)
        for i in range(n):
            superposition_state[i] = 1
        superposition_state /= np.linalg.norm(superposition_state)

        # Quantum Phase Estimation (QPE)
        spectrum = {}
        for t, unitary in unitary_gates.items():
            num_ancilla = 3
            initial_state = QuantumCircuit(n_qubits)
            initial_state.initialize(superposition_state)

            phase_estimation = PhaseEstimation(num_evaluation_qubits=num_ancilla, sampler=Sampler())
            simulator = Aer.get_backend("aer_simulator_statevector")
            circ = phase_estimation.construct_circuit(unitary, initial_state)
            circ.measure_all()
            transpiled = transpile(circ, simulator)
            job = simulator.run(transpiled, shots = 300, seed_simulator = 42)
            result = job.result()
            counts = result.get_counts()
            spectrum[t] = counts

        spectrum_collection.append(spectrum)

        heat_trace_vector = []

        # Constructing the spectral fingerprint
        for t, counts in spectrum.items():
            phases = self.extract_phases(counts, num_ancilla, t)
            heat_trace = np.average(np.exp(-t*np.array(list(phases.keys()))), weights=list(phases.values()))
            heat_trace_vector.append(heat_trace)

        heat_trace_vector = np.array(heat_trace_vector)
        heat_vectors[tuple(G.edges)] = heat_trace_vector

        for key, val in heat_vectors.items():
            return val
        
    def convert_spectral_fingerprint_into_hash(self, spectral_fingerprint):
        bit_strings = [''.join(f'{b:08b}' for b in np.frombuffer(v.tobytes(), dtype=np.uint8)[::-1]) for v in spectral_fingerprint]
        bit_string = ''.join(bit_strings)

        return bit_string

    def hash(self):
        sf = self.spectral_fingerprint()
        hash = self.convert_spectral_fingerprint_into_hash(sf)
        return hash

# Example
qgh = QGH_256("hella")
hash = qgh.hash()
print("Hash:",hash)

