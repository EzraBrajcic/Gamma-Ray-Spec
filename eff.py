# GATE-simulated efficiencies at 10 cm (fraction)
eps_gate_10cm = np.array([
    1.071,  # 59.54 keV
    1.341,  # 121.8 keV
    0.758,  # 344.3 keV
    0.338,  # 661.6 keV
    0.192,  # 1173.2 keV
    0.154,  # 1274.5 keV
    0.154,  # 1332.5 keV
    0.148   # 1408.0 keV
])

# Experimental efficiencies at 10 cm (fraction), missing values as NaN
eps_exp_10cm = np.array([
    1.012,  # 59.54 keV
    0.328,  # 661.6 keV
    0.181,  # 1173.2 keV
    0.142,  # 1274.5 keV
    0.142,  # 1332.5 keV
])

# --- 2) Tabulated efficiency points at 10 cm (GATE-simulated) ---
energies_keV = np.array([59.54, 121.8, 344.3, 511.0, 661.6, 1173.2, 1274.5, 1332.5, 1408.0])
eps_gate = np.array([1.071, 1.341, 0.758, np.nan, 0.338, 0.192, 0.154, 0.154, 0.148]) / 100
mask = ~np.isnan(eps_gate)
energies_MeV_pts = energies_keV[mask] / 1000.0
eps_gate_pts     = eps_gate[mask]
energies_MeV_all = data[:, 1]

# --- 4) Initial parameter guess and bounds ---
p0 = [9.0, 0.75, -2.4, 10.0, 8.0, -1.0, 5.0]
lb = [0,    -5,   -5,    1,   0,   -5,   0]
ub = [20,    5,    0,   50,  20,    5,  20]

# --- 5) Fit to the measured points ---
popt_eff, pcov = curve_fit(
    eff_func,
    energies_MeV_pts,
    eps_gate_pts,
    p0=p0,
    bounds=(lb, ub),
    maxfev=20000
)

# --- 6) Compute fit over full MeV axis and plot on a linear scale ---
eff_fit_all = eff_func(energies_MeV_all, *popt_eff)

plt.figure(figsize=(8, 5))
plt.plot(energies_MeV_all, eff_fit_all, '-', lw=2, label='Fitted Efficiency')
plt.scatter(energies_MeV_pts, eps_gate_pts, color='red', zorder=5, label='Sim Points @10 cm')
plt.xlabel('Photon Energy (MeV)')
plt.ylabel('Full‐Energy Peak Efficiency (fraction)')
plt.title('NaI(Tl) Efficiency vs Energy on Linear MeV Scale')
plt.legend()
plt.grid(True, ls='--', lw=0.5)
plt.tight_layout()
plt.show()

# Print out the final fit parameters
print("Fitted parameters:")
for name, val in zip(["t0","t1","t2","t3","t4","t5","t6"], popt_eff):
    print(f"{name} = {val:.4f}")