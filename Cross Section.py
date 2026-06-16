#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import Gammaspeclib

# Constants & Simple Models
E_gamma = 0.661657      # MeV, e.g. Cs-137
mec2 = 0.510999         # MeV
r0 = 2.81794e-13        # cm, classical electron radius
hc   = 1.9732696e-11    # MeV·cm
dE = 0.00148

x_values = np.array([
    0.0, 5e-3, 1e-2, 1.5e-2, 2e-2,
    2.5e-2, 3e-2, 4e-2, 5e-2, 7e-2,
    9e-2, 1e-1, 1.25e-1, 1.5e-1, 1.75e-1,
    2e-1, 2.5e-1, 3e-1, 4e-1, 5e-1,
    6e-1, 7e-1, 8e-1, 9e-1, 1.0,
    1.25, 1.5, 2.0, 2.5, 3.0,
    3.5, 4.0, 5.0, 6.0, 7.0,
    8.0, 1.0e1, 1.5e1, 2.0e1, 5.0e1,
    8.0e1, 1.0e2, 1.0e3, 1.0e6, 1.0e9,
]) * 1e8

# Na (Sodium) scattering values
S_values_Na = np.array([
    0.0000,     9.0000e-03, 3.6000e-02, 7.9300e-02, 1.3780e-01,
    2.0920e-01, 2.9120e-01, 4.7640e-01, 6.7400e-01,
    1.0490e+00, 1.3642e+00, 1.5030e+00, 1.8282e+00,
    2.1600e+00, 2.5150e+00, 2.8910e+00, 3.6672e+00,
    4.4310e+00, 5.8040e+00, 6.9030e+00, 7.7240e+00,
    8.3130e+00, 8.7290e+00, 9.0280e+00, 9.2520e+00,
    9.6465e+00, 9.9390e+00, 1.0376e+01, 1.0654e+01,
    1.0813e+01, 1.0900e+01, 1.0946e+01, 1.0983e+01,
    1.0994e+01, 1.0998e+01, 1.0990e+01, 1.1000e+01,
    1.1000e+01, 1.1000e+01, 1.1000e+01, 1.1000e+01,
    1.1000e+01, 1.1000e+01, 1.1000e+01, 1.1000e+01
])

# I (Iodine) scattering values
S_values_I = np.array([
    0.0000e+00, 1.3000e-02, 5.6000e-02, 1.2050e-01, 2.1280e-01, 3.2960e-01,
    4.6960e-01, 8.1320e-01, 1.2300e+00, 2.2213e+00, 3.3314e+00, 3.9030e+00,
    5.3281e+00, 6.7090e+00, 8.0300e+00, 9.2870e+00, 1.1579e+01, 1.3564e+01,
    1.6876e+01, 1.9777e+01, 2.2471e+01, 2.4980e+01, 2.7269e+01, 2.9298e+01,
    3.1056e+01, 3.4474e+01, 3.7024e+01, 4.0827e+01, 4.3529e+01, 4.5526e+01,
    4.7054e+01, 4.8233e+01, 4.9811e+01, 5.0714e+01, 5.1266e+01, 5.1647e+01,
    5.2165e+01, 5.2770e+01, 5.2937e+01, 5.2999e+01, 5.3000e+01, 5.3000e+01,
    5.3000e+01, 5.3000e+01, 5.3000e+01
])

S_interp_Na = interp1d(x_values, S_values_Na,
                       bounds_error=False,
                       fill_value=(S_values_Na[0], S_values_Na[-1]))

S_interp_I = interp1d(x_values, S_values_I,
                      bounds_error=False,
                      fill_value=(S_values_I[0], S_values_I[-1]))

S_values_NaI = (S_values_Na/11 + S_values_I/53)/2
S_interp_NaI = interp1d(x_values, S_values_NaI,
                        bounds_error=False,
                        fill_value=(S_values_NaI[0], S_values_NaI[-1]))

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

MeV, mu_coh, mu_incoh, mu_photoelectric, mu_pair_nuclear, mu_tot_with_coh, mu_tot_without_coh = attenuation_table.T


