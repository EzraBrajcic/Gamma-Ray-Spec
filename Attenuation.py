#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator, interp1d

# Extract the attenuation data from your code
attenuation_table = np.array([
    [1.000e-03, 7.422e+00, 5.916e-03, 7.794e+03, 0.000e+00, 7.801e+03, 7.794e+03],
    [1.035e-03, 7.394e+00, 6.244e-03, 7.245e+03, 0.000e+00, 7.252e+03, 7.245e+03],
    [1.072e-03, 7.366e+00, 6.586e-03, 6.736e+03, 0.000e+00, 6.744e+03, 6.736e+03],
    [1.072e-03, 7.366e+00, 6.586e-03, 7.021e+03, 0.000e+00, 7.029e+03, 7.021e+03],
    [1.072e-03, 7.366e+00, 6.586e-03, 7.925e+03, 0.000e+00, 7.932e+03, 7.925e+03],
    [1.072e-03, 7.366e+00, 6.587e-03, 7.021e+03, 0.000e+00, 7.028e+03, 7.021e+03],
    [1.072e-03, 7.366e+00, 6.587e-03, 7.924e+03, 0.000e+00, 7.932e+03, 7.924e+03],
    [1.500e-03, 7.010e+00, 1.065e-02, 3.801e+03, 0.000e+00, 3.808e+03, 3.801e+03],
    [2.000e-03, 6.555e+00, 1.541e-02, 1.917e+03, 0.000e+00, 1.924e+03, 1.917e+03],
    [3.000e-03, 5.687e+00, 2.459e-02, 7.003e+02, 0.000e+00, 7.060e+02, 7.003e+02],
    [4.000e-03, 4.947e+00, 3.292e-02, 3.351e+02, 0.000e+00, 3.401e+02, 3.352e+02],
    [4.557e-03, 4.592e+00, 3.712e-02, 2.387e+02, 0.000e+00, 2.433e+02, 2.387e+02],
    [4.557e-03, 4.592e+00, 3.712e-02, 6.585e+02, 0.000e+00, 6.631e+02, 6.585e+02],
    [4.702e-03, 4.506e+00, 3.816e-02, 6.166e+02, 0.000e+00, 6.211e+02, 6.166e+02],
    [4.852e-03, 4.419e+00, 3.923e-02, 5.774e+02, 0.000e+00, 5.819e+02, 5.775e+02],
    [4.852e-03, 4.419e+00, 3.923e-02, 7.719e+02, 0.000e+00, 7.763e+02, 7.719e+02],
    [5.000e-03, 4.335e+00, 4.026e-02, 7.277e+02, 0.000e+00, 7.320e+02, 7.277e+02],
    [5.188e-03, 4.229e+00, 4.155e-02, 6.611e+02, 0.000e+00, 6.654e+02, 6.612e+02],
    [5.188e-03, 4.229e+00, 4.155e-02, 7.604e+02, 0.000e+00, 7.646e+02, 7.604e+02],
    [6.000e-03, 3.816e+00, 4.679e-02, 5.297e+02, 0.000e+00, 5.336e+02, 5.298e+02],
    [8.000e-03, 3.009e+00, 5.799e-02, 2.489e+02, 0.000e+00, 2.519e+02, 2.489e+02],
    [1.000e-02, 2.437e+00, 6.731e-02, 1.375e+02, 0.000e+00, 1.400e+02, 1.376e+02],
    [1.500e-02, 1.598e+00, 8.410e-02, 4.570e+01, 0.000e+00, 4.738e+01, 4.578e+01],
    [2.000e-02, 1.136e+00, 9.463e-02, 2.062e+01, 0.000e+00, 2.185e+01, 2.071e+01],
    [3.000e-02, 6.443e-01, 1.067e-01, 6.607e+00, 0.000e+00, 7.358e+00, 6.714e+00],
    [3.317e-02, 5.556e-01, 1.090e-01, 4.972e+00, 0.000e+00, 5.636e+00, 5.081e+00],
    [3.317e-02, 5.556e-01, 1.090e-01, 2.976e+01, 0.000e+00, 3.042e+01, 2.987e+01],
    [4.000e-02, 4.196e-01, 1.127e-01, 1.824e+01, 0.000e+00, 1.877e+01, 1.835e+01],
    [5.000e-02, 2.978e-01, 1.157e-01, 1.006e+01, 0.000e+00, 1.048e+01, 1.018e+01],
    [6.000e-02, 2.221e-01, 1.169e-01, 6.111e+00, 0.000e+00, 6.450e+00, 6.228e+00],
    [8.000e-02, 1.365e-01, 1.165e-01, 2.746e+00, 0.000e+00, 2.999e+00, 2.863e+00],
    [1.000e-01, 9.243e-02, 1.144e-01, 1.462e+00, 0.000e+00, 1.669e+00, 1.576e+00],
    [1.500e-01, 4.491e-02, 1.071e-01, 4.592e-01, 0.000e+00, 6.112e-01, 5.663e-01],
    [2.000e-01, 2.654e-02, 1.000e-01, 2.019e-01, 0.000e+00, 3.285e-01, 3.020e-01],
    [3.000e-01, 1.238e-02, 8.860e-02, 6.481e-02, 0.000e+00, 1.658e-01, 1.534e-01],
    [4.000e-01, 7.126e-03, 8.009e-02, 2.987e-02, 0.000e+00, 1.171e-01, 1.100e-01],
    [5.000e-01, 4.622e-03, 7.351e-02, 1.684e-02, 0.000e+00, 9.497e-02, 9.035e-02],
    [6.000e-01, 3.238e-03, 6.822e-02, 1.079e-02, 0.000e+00, 8.225e-02, 7.901e-02],
    [8.000e-01, 1.840e-03, 6.012e-02, 5.588e-03, 0.000e+00, 6.755e-02, 6.571e-02],
    [1.000e+00, 1.184e-03, 5.413e-02, 3.491e-03, 0.000e+00, 5.881e-02, 5.762e-02],
    [1.022e+00, 1.134e-03, 5.355e-02, 3.323e-03, 0.000e+00, 5.801e-02, 5.687e-02],
    [1.250e+00, 7.607e-04, 4.846e-02, 2.240e-03, 1.634e-04, 5.162e-02, 5.086e-02],
    [1.500e+00, 5.293e-04, 4.407e-02, 1.604e-03, 7.594e-04, 4.697e-02, 4.644e-02],
    [2.000e+00, 2.985e-04, 3.764e-02, 9.761e-04, 2.575e-03, 4.149e-02, 4.119e-02]
])

