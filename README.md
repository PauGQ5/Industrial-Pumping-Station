# Industrial Pumping Station: Load Flow Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandapower](https://img.shields.io/badge/Pandapower-Power_Systems-green.svg)](https://pandapower.readthedocs.io/)

## 📌 Project Overview
This project models and analyzes the steady-state load flow of a medium/low voltage industrial pumping facility. The model evaluates the electrical distribution network feeding three deep-well submersible pumps (132 kW each) from a 1000 kVA (20kV/0.4kV) transformer.

This repository serves as a practical demonstration of low and medium voltage electrical design, translating real-world field constraints into a mathematical simulation. 

## ⚙️ Technical Specifications
* **Grid Connection:** 20 kV Medium Voltage (Slack Bus).
* **Transformer:** 1000 kVA, 20kV/400V, $u_{cc}$ = 6%. *Note: The secondary voltage has been tapped to 1.03 pu (412 V) to prevent undervoltage faults on the Variable Frequency Drives (VFDs).*
* **Cables:** 3x150 mm² Cu underground lines.
* **Loads:** 3x Induction motors (132 kW, $\cos  arphi  pprox 0.83$).

## 📊 Key Findings & Field Application
The initial simulation accurately predicted a significant voltage drop at the furthest node (B7, 250m) falling below the 400V nominal threshold, which triggers under-voltage protection on SD750 VFDs. 
By increasing the grid injection to **1.03 pu**, the simulation validates the field adjustment required to keep the furthest motor terminal above the critical operating voltage, ensuring stable VFD operation while maintaining thermal line loadings below 75%.

## 🚀 How to Run
1. Install requirements: `pip install pandapower pandas xlsxwriter`
2. Execute the simulation: `python load_flow_3_pumps.py`
3. Results are automatically exported to `resultados_flujo_cargas.xlsx` for further analysis in PowerWorld or AutoCAD.
