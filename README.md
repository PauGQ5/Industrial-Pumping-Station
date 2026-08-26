# Industrial Pumping Station: Network Expansion & Load Flow Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandapower](https://img.shields.io/badge/Pandapower-Power_Systems-green.svg)](https://pandapower.readthedocs.io/)

## 📌 Project Overview
This project models and analyzes the steady-state load flow of a medium/low voltage agricultural pumping facility undergoing a capacity expansion. The objective was to validate the electrical distribution network's capability to integrate a newly added third 132 kW deep-well submersible pump alongside the two existing units, all fed from a single 1000 kVA (20kV/0.4kV) transformer.

## ⚙️ Technical Specifications
* **Grid Connection:** 20 kV Medium Voltage (Slack Bus).
* **Transformer:** 1000 kVA, 20kV/400V, $u_{cc}$ = 6%.
* **Cables:** 3x150 mm² Cu underground lines.
* **Loads:** 3x Induction motors (132 kW, pf = 0.83).

## 📊 Engineering Challenge & Solution
Upon the theoretical addition of the third pump, preliminary field data indicated that the Variable Frequency Drives (VFDs)—located at the main LV board—would frequently trip on motor overload/overcurrent protections during simultaneous operation. 

Using `pandapower`, a load flow simulation was developed to diagnose the root cause. The model revealed that the combined current draw of all three pumps caused a significant voltage drop across the transformer's internal impedance and the long cable runs (up to 250m). Consequently, the voltage at the furthest motor terminal (Node B7) dropped to critical levels (~380 V). To maintain constant mechanical power, the induction motor drew excessive current, triggering the VFD's thermal overload protections.

**The validated solution:** 
Instead of costly cable resizing, the simulation proved that adjusting the transformer primary tap to **1.03 pu (412 V)** successfully compensated for the voltage drop. The model verifies that under this adjustment, the furthest node maintains a healthy 395 V, returning motor current draw to nominal levels and eliminating VFD trips, while keeping all cable thermal loadings safely below 75%.

## 🚀 How to Run
1. Install requirements: `pip install pandapower pandas xlsxwriter`
2. Execute the simulation: `python load_flow_3_pumps.py`
3. Results are automatically exported to `load_flow_results.xlsx` for integration with Power World Simulator visualization.
