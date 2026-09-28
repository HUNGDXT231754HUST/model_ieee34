import os

base_dir = r'D:\LAB\28092026\Original IEEE-34\dss'

with open(os.path.join(base_dir, 'line_data.dss'), 'r', encoding='utf-8') as f:
    line_data = f.read().replace('Buscoords IEEE34_BusXY.csv', '')

with open(os.path.join(base_dir, 'comp.dss'), 'r', encoding='utf-8') as f:
    comp_data = f.read()

with open(os.path.join(base_dir, 'loads.dss'), 'r', encoding='utf-8') as f:
    load_data = f.read()

bus_coords = []
with open(os.path.join(base_dir, 'IEEE34_BusXY.csv'), 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            bus_coords.append(f'Setbusxy bus={parts[0]} x={parts[1]} y={parts[2]}')
bus_coords_str = '\n'.join(bus_coords)

master_content = f'''! Master file for IEEE 34 Bus - Standalone/Merged Version
Clear
Set DefaultBaseFrequency=60

New object=circuit.ieee34-1
~ basekv=69 pu=1.05 angle=30 mvasc3=200000

{line_data}

{comp_data}

{load_data}

Set VoltageBases = "69,24.9,4.16, .48"
CalcVoltageBases

! --- BUS COORDINATES ---
{bus_coords_str}
'''

with open(os.path.join(base_dir, 'original_ieee34.dss'), 'w', encoding='utf-8') as f:
    f.write(master_content)
