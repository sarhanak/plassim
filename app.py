import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors

st.set_page_config(page_title="Advanced Plasma Fertilizer Simulator", layout="wide")
st.title("Advanced Plasma Fertilizer Technology Simulator")
st.write("Interactive simulation for maximizing plasma-based nitric oxide production using multi-modal reactor designs")

# Layout: Left column for parameters and outputs, right column for reactor visualization & graphs
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Process Parameters")
    
    # Basic process sliders
    power_input = st.slider("Power Input (kW)", 1.0, 10.0, 5.0, 0.1)
    air_flow = st.slider("Air Flow Rate (L/min)", 1.0, 20.0, 10.0, 0.5)
    pressure = st.slider("Pressure (atm)", 0.5, 2.0, 1.0, 0.1)
    
    # New advanced parameters
    pulsed_power_freq = st.slider("Pulsed Power Frequency (kHz)", 1, 100, 50, 1)
    magnetic_field = st.slider("Magnetic Field Strength (Tesla)", 0.0, 1.0, 0.5, 0.1)
    
    catalyst = st.selectbox("Catalyst Type", ["None", "Metal Oxide", "Zeolite", "Platinum"])
    # Expanded plasma type options
    plasma_type = st.selectbox("Plasma Technology", ["Gliding Arc", "DBD", "Advanced Propeller Arc"])
    
    st.markdown("---")
    st.subheader("Calculated Outputs")
    
    # Initialize outputs
    energy_efficiency = 0
    no_yield = 0
    
    # Define catalyst factors for each plasma type
    if plasma_type == "Gliding Arc":
        # Formula: base efficiency decreased by power & pressure, improved by air flow
        energy_efficiency = 35 - (power_input * 0.5) - (pressure * 2) + (air_flow * 0.2)
        catalyst_factor = {"None": 1.0, "Metal Oxide": 1.2, "Zeolite": 1.3, "Platinum": 1.5}
        no_yield = (power_input * 0.6) * (air_flow * 0.05) * catalyst_factor[catalyst] / pressure
        
    elif plasma_type == "DBD":
        energy_efficiency = 40 - (power_input * 0.3) - (pressure * 1.5) + (air_flow * 0.1)
        catalyst_factor = {"None": 1.0, "Metal Oxide": 1.3, "Zeolite": 1.4, "Platinum": 1.6}
        no_yield = (power_input * 0.5) * (air_flow * 0.06) * catalyst_factor[catalyst] / (pressure * 1.1)
        
    else:  # Advanced Propeller Arc with Reverse Vortex, Magnetic Field & Pulsed Power
        # Base efficiency is higher due to advanced design
        base_eff = 50 - (power_input * 0.4) - (pressure * 1.8) + (air_flow * 0.15)
        # Additional enhancements: pulsed power frequency and magnetic field boost efficiency
        enhancement = (pulsed_power_freq * 0.05) + (magnetic_field * 5)
        energy_efficiency = base_eff + enhancement
        
        # Catalyst factor is boosted in the advanced model
        catalyst_factor = {"None": 1.0, "Metal Oxide": 1.4, "Zeolite": 1.5, "Platinum": 1.8}
        # NO yield considers pulsed power and magnetic field improvements
        no_yield = (power_input * 0.7) * (air_flow * 0.07) * catalyst_factor[catalyst] / pressure
        no_yield *= (1 + (pulsed_power_freq / 200)) * (1 + (magnetic_field / 2))
    
    # Clamp output ranges for realistic simulation
    energy_efficiency = max(10, min(energy_efficiency, 90))
    no_yield = max(1, min(no_yield, 25))
    
    st.metric("Energy Efficiency (%)", f"{energy_efficiency:.1f}")
    st.metric("NO Yield (g/kWh)", f"{no_yield:.2f}")
    energy_consumption = 24 + (90 - energy_efficiency) / 2
    st.metric("Energy Consumption (GJ/tN)", f"{energy_consumption:.1f}")
    
    # Cost estimation compared to subsidized urea cost
    cost_per_kg_n = 11.5 * (24 / energy_consumption)
    st.metric("Est. Cost per kg N (₹)", f"{cost_per_kg_n:.2f}", delta=f"{11.5 - cost_per_kg_n:.2f} vs. Urea")
    
    st.markdown("---")
    st.subheader("Financial Impact")
    num_farmers = st.slider("Number of Farmers Served", 10, 100, 30)
    acres_per_farmer = st.slider("Average Acres per Farmer", 1, 20, 5)
    
    total_n_required = num_farmers * acres_per_farmer * 30  # 30 kg N per acre assumption
    annual_savings = num_farmers * acres_per_farmer * 30 * (11.5 - cost_per_kg_n)
    
    st.metric("Annual N Requirement (kg)", f"{total_n_required:,}")
    st.metric("Annual Farmer Savings (₹)", f"{annual_savings:,.0f}")
    
    if st.button("Generate Report"):
        st.write("Report generated and ready to export! (Simulation only)")

