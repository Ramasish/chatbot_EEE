from gs_agent import run_conversation

prompt = """
Calculate v at each bus
yBus = [3-8.95*1j -2+6*1j -1+3*1j 0
-2+6*1j 3.774-11.306*1j -0.674+2.024*1j -1.044+3.134*1j
-1+3*1j -0.674+2.024*1j 3.666-10.96*1j -2+6*1j
0 -1.044+3.134*1j -2+6*1j 3-8.99*1j ];

P = [
    0 + 0j,          # Slack
    -0.45 - 0.22j,   # Load bus 2
    0.98 - 0.40j,    # Gen bus 3
    -0.32 + 0.15j    # Load bus 4
]

V_init = [
    1.05 + 0j,
    1.0 + 0j,
    1.0 + 0j,
    1.0 + 0j
]

"""

print(run_conversation(prompt))