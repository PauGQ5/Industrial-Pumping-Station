import pandapower as pp
import pandas as pd

def create_pumping_network(tap_pu):

    # 1. INITIALIZE THE NETWORK
    net = pp.create_empty_network(name=f"Agricultural Pumping Station - Tap {tap_pu}pu")

    # 2. CREATE BUSES (Nodes)
    mv_bus = pp.create_bus(net, vn_kv=20.0, name="20kV MV Grid Connection")
    main_lv_board = pp.create_bus(net, vn_kv=0.4, name="Main LV Distribution Board")
    
    # Pump station buses
    pump_b3_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B3")
    pump_b5_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B5 (New)")
    pump_b7_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B7")

    # 3. EXTERNAL GRID AND TRANSFORMER
    # El voltaje de entrada varía según el parámetro tap_pu
    pp.create_ext_grid(net, bus=mv_bus, vm_pu=tap_pu, name="Utility Grid")

    pp.create_transformer_from_parameters(
        net, hv_bus=mv_bus, lv_bus=main_lv_board, 
        sn_mva=1.0, vn_hv_kv=20.0, vn_lv_kv=0.4, 
        vkr_percent=1.0, vk_percent=6.0, pfe_kw=2.0, i0_percent=0.2, 
        name="1000kVA Transformer"
    )

    # 4. CREATE LINES (Branches)
    line_params = {'r_ohm_per_km': 0.153, 'x_ohm_per_km': 0.08, 'c_nf_per_km': 0, 'max_i_ka': 0.34}
    
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b3_bus, length_km=0.15, name="Line B3 (150m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b5_bus, length_km=0.20, name="Line B5 (200m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b7_bus, length_km=0.25, name="Line B7 (250m)", **line_params)

    # 5. CREATE LOADS (PQ Buses)
    load_params = {'p_mw': 0.132, 'q_mvar': 0.0887}
    
    pp.create_load(net, bus=pump_b3_bus, name="Submersible Pump B3", **load_params)
    pp.create_load(net, bus=pump_b5_bus, name="Submersible Pump B5", **load_params)
    pp.create_load(net, bus=pump_b7_bus, name="Submersible Pump B7", **load_params)

    return net

def main():
    # --- SCENARIO 1: The Problem (Standard 1.00 pu Tap) ---
    print("Simulating Scenario 1: Pre-adjustment (Tap = 1.00 pu)...")
    net_problem = create_pumping_network(tap_pu=1.00)
    pp.runpp(net_problem)
    
    # --- SCENARIO 2: The Solution (Adjusted 1.03 pu Tap) ---
    print("Simulating Scenario 2: Post-adjustment (Tap = 1.03 pu)...")
    net_solution = create_pumping_network(tap_pu=1.03)
    pp.runpp(net_solution)
    
    # --- EXPORT RESULTS TO EXCEL ---
    writer = pd.ExcelWriter('load_flow_expansion_results.xlsx', engine='xlsxwriter')
    
    # Export Problem Scenario (Sheet 1)
    res_bus_prob = pd.concat([net_problem.bus['name'], net_problem.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']]], axis=1)
    res_line_prob = pd.concat([net_problem.line['name'], net_problem.res_line[['i_ka', 'loading_percent']]], axis=1)
    res_bus_prob.to_excel(writer, sheet_name='Nodes_Prob_1.00pu', index=False)
    res_line_prob.to_excel(writer, sheet_name='Lines_Prob_1.00pu', index=False)
    
    # Export Solution Scenario (Sheet 2)
    res_bus_sol = pd.concat([net_solution.bus['name'], net_solution.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']]], axis=1)
    res_line_sol = pd.concat([net_solution.line['name'], net_solution.res_line[['i_ka', 'loading_percent']]], axis=1)
    res_bus_sol.to_excel(writer, sheet_name='Nodes_Sol_1.03pu', index=False)
    res_line_sol.to_excel(writer, sheet_name='Lines_Sol_1.03pu', index=False)
    
    writer.close()
    print("Simulation complete: Both scenarios exported to 'load_flow_expansion_results.xlsx'.")

if __name__ == '__main__':
    main()