with col2:
    st.subheader("Plasma Reactor Visualization")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    def setup_reactor():
        ax.clear()
        # Reactor tube
        reactor = plt.Rectangle((1, 1), 8, 4, fill=False, color='black', linewidth=2)
        ax.add_patch(reactor)
        # Electrodes
        electrode1 = plt.Rectangle((2, 0.8), 0.5, 4.4, color='gray', alpha=0.7)
        electrode2 = plt.Rectangle((7.5, 0.8), 0.5, 4.4, color='gray', alpha=0.7)
        ax.add_patch(electrode1)
        ax.add_patch(electrode2)
        # Air inlet and outlet
        inlet = plt.Arrow(0.5, 3, 0.5, 0, width=0.8, color='blue', alpha=0.7)
        outlet = plt.Arrow(9, 3, 0.5, 0, width=0.8, color='green', alpha=0.7)
        ax.add_patch(inlet)
        ax.add_patch(outlet)
        ax.text(0.5, 4.2, 'Air Inlet', fontsize=10)
        ax.text(8.5, 4.2, 'NO Output', fontsize=10)
        ax.text(2.25, 0.4, 'Electrode', fontsize=10)
        ax.text(7.75, 0.4, 'Electrode', fontsize=10)
        # Catalyst bed (if used)
        if catalyst != "None":
            catalyst_patch = plt.Rectangle((4, 1.2), 2, 3.6, color='brown', alpha=0.3)
            ax.add_patch(catalyst_patch)
            ax.text(4.3, 0.8, f'{catalyst} Catalyst', fontsize=10)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        return []
    
    def animate(i, plasma_points, air_flow_rate, power, pulsed_freq, mag_field):
        arcs = []
        # Create arcs depending on plasma type
        if plasma_type == "Gliding Arc":
            for _ in range(3):
                x = np.array([2.5, 4.5 + np.random.rand()*2])
                y = np.array([3 + np.random.randn()*1.5, 3 + np.random.randn()*1.5])
                arc, = ax.plot(x, y, color='purple', linewidth=np.random.rand()*2 + 1, alpha=0.8)
                arcs.append(arc)
        elif plasma_type == "DBD":
            for _ in range(15):
                x = np.array([2.5, 3.5 + np.random.rand()*3])
                y = np.array([1.2 + np.random.rand()*3.6, 1.2 + np.random.rand()*3.6])
                arc, = ax.plot(x, y, color='blueviolet', linewidth=np.random.rand() + 0.5, alpha=0.6)
                arcs.append(arc)
        else:  # Advanced Propeller Arc
            # Combine fewer intense arcs with multiple mini discharges
            for _ in range(2):
                x = np.array([2.5, 4.5 + np.random.rand()*2])
                y = np.array([3 + np.random.randn()*1.5, 3 + np.random.randn()*1.5])
                arc, = ax.plot(x, y, color='red', linewidth=np.random.rand()*2 + 1.5, alpha=0.9)
                arcs.append(arc)
            for _ in range(10):
                x = np.array([2.5, 3.5 + np.random.rand()*3])
                y = np.array([1.2 + np.random.rand()*3.6, 1.2 + np.random.rand()*3.6])
                arc, = ax.plot(x, y, color='orange', linewidth=np.random.rand() + 0.5, alpha=0.7)
                arcs.append(arc)
        
        # Add air flow particles (simulate reverse vortex by randomizing y positions slightly)
        particles = []
        for _ in range(int(air_flow_rate)):
            x = np.linspace(1, 9, 20)
            y = 3 + np.random.randn()*0.8  # vortex effect can be implied by variability in y
            particle, = ax.plot(x[0], y, 'o', color='lightblue', alpha=0.7, markersize=3)
            particles.append((particle, x, y))
        
        # Add NO output particles
        no_particles = []
        for _ in range(int(no_yield)):
            x = 9
            y = 3 + np.random.randn()*0.8
            no_particle, = ax.plot(x, y, 'o', color='green', alpha=0.8, markersize=4)
            no_particles.append(no_particle)
        
        # Simulate pulsed power with periodic “spark” markers at the reactor inlet
        pulsed_indicators = []
        pulse_cycle = int(pulsed_freq / 10)  # scale factor for visualization frequency
        if i % pulse_cycle == 0:
            for _ in range(int(power)):
                x = 0.2 + np.random.rand()*0.3
                y = 0.2 + np.random.rand()*0.3
                pulse, = ax.plot(x, y, 's', color='red', alpha=0.9, markersize=6)
                pulsed_indicators.append(pulse)
        
        # Magnetic field visualization (show field lines as faint curves near reactor)
        field_lines = []
        for _ in range(3):
            theta = np.linspace(0, np.pi, 50)
            r = 0.5 + mag_field * 0.5
            x_field = 5 + r * np.cos(theta) + np.random.randn()*0.1
            y_field = 3 + r * np.sin(theta) + np.random.randn()*0.1
            line, = ax.plot(x_field, y_field, color='cyan', linewidth=1, alpha=0.5)
            field_lines.append(line)
            
        return arcs + [p[0] for p in particles] + no_particles + pulsed_indicators + field_lines
    
    # Initialize reactor and animation
    plasma_points = []
    setup_reactor()
    anim_placeholder = st.empty()
    anim = FuncAnimation(fig, animate, frames=20, fargs=(plasma_points, air_flow, power_input, pulsed_power_freq, magnetic_field),
                         blit=True, interval=200)
    anim_placeholder.pyplot(fig)
    
    st.subheader("Performance Metrics")
    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Efficiency vs. power for each plasma type over a range of power inputs
    power_range = np.linspace(1, 10, 10)
    eff_gliding = [35 - (p * 0.5) - (pressure * 2) + (air_flow * 0.2) for p in power_range]
    eff_dbd = [40 - (p * 0.3) - (pressure * 1.5) + (air_flow * 0.1) for p in power_range]
    # Advanced model includes pulsed power and magnetic field enhancements
    eff_adv = [ (50 - (p * 0.4) - (pressure * 1.8) + (air_flow * 0.15)) + (pulsed_power_freq * 0.05) + (magnetic_field * 5) for p in power_range ]
    
    ax1.plot(power_range, eff_gliding, label='Gliding Arc')
    ax1.plot(power_range, eff_dbd, label='DBD')
    ax1.plot(power_range, eff_adv, label='Advanced Propeller Arc')
    ax1.axvline(x=power_input, color='r', linestyle='--', label='Selected Power')
    ax1.set_xlabel('Power Input (kW)')
    ax1.set_ylabel('Energy Efficiency (%)')
    ax1.set_title('Efficiency vs. Power')
    ax1.legend()
    
    # Cost Comparison Bar Chart
    labels = ['Urea (Subsidized)', 'Your Tech']
    costs = [11.5, cost_per_kg_n]
    ax2.bar(labels, costs, color=['gray', 'green'])
    ax2.set_ylabel('Cost per kg N (₹)')
    ax2.set_title('Cost Comparison')
    for i, v in enumerate(costs):
        ax2.text(i, v + 0.1, f'₹{v:.2f}', ha='center')
    
    plt.tight_layout()
    st.pyplot(fig2)

