import pandas as pd
import math
import os

base_dir = r'D:\LAB\28092026\Original IEEE-34\dss'

df = pd.read_excel('D:/LAB/28092026/Original IEEE-34/data/load/spot load data.xls', skiprows=2)

spot_lines = ['\n! --- SPOT LOADS ---\n']

for idx, row in df.iterrows():
    node = str(row['Node']).strip()
    load_type = str(row['Load']).strip()
    
    if node == 'nan' or node == 'Node' or node == 'A' or node == 'Total': continue
    if load_type == 'nan': continue
    
    conn, mod = load_type.split('-')
    
    if mod == 'PQ': model = 1
    elif mod == 'Z': model = 2
    elif mod == 'I': model = 5
    else: model = 1
    
    is_delta = (conn == 'D')
    
    if node in ['888', '890']:
        kv_ll = 4.16
    else:
        kv_ll = 24.9
        
    kv = kv_ll if is_delta else (kv_ll / math.sqrt(3))
    conn_str = 'Delta' if is_delta else 'Wye'
    
    # Phase 1
    try: p1_kw = float(row['Ph-1'])
    except: p1_kw = 0.0
    try: p1_kvar = float(row['Ph-1.1'])
    except: p1_kvar = 0.0
    
    if p1_kw != 0 or p1_kvar != 0:
        bus = f"{node}.1.2" if is_delta else f"{node}.1"
        spot_lines.append(f"New Load.S{node}_a Bus1={bus} Phases=1 Conn={conn_str} Model={model} kV={kv:.3f} kW={p1_kw} kVAR={p1_kvar}\n")
        
    # Phase 2
    try: p2_kw = float(row['Ph-2'])
    except: p2_kw = 0.0
    try: p2_kvar = float(row['Ph-2.1'])
    except: p2_kvar = 0.0
    
    if p2_kw != 0 or p2_kvar != 0:
        bus = f"{node}.2.3" if is_delta else f"{node}.2"
        spot_lines.append(f"New Load.S{node}_b Bus1={bus} Phases=1 Conn={conn_str} Model={model} kV={kv:.3f} kW={p2_kw} kVAR={p2_kvar}\n")
        
    # Phase 3
    try: p3_kw = float(row['Ph-3'])
    except: p3_kw = 0.0
    try: p3_kvar = float(row['Ph-4'])  # Note: Excel header typo Ph-4
    except: p3_kvar = 0.0
    
    if p3_kw != 0 or p3_kvar != 0:
        bus = f"{node}.3.1" if is_delta else f"{node}.3"
        spot_lines.append(f"New Load.S{node}_c Bus1={bus} Phases=1 Conn={conn_str} Model={model} kV={kv:.3f} kW={p3_kw} kVAR={p3_kvar}\n")

# Append to loads.dss
with open(os.path.join(base_dir, 'loads.dss'), 'a', encoding='utf-8') as f:
    f.writelines(spot_lines)

print('Spot loads added to loads.dss')
