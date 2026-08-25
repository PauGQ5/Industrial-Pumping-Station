import pandapower as pp
import pandas as pd
import pandapower.plotting.plotly as pplotly

def main():
    # 1. INICIALIZAR LA RED
    net = pp.create_empty_network(name="Sistema de Bombeo Agrícola - 3 Pozos")

    # 2. CREACIÓN DE NUDOS (Buses)
    bus_mt = pp.create_bus(net, vn_kv=20.0, name="Acometida MT 20kV")
    bus_cgb = pp.create_bus(net, vn_kv=0.4, name="Cuadro General BT")
    
    # Nudos de los pozos
    bus_pozo_b3 = pp.create_bus(net, vn_kv=0.4, name="Pozo B3")
    bus_pozo_b5 = pp.create_bus(net, vn_kv=0.4, name="Pozo B5 (Nuevo)")
    bus_pozo_b7 = pp.create_bus(net, vn_kv=0.4, name="Pozo B7")

    # 3. RED EXTERNA Y TRANSFORMADOR
    # Mantenemos el ajuste de 1.03 pu para emular los 412V reales en el secundario
    pp.create_ext_grid(net, bus=bus_mt, vm_pu=1.03, name="Red Distribuidora")

    pp.create_transformer_from_parameters(
        net, hv_bus=bus_mt, lv_bus=bus_cgb, 
        sn_mva=1.0, vn_hv_kv=20.0, vn_lv_kv=0.4, 
        vkr_percent=1.0, vk_percent=6.0, pfe_kw=2.0, i0_percent=0.2, 
        name="Trafo 1000kVA"
    )

    # 4. CREACIÓN DE LÍNEAS (Ramas)
    # Cable 3x150mm2 Cu (max 340A). Asumimos 200m para el nuevo pozo B5.
    line_params = {'r_ohm_per_km': 0.153, 'x_ohm_per_km': 0.08, 'c_nf_per_km': 0, 'max_i_ka': 0.34}
    
    pp.create_line_from_parameters(net, from_bus=bus_cgb, to_bus=bus_pozo_b3, length_km=0.15, name="Línea B3 (150m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=bus_cgb, to_bus=bus_pozo_b5, length_km=0.20, name="Línea B5 (200m)", **line_params)
    pp.create_line_from_parameters(net, from_bus=bus_cgb, to_bus=bus_pozo_b7, length_km=0.25, name="Línea B7 (250m)", **line_params)

    # 5. CREACIÓN DE CARGAS (Nudos PQ)
    # Motores sumergibles de 132 kW, fp = 0.83
    load_params = {'p_mw': 0.132, 'q_mvar': 0.0887}
    
    pp.create_load(net, bus=bus_pozo_b3, name="Bomba B3", **load_params)
    pp.create_load(net, bus=bus_pozo_b5, name="Bomba B5", **load_params)
    pp.create_load(net, bus=bus_pozo_b7, name="Bomba B7", **load_params)

    # 6. EJECUCIÓN DEL FLUJO DE CARGAS
    pp.runpp(net)
    
    # 7. EXPORTAR RESULTADOS
    # Guardamos los resultados en Excel para documentar el proyecto
    writer = pd.ExcelWriter('resultados_flujo_cargas.xlsx', engine='xlsxwriter')
    
    res_bus = pd.concat([net.bus['name'], net.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']]], axis=1)
    res_line = pd.concat([net.line['name'], net.res_line[['i_ka', 'loading_percent', 'pl_mw', 'ql_mvar']]], axis=1)
    
    res_bus.to_excel(writer, sheet_name='Nudos_Tensiones', index=False)
    res_line.to_excel(writer, sheet_name='Lineas_Cargas', index=False)
    writer.close()
    
    print("Flujo de cargas completado y exportado a Excel.")

if __name__ == '__main__':
    main()