# Load data & Fit the Photopeak to find sigma
data = np.loadtxt("part4caesium.csv", skiprows=28, delimiter=',')

popt_pp, _ = curve_fit(Gammaspeclib.gaussian_model, data[430:470, 1], data[430:470, 4],
                      p0=[data[450, 4], data[450, 1], 0.9])
A_pp, mu_pp, sigma_pp = popt_pp

# --- Prepare the Compton region ---
E_com = data[190:406, 1]
N_com = data[190:406, 4]

half_kernel = sigma_pp / dE
x_kernel = np.arange(-half_kernel, half_kernel + 1) * dE
kernel = np.exp(- x_kernel**2 / (2 * sigma_pp**2))
kernel /= np.trapz(kernel, x_kernel)

N_smeared = np.convolve(N_com, kernel, mode='same') * dE

E_plot = data[180:500, 1]
gauss_fit = Gammaspeclib.gaussian_model(E_plot, *popt_pp)
interp_func = interp1d(E_com, N_smeared, kind='linear', fill_value="extrapolate")
N_smeared_interp = interp_func(E_plot)
N_smeared_interp[E_plot > E_com[-1]] = np.maximum(0, N_smeared_interp[E_plot > E_com[-1]])
combined_model = gauss_fit + N_smeared_interp
integral = np.trapz(gauss_fit)
print(f'peak counts = {integral}')
print(f'uncertainty = {integral*sigma_pp}')
print(f'sigma = {sigma_pp}\n')

# Plot raw photon spectrum (for reference)
plt.figure(figsize=(20, 15))
plt.plot(data[:450, 1], data[:450, 4], 'o', ms=4, label='Observed Counts', alpha=0.5, color = 'black')
plt.plot(data[200:500, 1], Gammaspeclib.gaussian_model(data[200:500, 1], *popt_pp), lw=2, label='Photopeak Gaussian Fit', color='blue')
plt.plot(E_plot, N_smeared_interp, '-', lw=2, label=f'Convolved Response (σ={sigma_pp:.3f} MeV)', color='red')
plt.plot(E_plot, combined_model, '--', lw=2, label='Combined Model (Gaussian + Convolution)', color='magenta')

# Determine the detected Compton edge as the minimum gradient point of the smeared counts.
dN_dE = np.gradient(N_smeared, E_com)
edge_idx = np.argmin(dN_dE)
E_edge_detected = E_com[edge_idx]
plt.axvline(E_edge_detected, color='black', ls='--', label=f'Estimated Compton Edge ({E_edge_detected:.3f} MeV)')

plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel('Counts', fontsize=30)
plt.xlim(0.35, 0.665)
plt.grid(True, alpha=0.3)
plt.legend(loc = 'upper left', fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.show()

# Use the original energy grid from data
E_grid = data[18:, 1]
dE = np.mean(np.diff(E_grid))
energy_bins = data[18:450, 1]

# Compute bin widths for non-uniform grid
dE_bins = np.empty_like(E_grid)
dE_bins[:-1] = np.diff(E_grid)
dE_bins[-1] = dE_bins[-2]

# Theoretical Compton edge in deposited energy
T_max = E_gamma * (2 * (E_gamma / mec2)) / (1 + 2 * (E_gamma / mec2))

# Define backscatter peak and Compton edge energies
E_bsp = 0.184  # MeV, backscatter peak (left side, stays fixed)
E_ce = T_max   # MeV, Compton edge (right side, to be shifted)

# Detector properties
activity = 253152.0543 * 0.851     # Bq
flux = 201.452004 * 0.851          # cm^-2 s^-1
detector_radius = 1.905            # cm
detector_thickness = 3.81          # cm
measurement_time = 600             # seconds
source_distance = 9.3               # cm

# --- Compute electron density from molar density of NaI(Tl) ---
# Density and molar mass
rho_NaI   = 3.667                   # g/cm³
M_NaI     = 22.9897 + 126.9045      # g/mol
mol_per_cm3 = rho_NaI / M_NaI       # mol/cm³
N_A       = 6.02214076e23           # mol⁻¹
e_per_unit = (11 + 53)            # electrons per formula unit

electron_density = mol_per_cm3 * N_A * e_per_unit

mu_lin = mu_tot_with_coh * rho_NaI
mu_energy = interp1d(
    MeV,
    mu_lin,
    kind="linear",
    bounds_error=False,
    fill_value=mu_lin[0]
)
print(mu_energy(E_gamma))
mu_compton_lin = mu_incoh * rho_NaI
mu_compton = interp1d(
    MeV,
    mu_compton_lin,
    kind='linear',
    bounds_error=False,
    fill_value=(mu_compton_lin[0], mu_compton_lin[-1])
)

N = len(energy_bins)
convolved_observed = Gammaspeclib.apply_detector_response(energy_bins, data[18:18+N, 4], Gammaspeclib.energy_resolution)
# Calculate the differential cross section directly for deposited energy
dSigma_dT = Gammaspeclib.klein_nishina_with_incoh_func(E_grid, E_gamma, S_interp_NaI)

P_abs, P_esc, avg_L = Gammaspeclib.probabilities(
                E_grid, E_gamma, detector_thickness, detector_radius,
                mu_energy, mu_compton, source_distance
                )
print(avg_L)
incident_photons = activity * (1-source_distance/np.sqrt(detector_radius**2+source_distance**2))/2 * measurement_time  # total photons hitting detector
print(incident_photons)
pretrans = np.exp(-((2.52657034e-1 * 0.05 * 2.7) + (1.80453353e-1 * 10 * 0.001225)))

response = Gammaspeclib.apply_detector_response(E_grid, P_esc * (dSigma_dT * dE_bins)/(np.trapz(dSigma_dT, x = E_grid)) * (1 - np.exp(-1 * np.trapz(dSigma_dT, x = E_grid) * electron_density * avg_L)), Gammaspeclib.energy_resolution)

expected_counts = incident_photons * pretrans * response

# 8) Plot updated spectrum
plt.figure(figsize=(20, 15))
plt.plot(energy_bins, expected_counts[:N],
         label='Escaped Compton Scattered γ-ray Detector Response', lw=2, alpha=0.8, color = 'red')
plt.plot(data[:450, 1], data[:450, 4], 'o', ms=4,
         label='Observed Counts', alpha=0.5, color = 'black')
plt.plot(data[18:430, 1], convolved_observed[:N-20] - expected_counts[:N-20],
         label = 'Observed - Expected Response', color = 'magenta')
plt.plot(data[18:430, 1], convolved_observed[:N-20], label = 'Convolved Observed Spectrum', color = 'blue')
plt.axvline(E_bsp, color="black", ls="--", 
            label=f"Backscatter Peak ({E_bsp:.3f} MeV)")

# Edge detection
dN_dE = np.gradient(expected_counts[:N], energy_bins)
edge_idx = np.argmin(dN_dE)
E_edge = energy_bins[edge_idx]
plt.axvline(E_edge, color='blue', ls='--', label=f'Estimated Compton Edge ({E_edge:.3f} MeV)')

plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel('Counts', fontsize=30)
plt.xlim(0.01, 0.55)
plt.ylim(0.0)
plt.grid(True, alpha=0.3)
plt.legend(loc = 'upper left', fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.show()

#Calculate the integrated KN cross-section with incoherent scattering function
# for each deposited energy point
# Calculate the pure Klein-Nishina differential cross section (without incoherent scattering)
# Calculate the pure Klein-Nishina differential cross section (without incoherent scattering)
dSigma_dT_pure = Gammaspeclib.klein_nishina_E(E_grid, E_gamma)

# Calculate Klein-Nishina with incoherent scattering function for NaI
dSigma_dT_with_scattering = Gammaspeclib.klein_nishina_with_incoh_func(E_grid, E_gamma, S_interp_NaI)

# Apply detector response convolution to both versions
dSigma_dT_pure_convolved = Gammaspeclib.apply_detector_response(
    E_grid, dSigma_dT_pure, Gammaspeclib.energy_resolution
)
dSigma_dT_with_scattering_convolved = Gammaspeclib.apply_detector_response(
    E_grid, dSigma_dT_with_scattering, Gammaspeclib.energy_resolution
)

# After the first scatter, the remaining photon energy is E' = E_gamma - T
E_prime = E_gamma - E_grid

# Compute attenuation coefficients at E'
mu_compton_Eprime = mu_compton(E_prime)
mu_total_Eprime = mu_energy(E_prime)

# Avoid division by zero
with np.errstate(divide='ignore', invalid='ignore'):
    compton_fraction = np.where(mu_total_Eprime > 0, mu_compton_Eprime / mu_total_Eprime, 0.0)

# Split probabilities after first scatter
P_abs_compton = P_abs[:N] * compton_fraction[:N]
P_esc_compton = P_esc[:N] * compton_fraction[:N]
P_abs_other = P_abs[:N] - P_abs_compton
P_esc_other = P_esc[:N] - P_esc_compton

# Ensure all probabilities are physically meaningful
P_abs_compton = np.clip(P_abs_compton, 0, P_abs[:N])
P_esc_compton = np.clip(P_esc_compton, 0, P_esc[:N])
P_abs_other = np.clip(P_abs_other, 0, P_abs[:N])
P_esc_other = np.clip(P_esc_other, 0, P_esc[:N])

# Plot probabilities
plt.figure(figsize=(20, 15))
plt.plot(E_grid[:N], P_abs[:N], color='blue', lw=3,
         label='Total Absorption Probability')
plt.plot(E_grid[:N], P_esc[:N], color='red', lw=3,
         label='Total Escape Probability')
plt.plot(E_grid[:N], P_abs_compton, color='darkblue', lw=3, ls='--',
         label='Absorption via Compton')
plt.plot(E_grid[:N], P_esc_compton, color='purple', lw=3, ls='--',
         label='Escape via Compton')
plt.plot(E_grid[:N], P_abs_other, color='skyblue', lw=3, ls=':',
         label='Absorption via Other')
plt.plot(E_grid[:N], P_esc_other, color='salmon', lw=3, ls=':',
         label='Escape via Other')

# Improve appearance
plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel('Probability', fontsize=30)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=30, loc='upper left')
plt.xlim(0.01, 0.477)
plt.ylim(0, 1.05)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.savefig('interaction_probabilities_kn.png', dpi=600)
plt.show()

# Calculate total cross sections for reference
total_xs_pure = np.trapz(dSigma_dT_pure, x=E_grid)
total_xs_with_scattering = np.trapz(dSigma_dT_with_scattering, x=E_grid)
print(f'Pure Klein-Nishina total cross section: {total_xs_pure:.6e} cm²')
print(f'Klein-Nishina with incoherent scattering total cross section: {total_xs_with_scattering:.6e} cm²')
print(f'Ratio: {total_xs_with_scattering/total_xs_pure:.4e}')

# Create an improved plot comparing the differential cross sections
fig = plt.figure(figsize = (20, 15))

# Plot the raw cross sections
plt.subplot(2, 1, 1)
plt.plot(E_grid[:N], dSigma_dT_pure[:N], 
         label='Klein-Nishina', 
         color='lime', 
         linestyle='-', 
         linewidth=2)
plt.plot(E_grid[:N], dSigma_dT_pure_convolved[:N], 
         label='Klein-Nishina (convolved)', 
         color='magenta',  
         linewidth=2)
plt.xlabel('Energy (MeV)', fontsize=30)
plt.grid(True, alpha=0.3)
plt.text(0.02, 0.92, "a)", transform=plt.gca().transAxes, fontsize=30, fontweight='bold')
plt.xlim(0, 0.55)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30)

