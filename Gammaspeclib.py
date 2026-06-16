import numpy as np
from scipy.interpolate import interp1d
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import gc

# -----------------------------
# 1) Constants & Simple Models
# -----------------------------
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

def gaussian_model(x, amplitude, mean, sigma):
    """Simple Gaussian for fitting the photopeak."""
    norm = amplitude / (sigma * np.sqrt(2 * np.pi))
    return norm * np.exp(-(x - mean)**2 / (2 * sigma**2))

def klein_nishina_E(T_grid, E_gamma):
    """
    Returns Klein-Nishina differential cross section dσ/dT
    for deposited energy T = E_gamma - E',
    _including_ the incoherent‐scattering factor for Na.
    """
    # --- your existing theta, alpha, E_prime, T_vals … ---
    theta = np.linspace(0.001, np.pi - 0.001, 10000)
    alpha = E_gamma / mec2
    E_prime = E_gamma / (1 + alpha * (1 - np.cos(theta)))
    T_vals = E_gamma - E_prime

    # Differential cross section dσ/dΩ
    ratio = E_prime / E_gamma
    d_sigma_dOmega = (r0**2 / 2) * ratio**2 * (ratio + 1/ratio - np.sin(theta)**2)

    # Chain rule: dσ/dT = (dσ/dΩ) / (dT/dΩ)
    dT_dtheta   = np.gradient(T_vals, theta)
    dOmega_dtheta = 2 * np.pi * np.sin(theta)
    d_sigma_dT  = d_sigma_dOmega / np.abs(dT_dtheta / dOmega_dtheta)

    # Interpolate onto desired deposited-energy grid
    idx = np.argsort(T_vals)
    T_sorted = T_vals[idx]
    d_sigma_dT_sorted = d_sigma_dT[idx]

    interp_sigma = interp1d(T_sorted, d_sigma_dT_sorted,
                            bounds_error=False, fill_value=0)

    return interp_sigma(T_grid)

def klein_nishina_total(E_gamma):
    """Calculate total Klein-Nishina cross section (cm²) per electron"""
    alpha = E_gamma / mec2
    
    term1 = 2 * np.pi * r0**2
    term2 = (1 + alpha) / (alpha**3)
    term3 = (2 * alpha * (1 + alpha)) / (1 + 2*alpha) - np.log(1 + 2*alpha)
    term4 = np.log(1 + 2*alpha) / (2*alpha)
    term5 = -(1 + 3*alpha) / ((1 + 2*alpha)**2)
    
    return term1 * (term2 * term3 + term4 + term5)

def energy_resolution(E):
    """Resolution as function of deposited energy."""
    return 0.076638229371 * np.sqrt(E)/(2 * np.sqrt(2 * np.log(2)))

# Apply detector response function to the deposited energy spectrum
def apply_detector_response(T_grid, dSigma_dT, sigma_func):
    dSigma_sm = np.zeros_like(dSigma_dT)
    
    dE = np.empty_like(T_grid)
    dE[:-1] = np.diff(T_grid)
    dE[-1]  = dE[-2]
    
    for i, T_obs in enumerate(T_grid):
        for j, T_true in enumerate(T_grid):
            if dSigma_dT[j] <= 0:
                continue
            sigma = sigma_func(T_true)
            if sigma <= 0:
                continue
            # resp has units 1/MeV, multiply by dE[j] → dimensionless weight
            resp = (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-(T_obs - T_true)**2/(2*sigma**2))
            dSigma_sm[i] += dSigma_dT[j] * resp * dE[j]
    return dSigma_sm

def eff_func(E_MeV, t0, t1, t2, t3, t4, t5, t6):
    # Convert to keV for the log formula
    E_keV = E_MeV * 1000.0
    x = np.log(E_keV / 100.0)
    y = np.log(E_keV / 1000.0)
    a = np.clip(t0 + t1 * x + t2 * x**2, 1e-6, None)
    b = np.clip(t4 + t5 * y + t6 * y**2, 1e-6, None)
    inside = (a**(-t3) + b**(-t3))**(-1.0 / t3)
    return np.exp(-inside)