# Unpack the data columns - these are already mass attenuation coefficients in cm²/g
MeV, mu_coh, mu_incoh, mu_photoelectric, mu_pair_nuclear, mu_tot_with_coh, mu_tot_without_coh = attenuation_table.T

# Note: No need to divide by density as the data is already in mass attenuation coefficients

# Function to identify and handle absorption edges (duplicate energy values)
def prepare_data_for_interpolation(energy, values):
    processed_energy = []
    processed_values = []
    energy_values_map = {}
    
    for e, v in zip(energy, values):
        if e not in energy_values_map:
            energy_values_map[e] = []
        energy_values_map[e].append(v)
    
    sorted_energies = sorted(energy_values_map.keys())
    
    for e in sorted_energies:
        values_at_e = energy_values_map[e]
        
        if len(values_at_e) == 1:
            processed_energy.append(e)
            processed_values.append(values_at_e[0])
        else:
            # Use relative epsilon based on current energy
            epsilon = max(e * 1e-10, 1e-20)  # Ensure minimum epsilon to avoid zero
            values_sorted = sorted(values_at_e)
            processed_energy.append(e)
            processed_values.append(values_sorted[0])
            for i, v in enumerate(values_sorted[1:], 1):
                processed_energy.append(e + epsilon * i)
                processed_values.append(v)
    
    return np.array(processed_energy), np.array(processed_values)

# Update the interpolation function to use log-log
def piecewise_monotonic_interp(x_data, y_data, x_query):
    """Piecewise PCHIP interpolation applied ONLY at discontinuities/edges"""
    # Convert to log space for better behavior over orders of magnitude
    log_x = np.log(x_data)
    log_y = np.log(y_data)
    log_x_query = np.log(x_query)

    # 1. Identify TRUE discontinuities -----------------------------------------
    # Find absorption edges (duplicate x values)
    _, unique_indices, counts = np.unique(x_data, return_index=True, return_counts=True)
    edge_indices = sorted([i for i, cnt in zip(unique_indices, counts) if cnt > 1])

    # Find large derivative changes in LINEAR space (better for physics)
    dy_linear = np.gradient(y_data, x_data)
    d2y_linear = np.gradient(dy_linear, x_data)
    jump_mask = np.abs(d2y_linear) > 5 * np.std(np.abs(d2y_linear))
    jump_indices = np.where(jump_mask)[0]

    # Combine edge indices and jump indices (add buffer around jumps)
    all_split_points = sorted(list(set(
        [0] + 
        edge_indices + 
        [max(0, i-1) for i in jump_indices] + 
        [min(len(x_data)-1, i+1) for i in jump_indices] + 
        [len(x_data)-1]
    )))

    # 2. Create segments between discontinuities -------------------------------
    segments = []
    for i in range(len(all_split_points)-1):
        start = all_split_points[i]
        end = all_split_points[i+1]
        segments.append((start, end))

    # 3. Interpolate each segment with PCHIP ----------------------------------
    result = np.full_like(log_x_query, np.nan)
    
    for seg_start, seg_end in segments:
        # Extract segment data in log space
        seg_logx = log_x[seg_start:seg_end+1]
        seg_logy = log_y[seg_start:seg_end+1]
        
        # Handle single-point segments
        if len(seg_logx) == 1:
            mask = (log_x_query >= seg_logx[0]-1e-9) & (log_x_query <= seg_logx[0]+1e-9)
            result[mask] = seg_logy[0]
            continue

        # Create interpolator for this segment
        try:
            interp = PchipInterpolator(seg_logx, seg_logy, extrapolate=False)
        except ValueError:
            interp = interp1d(seg_logx, seg_logy, kind='linear', fill_value=np.nan)

        # Apply interpolation only within segment bounds
        mask = (log_x_query >= seg_logx[0]) & (log_x_query <= seg_logx[-1])
        result[mask] = interp(log_x_query[mask])

    # Convert back from log space
    return np.exp(result)

