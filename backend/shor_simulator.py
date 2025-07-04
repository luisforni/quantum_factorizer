import random
from math import gcd
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.circuit.library import QFT
from qiskit.algorithms import PhaseEstimation

def modular_exp(a, x, N):
    """Cálculo de a^x mod N."""
    return pow(a, x, N)

def find_order(a, N, backend, shots=1024):
    """Usa estimación de fase cuántica para encontrar el orden r de a mod N."""
    from qiskit.circuit import QuantumCircuit
    from qiskit.circuit.library import ModularExponentiation

    n = N.bit_length() + 1
    qpe = PhaseEstimation(num_evaluation_qubits=n, quantum_instance=QuantumInstance(backend, shots=shots))

    exponentiation = ModularExponentiation(base=a, modulus=N, exponent=1)
    result = qpe.estimate(unitary=exponentiation, state_preparation=None)

    phase = result.phase
    if phase == 0:
        return None

    r = round(1 / phase)
    return r

def run_shor_factorization(N: int) -> dict:
    """Ejecuta una versión simplificada del algoritmo de Shor."""
    print(f"\n🔍 Buscando factores de {N}")

    if N % 2 == 0:
        return {"number": N, "factors": [2, N // 2], "method": "trivial"}

    a = random.randint(2, N - 2)
    print(f"\n✅ Número aleatorio a = {a}")

    d = gcd(a, N)
    if d > 1:
        print(f"🎉 ¡Factor encontrado sin cuántica!: {d}")
        return {"number": N, "factors": [d, N // d], "method": "gcd"}

    try:
        backend = Aer.get_backend("aer_simulator")
        r = find_order(a, N, backend)

        if r is None or r % 2 != 0:
            return {"number": N, "factors": [], "error": "No se pudo estimar el período", "method": "quantum"}

        factor1 = gcd(pow(a, r // 2) - 1, N)
        factor2 = gcd(pow(a, r // 2) + 1, N)

        if factor1 * factor2 == N:
            return {"number": N, "factors": [factor1, factor2], "method": "quantum"}
        else:
            return {"number": N, "factors": [], "error": "Factores incorrectos", "method": "quantum"}

    except Exception as e:
        return {"number": N, "factors": [], "error": str(e), "method": "quantum"}