def klein_nishina_with_incoh_func(T_grid, E_gamma, S_interp):
    """
    Returns dσ/dT including energy-dependent, incoherent scattering functions.
    """
    
    # Generate improved θ grid for scattering angles
    n_theta = 1000  # More points for better accuracy
    theta = np.linspace(1e-6, np.pi-1e-6, n_theta)
    
    # Calculate energy transfer for each scattering angle
    alpha = E_gamma / mec2
    E_prime = E_gamma / (1 + alpha * (1 - np.cos(theta)))
    T_vals = E_gamma - E_prime
    
    # Differential cross section dσ/dΩ with Klein-Nishina formula
    ratio = E_prime / E_gamma
    d_sigma_dOmega = (r0**2 / 2) * ratio**2 * (ratio + 1/ratio - np.sin(theta)**2)
    
    # Apply incoherent‐scattering factor S(x) with improved accuracy
    x_theta = np.sin(theta/2) / (hc / E_gamma)
    S_values = S_interp(x_theta)
    
    # Apply scattering factor with bounds checking
    valid_idx = ~np.isnan(S_values) & ~np.isinf(S_values)
    d_sigma_dOmega[valid_idx] *= S_values[valid_idx]
    d_sigma_dOmega[~valid_idx] = 0.0
    
    # Precompute quantities for scattering events
    dT_dtheta = np.gradient(T_vals, theta)
    dOmega_dtheta = 2 * np.pi * np.sin(theta)
    
    # Apply chain rule with careful handling of edge cases
    d_sigma_dT = np.zeros_like(theta, dtype=float)
    
    # Only compute for valid indices
    if np.any(valid_idx):
        d_sigma_dT[valid_idx] = (d_sigma_dOmega[valid_idx] / np.abs(dT_dtheta[valid_idx] / dOmega_dtheta[valid_idx]))
    
    # Sort by T_vals for interpolation
    idx = np.argsort(T_vals)
    T_sorted = T_vals[idx]
    d_sigma_dT_sorted = d_sigma_dT[idx]
    
    # When ready to add interpolated values:
    if len(T_sorted) >= 2:
        interp = interp1d(
            T_sorted, 
            d_sigma_dT_sorted, 
            kind='linear',
            bounds_error=False, 
            fill_value=0.0
        )
        final_d_sigma_dT = interp(T_grid)

    return final_d_sigma_dT  # Return the accumulated result