# Create energy grid for plotting (log scale for wide range)
energy_grid = np.logspace(-3, 0.5, 1000)  # 1 keV to 3.16 MeV

# Create interpolated values using the monotonic interpolation
mu_coh_interp = piecewise_monotonic_interp(MeV, mu_coh, energy_grid)
mu_incoh_interp = piecewise_monotonic_interp(MeV, mu_incoh, energy_grid)
mu_photoelectric_interp = piecewise_monotonic_interp(MeV, mu_photoelectric, energy_grid)
mu_pair_nuclear_interp = piecewise_monotonic_interp(MeV, mu_pair_nuclear, energy_grid)
mu_tot_with_coh_interp = piecewise_monotonic_interp(MeV, mu_tot_with_coh, energy_grid)
mu_tot_without_coh_interp = piecewise_monotonic_interp(MeV, mu_tot_without_coh, energy_grid)

# Create the plot with improved interpolation
plt.figure(figsize=(20, 15))

# Plot each component using monotonic interpolation
plt.loglog(energy_grid, mu_coh_interp, 'r-', linewidth=2, label='Coherent (Rayleigh) Scattering')
plt.loglog(energy_grid, mu_incoh_interp, 'g-', linewidth=2, label='Incoherent (Compton) Scattering')
plt.loglog(energy_grid, mu_photoelectric_interp, 'b-', linewidth=2, label='Photoelectric Absorption')
plt.loglog(energy_grid, mu_pair_nuclear_interp, 'm-', linewidth=2, label='Pair Production (Nuclear Field)')
plt.loglog(energy_grid, mu_tot_with_coh_interp, 'k-', linewidth=3, label='Total (with coherent)')
plt.loglog(energy_grid, mu_tot_without_coh_interp, 'k--', linewidth=2, label='Total (without coherent)')

# Add original data points
plt.loglog(MeV, mu_coh, 'ro', markersize=4)
plt.loglog(MeV, mu_incoh, 'go', markersize=4)
plt.loglog(MeV, mu_photoelectric, 'bo', markersize=4)
plt.loglog(MeV, mu_pair_nuclear, 'mo', markersize=4)
plt.loglog(MeV, mu_tot_with_coh, 'ko', markersize=4)

# Mark the energy of Cs-137 (0.662 MeV)
E_gamma = 0.661657  # MeV
plt.axvline(x=E_gamma, color='cyan', linestyle='--', linewidth=2, label='Cs-137 (0.662 MeV)')

# Function to get interpolated value at a specific point
def interp_value_at_point(energy_grid, interp_values, energy_point):
    """Get value at specific energy using our interpolation results"""
    idx = np.abs(energy_grid - energy_point).argmin()
    return interp_values[idx]

# Find the values at Cs-137 energy using our interpolation
cs137_coh = interp_value_at_point(energy_grid, mu_coh_interp, E_gamma)
cs137_incoh = interp_value_at_point(energy_grid, mu_incoh_interp, E_gamma)
cs137_photoelectric = interp_value_at_point(energy_grid, mu_photoelectric_interp, E_gamma)
cs137_pair = interp_value_at_point(energy_grid, mu_pair_nuclear_interp, E_gamma)
cs137_tot = interp_value_at_point(energy_grid, mu_tot_with_coh_interp, E_gamma)
cs137_tot_nocoh = interp_value_at_point(energy_grid, mu_tot_without_coh_interp, E_gamma)

# MODIFICATION: Replace arrow annotations with text labels
# This creates a text box with the values at Cs-137 energy
cs137_info = (
    f"Values at Cs-137 (0.662 MeV):\n"
    f"μ/ρ_tot = {cs137_tot:.4f} cm²/g\n"
    f"μ/ρ_incoh = {cs137_incoh:.4f} cm²/g\n"
    f"μ/ρ_photo = {cs137_photoelectric:.4f} cm²/g\n"
    f"μ/ρ_coh = {cs137_coh:.4f} cm²/g"
)

