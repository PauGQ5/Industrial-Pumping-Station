import pandapower as pp
import pandas as pd
import pandapower.plotting.plotly as pplotly

def main():
    # 1. INITIALIZE THE NETWORK
    net = pp.create_empty_network(name="Agricultural Pumping Station - 3 Wells")

    # 2. CREATE BUSES (Nodes)
    mv_bus = pp.create_bus(net, vn_kv=20.0, name="20kV MV Grid Connection")
    main_lv_board = pp.create_bus(net, vn_kv=0.4, name="Main LV Distribution Board")
    
    # Pump station buses
    pump_b3_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B3")
    pump_b5_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B5")
    pump_b7_bus = pp.create_bus(net, vn_kv=0.4, name="Pump Station B7")

    # 3. EXTERNAL GRID AND TRANSFORMER
    # Kept at 1.03 pu to emulate the real 412V tap adjustment at the secondary
    pp.create_ext_grid(net, bus=mv_bus, vm_pu=1.03, name="Utility Grid")

    pp.create_transformer_from_parameters(
        net, hv_bus=mv_bus, lv_bus=main_lv_board, 
        sn_mva=1.0, vn_hv_kv=20.0, vn_lv_kv=0.4, 
        vkr_percent=1.0, vk_percent=6.0, pfe_kw=2.0, i0_percent=0.2, 
        name="1000kVA Transformer"
    )

    # 4. CREATE LINES (Branches)
    # 3x150mm2 Cu underground cables (max 340A). Assumed 200m for the new B5 pump.
    line_params = {'r_ohm_per_km': 0.153, 'x_ohm_per_km': 0.08, 'c_nf_per_km': 0, 'max_i_ka': 0.34}
    
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b3_bus, length_km=0.15, name="Line B3 (150m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b5_bus, length_km=0.20, name="Line B5 (200m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=main_lv_board, to_bus=pump_b7_bus, length_km=0.25, name="Line B7 (250m)", **line_params)

    # 5. CREATE LOADS (PQ Buses)
    # Deep-well submersible induction motors (132 kW, pf = 0.83)
    load_params = {'p_mw': 0.132, 'q_mvar': 0.0887}
    
    pp.create_load(net, bus=pump_b3_bus, name="Submersible Pump B3", **load_params)
    pp.create_load(net, bus=pump_b5_bus, name="Submersible Pump B5", **load_params)
    pp.create_load(net, bus=pump_b7_bus, name="Submersible Pump B7", **load_params)

    # 6. RUN POWER FLOW
    pp.runpp(net)
    
    # 7. EXPORT RESULTS
    # Save the simulation results to an Excel file for project documentation
    writer = pd.ExcelWriter('load_flow_results.xlsx', engine='xlsxwriter')
    
    res_bus = pd.concat([net.bus['name'], net.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']]], axis=1)
    res_line = pd.concat([net.line['name'], net.res_line[['i_ka', 'loading_percent', 'pl_mw', 'ql_mvar']]], axis=1)
    
    res_bus.to_excel(writer, sheet_name='Nodes_Voltages', index=False)
    res_line.to_excel(writer, sheet_name='Lines_Loading', index=False)
    writer.close()
    
    print("Power flow successfully calculated and exported to Excel.")

if __name__ == '__main__':
    main()
