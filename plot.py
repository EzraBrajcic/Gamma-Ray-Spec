#%%
import numpy as np
import matplotlib.pyplot as plt

# Constants
E0 = 662.0  # keV, incident photon energy (from annihilation)
mec2 = 511.0  # keV, electron rest energy

# Define a range of scattering angles (avoid 0 and 180 to prevent division by zero)
theta = np.linspace(0.001, np.pi - 0.001, 10000)

# Scattered photon energy as a function of angle
E_prime = E0 / (1 + (E0 / mec2) * (1 - np.cos(theta)))  # simplified since E0 = mec2

# Klein-Nishina differential cross-section per unit solid angle (in arbitrary units)
r0_squared = 1.0  # normalized constant
ratio = E_prime / E0
d_sigma_dOmega = (r0_squared / 2.0) * (ratio**2) * (1/ratio + ratio - np.sin(theta)**2)

# Convert to probability density function over energy using the Jacobian
dE_dtheta = np.gradient(E_prime, theta)
dOmega_dtheta = 2 * np.pi * np.sin(theta)
dE_dOmega = dE_dtheta / dOmega_dtheta
pdf_energy = d_sigma_dOmega / np.abs(dE_dOmega)

# Sort by energy for plotting
sort_indices = np.argsort(E_prime)
E_prime_sorted = E_prime[sort_indices]
pdf_sorted = pdf_energy[sort_indices]
pdf_sorted /= np.trapz(pdf_sorted, E_prime_sorted)  # Normalize to unit area

# Plot
plt.figure(figsize=(10, 6))
plt.plot(E_prime_sorted, pdf_sorted, label="PDF of Scattered Photon Energy", color='darkorange')
plt.axvline(x=184, color='red', linestyle='--', label='Backscatter Peak (~170 keV)')
plt.axvline(x=E0, color='green', linestyle='--', label='Compton Edge (511 keV)')
plt.xlabel("Scattered Photon Energy (keV)")
plt.ylabel("Probability Density (1/keV)")
plt.title("Photon Energy PDF for 511 keV Compton Scattering")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
#%%