def probabilities(T_grid, E_gamma, thickness, detector_radius, mu_energy, mu_energy_compton, source_distance,
                  num_threads=None, n_theta=500, N_incident=300, n_z=150, n_phi_scat=200):
    
    # Use available CPU cores if num_threads not specified
    if num_threads is None:
        num_threads = max(1, multiprocessing.cpu_count() - 1)
    
    print(f"Starting calculation with {num_threads} threads...")
    
    # First create a fine grid to calculate the KN distribution accurately
    theta_fine = np.linspace(1e-10, np.pi-1e-10, 10000)
    alpha = E_gamma / mec2
    E_prime_fine = E_gamma / (1 + alpha * (1 - np.cos(theta_fine)))
    
    # Apply incoherent‐scattering factor S(x) with improved accuracy
    x_theta = np.sin(theta_fine/2) / (hc / E_gamma)
    S_values = S_interp_NaI(x_theta)
    
    # Calculate KN differential cross section
    ratio = E_prime_fine / E_gamma
    dSigma_dOmega_fine = (r0**2 / 2) * ratio**2 * (ratio + 1/ratio - np.sin(theta_fine)**2) * S_values
    
    # Convert to dσ/dθ
    dSigma_dTheta_fine = dSigma_dOmega_fine * 2 * np.pi * np.sin(theta_fine)
    
    # Create CDF for inverse transform sampling
    cdf = np.cumsum(dSigma_dTheta_fine)
    cdf = cdf / cdf[-1]  # Normalize to [0,1]
    
    # Clean up memory from step 1
    del dSigma_dOmega_fine, dSigma_dTheta_fine
    gc.collect()
    
    # Use inverse transform sampling to get KN-distributed angles
    uniform_samples = np.linspace(0, 1, n_theta)
    theta_scat = np.interp(uniform_samples, cdf, theta_fine)
    
    # Clean up memory from step 2
    del uniform_samples, cdf, theta_fine
    gc.collect()
    
    # Calculate energies and transfers for these angles
    E_prime = E_gamma / (1 + alpha * (1 - np.cos(theta_scat)))
    T_vals = E_gamma - E_prime
    
    # Get total attenuation coefficient from the passed function
    mu_tot_inc = mu_energy(E_gamma)
    mu_compton_inc = mu_energy_compton(E_gamma)
    
    # Calculate attenuation for scattered photons - optimized
    mu_tot_sc = np.zeros_like(E_prime)
    valid_E_prime = E_prime >= 0
    
    # Calculate attenuation for scattered photons - vectorized
    mu_tot_sc = np.zeros_like(E_prime)
    valid_E_prime = E_prime >= 0
    mu_tot_sc[valid_E_prime] = np.array([mu_energy(ep) for ep in E_prime[valid_E_prime]])
    
    # Define the incident beam cone angle
    theta_inc_max = np.arctan(detector_radius/source_distance)
    theta_inc = np.linspace(0+1e-10, theta_inc_max-1e-10, N_incident)
    
    # PDF for incoming photon angles (normalized)
    pdf = np.sin(theta_inc) / (1 - np.cos(theta_inc_max))
    
    # Create phi values just once
    phi_scat = np.linspace(0.0 + 1e-10, 2*np.pi, n_phi_scat, endpoint=False)
    dphi = 2*np.pi / n_phi_scat  # Pre-calculate for later use
    
    # Helper function for vector rotation
    def rotate_from_z_axis(theta_val, phi_val):
        """
        Create direction vector from angles theta and phi,
        where theta is angle from z-axis and phi is azimuthal angle.
        """
        return np.array([
            np.sin(theta_val) * np.cos(phi_val),
            np.sin(theta_val) * np.sin(phi_val),
            np.cos(theta_val)
        ])
    
    def rodrigues(v, k, angle):
        """
        Vectorized Rodrigues' rotation formula.
        v, k: (..., 3)
        angle: (..., 1)
        Returns rotated vectors (..., 3)
        """
        k_norm = np.linalg.norm(k, axis=-1, keepdims=True)
        k_unit = np.where(k_norm < 1e-10, k, k / k_norm)

        cos_ang = np.cos(angle)  # shape (..., 1)
        sin_ang = np.sin(angle)  # shape (..., 1)

        dot = np.sum(v * k_unit, axis=-1, keepdims=True)

        return (
            v * cos_ang +
            np.cross(k_unit, v) * sin_ang +
            k_unit * dot * (1 - cos_ang)
        )
    
    def pick_perp_ref(incident_vec):
        """
        Returns a unit vector perpendicular to incident_vec.
        incident_vec: array-like of shape (3,)
        """
        v = np.asarray(incident_vec, dtype=np.float64)
        v = v / np.linalg.norm(v)  # Ensure unit vector
        
        # Find the smallest component of the vector
        abs_v = np.abs(v)
        min_idx = np.argmin(abs_v)
        
        # Create a basis vector with 1 in that position
        e = np.zeros(3, dtype=np.float64)
        e[min_idx] = 1.0
        
        # Take cross product of v with this basis vector
        # This gives a vector guaranteed to be perpendicular to v
        perp = np.cross(v, e)
        
        # If the cross product is too small, try a different basis vector
        norm = np.linalg.norm(perp)
        if norm < 1e-10:
            # Try a different basis vector
            e = np.zeros(3, dtype=np.float64)
            e[(min_idx + 1) % 3] = 1.0
            perp = np.cross(v, e)
            norm = np.linalg.norm(perp)
            
            if norm < 1e-10:
                # If still too small, try the third basis vector
                e = np.zeros(3, dtype=np.float64)
                e[(min_idx + 2) % 3] = 1.0
                perp = np.cross(v, e)
                norm = np.linalg.norm(perp)
        
        # Normalize
        perp = perp / np.linalg.norm(perp)
        return perp
    
    # Vectorized ray-cylinder intersection
    def ray_cylinder_intersect(x0s, y0s, z0s, dirs, radius, height):
        """
        Compute intersection lengths for rays with a cylinder.
        x0s, y0s, z0s: arrays shape (n_z,1,1)
        dirs: array shape (n_z,n_theta,n_phi,3)
        radius: scalar
        height: scalar
        Returns: t values shape (n_z,n_theta,n_phi)
        """
        dx = dirs[..., 0]
        dy = dirs[..., 1]
        dz = dirs[..., 2]

        # Intersection with top and bottom planes
        with np.errstate(divide='ignore', invalid='ignore'):
            t_top    = (height - z0s) / dz
            t_bottom = -z0s / dz

        # Initialize t as infinite
        t = np.full_like(dx, np.inf)

        # Test top plane
        xt = x0s + dx * t_top
        yt = y0s + dy * t_top
        mask_top = (dz != 0) & (t_top > 0) & (xt*xt + yt*yt <= radius**2)
        t = np.where(mask_top, np.minimum(t, t_top), t)

        # Test bottom plane
        xb = x0s + dx * t_bottom
        yb = y0s + dy * t_bottom
        mask_bot = (dz != 0) & (t_bottom > 0) & (xb*xb + yb*yb <= radius**2)
        t = np.where(mask_bot, np.minimum(t, t_bottom), t)

        # Intersection with cylindrical side
        a = dx*dx + dy*dy
        b = 2 * (x0s * dx + y0s * dy)
        c = x0s*x0s + y0s*y0s - radius**2
        disc = b*b - 4*a*c
        mask_a = a > 1e-12
        mask_disc = disc >= 0
        sqrt_disc = np.sqrt(np.where(mask_disc, disc, 0))
        t1 = (-b + sqrt_disc) / (2*a)
        t2 = (-b - sqrt_disc) / (2*a)

        # Check t1
        z1 = z0s + dz * t1
        mask1 = mask_a & mask_disc & (t1 > 0) & (z1 >= 0) & (z1 <= height)
        t = np.where(mask1, np.minimum(t, t1), t)

        # Check t2
        z2 = z0s + dz * t2
        mask2 = mask_a & mask_disc & (t2 > 0) & (z2 >= 0) & (z2 <= height)
        t = np.where(mask2, np.minimum(t, t2), t)

        # Replace infinities with zero (no intersection)
        t = np.where(np.isfinite(t), t, 0.0)
        return t
    
    # Vectorized process_incident_angle skeleton
    def process_incident_angle(angle_index):
        # Initialize the contribution for this specific angle
        angle_contribution_abs = np.zeros_like(theta_scat)
        angle_contribution_esc = np.zeros_like(theta_scat)
        angle_contribution_L = 0
        
        # Define theta_i and related values properly
        theta_max = np.arctan(detector_radius / source_distance)
        theta_i = np.linspace(0, theta_max, N_incident)
        current_theta_i = theta_i[angle_index]
        
        # Calculate incident direction vector for this angle
        incident_vec = rotate_from_z_axis(current_theta_i, 0)
        dx_inc, dy_inc, dz_inc = incident_vec
        
        t_e = -source_distance / dz_inc
        x_entry = t_e * dx_inc
        y_entry = t_e * dy_inc
        
        if x_entry*x_entry + y_entry*y_entry > detector_radius**2:
            # Entry point outside detector radius
            return angle_index, angle_contribution_abs, angle_contribution_esc, pdf[angle_index] * angle_contribution_L
        
        # Calculate maximum path length through detector
        L_max = ray_cylinder_intersect(
            x_entry, y_entry, 0.0,
            np.array([dx_inc, dy_inc, dz_inc])[None,None,None,:],
            detector_radius, thickness)[0,0,0]
        
        if L_max <= 0:
            # No intersection with detector
            return angle_index, angle_contribution_abs, angle_contribution_esc, angle_contribution_L
        
        # 4) Depth grid & weights
        depth_vals     = np.linspace(0.0, L_max, n_z)
        depth_weights  = mu_compton_inc * np.exp(-mu_tot_inc * depth_vals)
        depth_weights /= np.trapz(depth_weights, depth_vals)

        # 6) Broadcast
        depth_b = depth_vals[:,None,None]
        theta_b = theta_scat[None,:,None]

        # 7) Points
        x0s = x_entry + dx_inc * depth_b
        y0s = y_entry + dy_inc * depth_b
        z0s = dz_inc  * depth_b

        # 8) References
        perp_ref = pick_perp_ref(incident_vec)

        # incident_vec and perp_ref have shape (3,)
        # We want shapes compatible with (1, 1, 60, 3)

        incident_vec_exp = incident_vec[None, None, None, :]     # (1, 1, 1, 3)
        perp_ref_exp = perp_ref[None, None, None, :]         # (1, 1, 1, 3)

        # 5) Scattering-azimuth grid
        phi_b = phi_scat[None, None, :, None]  # (1, 1, 60, 1)

        # 9) Rotations
        v1 = rodrigues(perp_ref_exp, incident_vec_exp, phi_b)  # shape (1, 1, 60, 3)
        
        incident_b = np.broadcast_to(incident_vec, (1, n_theta, n_phi_scat, 3))
        v1_broadcasted = np.broadcast_to(v1, (1, n_theta, n_phi_scat, 3))
        angles = np.broadcast_to(theta_b[..., None], (1, n_theta, n_phi_scat, 1))

        scattered_ds = rodrigues(incident_b, v1_broadcasted, angles)

        # 10) Intersect
        Ls = ray_cylinder_intersect(
            x0s, y0s, z0s, scattered_ds,
            detector_radius, thickness)

        # 11–12) Escape probs & weighting
        mu_sc = mu_tot_sc[None,:,None]
        esc = np.exp(-mu_sc * Ls)   # esc.shape = (n_z, n_theta, n_phi_scat)
        
        # trapz( esc, dx=dphi, axis=2 ) gives ∫ esc dφ
        # dividing by 2π then gives the average
        mean_phi = np.trapz(esc, dx=dphi, axis=2) / (2*np.pi)
        P_abs_ang = np.trapz(depth_weights[:,None] * (1 - mean_phi), x=depth_vals, axis=0)
        P_esc_ang = np.trapz(depth_weights[:,None] * mean_phi, x=depth_vals, axis=0)
        
        # Apply the specific weight for this incident angle
        angle_contribution_abs = pdf[angle_index] * P_abs_ang
        angle_contribution_esc = pdf[angle_index] * P_esc_ang
        angle_contribution_L = pdf[angle_index] * L_max
        
        return angle_index, angle_contribution_abs, angle_contribution_esc, angle_contribution_L
    
    print(f"Processing {N_incident} incident angles using {num_threads} threads…")

    # Initialize arrays with the right shape to store results in correct order
    angle_contributions_abs = [None] * len(theta_inc)
    angle_contributions_esc = [None] * len(theta_inc)
    angle_contributions_L = [None] * len(theta_inc)
    bar_length = 69
    completed = 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_incident_angle, i) for i in range(len(theta_inc))]

        for future in as_completed(futures):
            try:
                idx, abs_contrib, esc_contrib, L_contrib = future.result()
                # Store results at the correct index position
                angle_contributions_abs[idx] = abs_contrib
                angle_contributions_esc[idx] = esc_contrib
                angle_contributions_L[idx] = L_contrib
            except Exception as exc:
                print(f"\nAngle task exception: {exc}")

            # update progress in main thread only
            completed += 1
            pct = completed / len(theta_inc)
            filled = int(bar_length * pct)
            bar = '█' * filled + '-' * (bar_length - filled)
            print(f"\rProgress: [{bar}] {pct*100:5.1f}% ({completed}/{len(theta_inc)})", end='', flush=True)
    
    print("\nCalculation completed!")
    
    # Stack the contributions into 2D arrays - now guaranteed to be in correct order
    abs_array = np.stack(angle_contributions_abs, axis = 0)
    esc_array = np.stack(angle_contributions_esc, axis = 0)
    L_array = np.array(angle_contributions_L)
    
    final_prob_abs = np.trapz(abs_array, x = theta_inc, axis = 0)
    final_prob_esc = np.trapz(esc_array, x = theta_inc, axis = 0)
    avg_L = np.trapz(L_array, x = theta_inc)
    
    probability_abs = interp1d(T_vals, final_prob_abs, kind='cubic', bounds_error=False, fill_value=0.0)
    probability_esc = interp1d(T_vals, final_prob_esc, kind='cubic', bounds_error=False, fill_value=0.0)
    
    return probability_abs(T_grid), probability_esc(T_grid), avg_L