plt.subplot(2, 1, 2)
plt.plot(E_grid[:N], dSigma_dT_with_scattering[:N], 
         label='Klein-Nishina with S(x)', 
         color='blue', 
         linestyle='-', 
         linewidth=2)
plt.plot(E_grid[:N], dSigma_dT_with_scattering_convolved[:N], 
         label='Klein-Nishina with S(x) (convolved)', 
         color='red', 
         linewidth=2)
plt.xlabel('Energy (MeV)', fontsize=30)
plt.xlim(0, 0.55)
plt.legend(fontsize=30)
plt.grid(True, alpha=0.3)

fig.supylabel(r'Differential Cross Section $d\sigma/dE$ (cm$^2$MeV$^{-1}$)', fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)    
plt.tight_layout()
plt.show()

# Plot the ratio of cross sections to highlight the effect of the incoherent scattering function
plt.figure(figsize=(20, 15))
ratio = dSigma_dT_with_scattering / dSigma_dT_pure
plt.plot(E_grid[3:N], ratio[3:N],
         label=r'Ratio: $d\sigma/dE$ S(x) / $d\sigma/dE$', 
         color='blue', ms = 4)
plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel(r'$d\sigma/dE$ S(x) / $d\sigma/dE$', fontsize=30)
plt.grid(True, alpha=0.3)
plt.text(0.02, 0.92, "b)", transform=plt.gca().transAxes, fontsize=30, fontweight='bold')
plt.legend(fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.show()

# Calculate expected counts incorporating absorption probability
expected_counts_absorbed = incident_photons * pretrans * P_abs * (dSigma_dT * dE_bins)/(np.trapz(dSigma_dT, x = E_grid)) * (1 - np.exp(-1 * np.trapz(dSigma_dT, x = E_grid) * electron_density * avg_L))
print(np.sum(expected_counts_absorbed))

# Calculate expected counts incorporating escape probability
expected_counts_escaped = incident_photons * pretrans * Gammaspeclib.apply_detector_response(E_grid, P_esc * (dSigma_dT * dE_bins)/(np.trapz(dSigma_dT, x = E_grid)) * (1 - np.exp(-1 * np.trapz(dSigma_dT, x = E_grid) * electron_density * avg_L)), Gammaspeclib.energy_resolution)
print(np.sum(expected_counts_escaped))

counts_remaining = np.sum(data[:N-20, 4] - expected_counts_escaped[:N-20])
print(f'{counts_remaining} Counts unaccounted for')
print(f'{np.sum(expected_counts_absorbed)-273968.97169182834} Absorbed count difference under photopeak')
# Create comprehensive figure with multiple panels
plt.figure(figsize=(20, 15))
plt.plot(E_grid[:N], expected_counts_escaped[:N], 
         label='Escaped Compton Scattered γ-ray Detector Response', 
         color='red', 
         linewidth=2)
plt.plot(energy_bins, data[18:450, 4], 'o', ms=4,
         label='Observed Counts', alpha=0.5, color = 'black')
plt.plot(E_grid[:N], Gammaspeclib.gaussian_model(E_grid[:N], *popt_pp),
         lw=2, label='Photopeak Fit', color='blue')

# Edge detection
dN_dE = np.gradient(expected_counts_escaped[:N], E_grid[:N])
edge_idx = np.argmin(dN_dE)
E_edge = E_grid[edge_idx]
# Add vertical line for Compton edge
plt.axvline(T_max, color='blue', linestyle='--', 
           label=f'Estimated Compton Edge ({E_edge:.3f} MeV)')

# Label the backscatter peak region
E_bsp = 0.184  # MeV, backscatter peak
plt.axvline(E_bsp, color='black', linestyle='--', 
           label=f'Backscatter Peak ({E_bsp:.3f} MeV)')

plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel('Counts', fontsize=30)
plt.legend(loc = 'upper left', fontsize=30)
plt.grid(True, alpha=0.3)
plt.xlim(0.01, 0.65)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.show()

# Create comprehensive figure with multiple panels
plt.figure(figsize=(20, 15))
plt.plot(E_grid[:N], expected_counts_absorbed[:N], 
         label='Absorbed Compton Scattered γ-rays', 
         color='red', 
         linewidth=2)

# Add vertical line for Compton edge
plt.axvline(0.478, color='black', linestyle='--', 
           label=f'Compton Edge ({0.478:.3f} MeV)')

plt.xlabel('Energy (MeV)', fontsize=30)
plt.ylabel('Counts', fontsize=30)
plt.legend(fontsize=30)
plt.grid(True, alpha=0.3)
plt.xlim(0.01, 0.55)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.tight_layout()
plt.show()
#%%