# Position the text box in the upper right corner of the plot
'''
plt.text(0.75, 0.7, cs137_info, 
         transform=plt.gca().transAxes, 
         fontsize=30, 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'),
         verticalalignment='top')
'''
# Customize the plot
plt.xlabel('Photon Energy (MeV)', fontsize=30)
plt.ylabel('Mass Attenuation Coefficient (cm²/g)', fontsize=30)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(loc='upper right', fontsize=28, edgecolor='gray')

# Set the x and y limits appropriately
plt.xlim(0.001, 2)
plt.ylim(1e-4, 1e4)

# Add a secondary x-axis for energy in keV
ax1 = plt.gca()
ax2 = ax1.twiny()
ax2.set_xscale('log')
ax2.set_xlim(1, 3000)  # 1 keV to 3000 keV
ax2.set_xlabel('Photon Energy (keV)', fontsize=30)

plt.tight_layout()
plt.savefig('nai_mass_attenuation_full_range_monotonic.png', dpi=600)
plt.show()

# Create a second plot focusing on the Cs-137 energy region
plt.figure(figsize=(12, 9))

# Define a narrower energy range around Cs-137
narrow_energy = np.linspace(0.1, 1.5, 1000)  # 0.1 to 1.5 MeV

# Create narrower range interpolated values
narrow_mu_coh = piecewise_monotonic_interp(MeV, mu_coh, narrow_energy)
narrow_mu_incoh = piecewise_monotonic_interp(MeV, mu_incoh, narrow_energy)
narrow_mu_photoelectric = piecewise_monotonic_interp(MeV, mu_photoelectric, narrow_energy)
narrow_mu_pair_nuclear = piecewise_monotonic_interp(MeV, mu_pair_nuclear, narrow_energy)
narrow_mu_tot_with_coh = piecewise_monotonic_interp(MeV, mu_tot_with_coh, narrow_energy)

# Plot the curves on linear scales for better detail
plt.plot(narrow_energy, narrow_mu_coh, 'r-', linewidth=2, label='Coherent (Rayleigh) Scattering')
plt.plot(narrow_energy, narrow_mu_incoh, 'g-', linewidth=2, label='Incoherent (Compton) Scattering')
plt.plot(narrow_energy, narrow_mu_photoelectric, 'b-', linewidth=2, label='Photoelectric Absorption')
plt.plot(narrow_energy, narrow_mu_pair_nuclear, 'm-', linewidth=2, label='Pair Production (Nuclear Field)')
plt.plot(narrow_energy, narrow_mu_tot_with_coh, 'k-', linewidth=3, label='Total (with coherent)')

# Mark Cs-137 energy
plt.axvline(x=E_gamma, color='cyan', linestyle='--', linewidth=2, label='Cs-137 (0.662 MeV)')

# Filter out data points within our energy range to show on plot
mask = (MeV >= 0.1) & (MeV <= 1.5)
plt.plot(MeV[mask], mu_coh[mask], 'ro', markersize=6)
plt.plot(MeV[mask], mu_incoh[mask], 'go', markersize=6)
plt.plot(MeV[mask], mu_photoelectric[mask], 'bo', markersize=6)
plt.plot(MeV[mask], mu_pair_nuclear[mask], 'mo', markersize=6)
plt.plot(MeV[mask], mu_tot_with_coh[mask], 'ko', markersize=6)

# Calculate contribution percentages at Cs-137 energy
compton_ratio = cs137_incoh / cs137_tot * 100
photoelectric_ratio = cs137_photoelectric / cs137_tot * 100
coherent_ratio = cs137_coh / cs137_tot * 100
pair_ratio = cs137_pair / cs137_tot * 100

# MODIFICATION: Use a structured format for information display with better positioning
info_text = (
    f"At Cs-137 energy (0.662 MeV):\n"
    f"Total μ/ρ = {cs137_tot:.4f} cm²/g\n"
    f"Compton: {compton_ratio:.1f}%\n"
    f"Photoelectric: {photoelectric_ratio:.1f}%\n"
    f"Coherent: {coherent_ratio:.2f}%\n"
    f"Pair Production: {pair_ratio:.2f}%"
)

# Position the text in the upper left corner with better styling
plt.text(0.69, 0.7, info_text, 
         transform=plt.gca().transAxes, 
         fontsize=30, 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'),
         verticalalignment='top')

plt.xlabel('Photon Energy (MeV)', fontsize=30)
plt.ylabel('Mass Attenuation Coefficient (cm²/g)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize=30, edgecolor='gray')

plt.tight_layout()
plt.savefig('nai_mass_attenuation_cs137_range_monotonic.png', dpi=600)
plt.show()
#%%