st.subheader("Technology Process Flow")
col3, col4 = st.columns(2)
with col3:
    st.markdown("""
    ### Process Steps:
    1. **Air Intake**: Ambient air is drawn into the system.
    2. **Plasma Generation**: Electric discharge creates plasma (via DBD, Gliding Arc, or Advanced Propeller Arc).
    3. **NO Formation**: N₂ + O₂ → 2NO, enhanced by pulsed power and catalyst.
    4. **Cooling & Vortex Flow**: Reverse vortex flow and fluidized bed help cool the gas.
    5. **Magnetic Field Application**: Magnetic field stabilizes plasma arcs.
    6. **Oxidation**: 2NO + O₂ → 2NO₂.
    7. **Absorption**: 3NO₂ + H₂O → 2HNO₃ + NO.
    8. **Neutralization**: HNO₃ + Ca(OH)₂ → Ca(NO₃)₂ + 2H₂O.
    9. **Final Product**: Calcium Nitrate fertilizer.
    """)
with col4:
    st.markdown("""
    ### Key Advantages:
    - **Enhanced Efficiency**: Combines multiple plasma techniques with pulsed power and magnetic stabilization.
    - **Optimized NO Yield**: Leverages advanced catalyst and reactor designs.
    - **Cost Competitive**: Lower energy consumption and fertilizer production cost.
    - **Scalable & Modular**: Suitable for regional plants and easy process adjustments.
    - **Future-Ready**: Provides a platform for AI optimization and process control.
    """)
    
st.markdown("---")
st.caption("This advanced simulator integrates cutting-edge plasma reactor designs to maximize efficiency. Use this tool to demonstrate process feasibility and secure funding for a prototype.")
