#%%
import numpy as np
import matplotlib.pyplot as plt
import wlinreg

measurements = 15

density_Al = 2.699 #g/cm^3
density_Pb = 11.348 #g/cm^3

I0 = 104586/90
I_bg = 1581/600
I0T = I0 - I_bg


Thickness_Al = np.array([5.44, 5.51, 5.03, 4.98, 4.52, 9.60, 14.99, 20.45, 25.48, 20.50, 15.06, 9.55, 10.03, 15.47, 46.0]) #mm
Thickness_Al_error = np.array([0.005, 0.005, 0.005, 0.005, 0.005, 0.007, 0.009, 0.01, 0.011, 0.01, 0.009, 0.007, 0.007, 0.009, 0.05]) #mm

density_thickness_Al = Thickness_Al/10 * density_Al #g/cm^2
density_thickness_Al_error = Thickness_Al_error/10 * density_Al #g/cm^2

Gross_counts_Al = np.array([95267, 95880, 96280, 97108, 97202, 91952, 82940, 75069, 68945, 74479, 83258, 90443, 89608, 81569, 48796])
I_Al = Gross_counts_Al/90 - I_bg

s_Al, b_Al, s_Al_std, b_Al_std = wlinreg.weighted_linear_regression(np.log(I0T/I_Al), density_thickness_Al, density_thickness_Al_error)

caption1 = r'Semilog plot of intensity relative to initial intensity of $\gamma$-rays produced by daughter product of $^{137}$Cs decay posittioned 5cm away from detector, separated by air versus the density thickness of aluminum in g/cm$^{2}$. The resultant slope is the calculated attenuation coefficient of aluminum for 0.662MeV $\gamma$-rays'

wlinreg.data_plot(density_thickness_Al, np.log(I0T/I_Al), density_thickness_Al_error, None, 1/s_Al, -b_Al / s_Al, s_Al_std / (s_Al ** 2), np.sqrt((b_Al_std / s_Al)**2 + (b_Al * s_Al_std / s_Al**2)**2), 'Cs137 Al Intensity Plot.svg', r'$x$ (g/cm$^{2}$)', r'$\ln(\frac{I}{I_0})$', caption1)

print(f'Slope (1/s_Al): {1/s_Al:.3f} ± {s_Al_std / (s_Al ** 2):.3f}', r'cm^2/g')
print(f'intercept (-b_Al / s_Al): {-b_Al / s_Al:.3f} ± {np.sqrt((b_Al_std / s_Al)**2 + (b_Al * s_Al_std / s_Al**2)**2):.3f}')
print(s_Al, b_Al, s_Al_std, b_Al_std)
print(f'HVL (ln(2)/mu): {s_Al * (np.log(2) + (b_Al / s_Al)):.3f} g/cm^2')
print(f'mu (ln(2)/(ln(2) * s_Al + b_Al)): {np.log(2)/(np.log(2)*s_Al + b_Al):.3f} ± {np.sqrt(((-np.log(2)**2 / (np.log(2) * s_Al + b_Al)**2) * s_Al_std)**2 + ((-np.log(2) / (np.log(2) * s_Al + b_Al)**2) * b_Al_std)**2):.3f} cm^2/g')

Thickness_Pb = np.array([0.85, 1.60, 0.83, 4.99, 6.25, 2.45, 3.28, 8.27, 14.52, 12.92, 12.09, 7.10, 11.24, 6.59, 7.85])
Thickness_Pb_error = np.array([0.005, 0.005, 0.005, 0.005, 0.005, 0.007, 0.009, 0.010, 0.011, 0.010, 0.009, 0.007, 0.007, 0.007, 0.007])

density_thickness_Pb = Thickness_Pb/10 * density_Pb #cm^2/g
density_thickness_Pb_error = Thickness_Pb_error/10 * density_Pb #cm^2/g

Gross_counts_Pb = np.array([88511, 84324, 83105, 64091, 51850, 76996, 70455, 45793, 23722, 28096, 30930, 47688, 33214, 52950, 43441])
I_Pb = Gross_counts_Pb/90 - I_bg

s_Pb, b_Pb, s_Pb_std, b_Pb_std = wlinreg.weighted_linear_regression(np.log(I0T/I_Pb), density_thickness_Pb, density_thickness_Pb_error)

caption2 = r'Semilog plot of intensity relative to initial intensity of by daughter product of $^{137}$Cs posittioned 5cm away from detector, separated by air versus the density thickness of lead in g/cm$^{2}$. The resultant slope is the calculated attenuation coefficient of lead for 0.662MeV $\gamma$-rays'

wlinreg.data_plot(density_thickness_Pb, np.log(I0T/I_Pb), density_thickness_Pb_error, None, 1/s_Pb, -b_Pb / s_Pb, s_Pb_std / (s_Pb ** 2), np.sqrt((b_Pb_std / s_Pb)**2 + (b_Pb * s_Pb_std / s_Pb**2)**2), 'Cs137 Pb Intensity Plot.svg', r'$x$ (g/cm$^{2}$)', r'$\ln(\frac{I}{I_0})$', caption2)

print(f'Slope (1/s_Pb): {1/s_Pb:.4f} ± {s_Pb_std / (s_Pb ** 2):.4f}', r'cm^2/g')
print(f'Intercept (-b_Pb / s_Pb): {-b_Pb / s_Pb:.4f} ± {np.sqrt((b_Pb_std / s_Pb)**2 + (b_Pb * s_Pb_std / s_Pb**2)**2):.4f}')
print(s_Pb, b_Pb, s_Pb_std, b_Pb_std)
print(f'HVL (ln(2)/mu): {s_Pb * (np.log(2) + (b_Pb / s_Pb)):.4f} g/cm^2')
print(f'mu (ln(2)/(ln(2) * s_Pb + b_Pb)): {np.log(2)/(np.log(2)*s_Pb + b_Pb):.4f} ± {np.sqrt(((-np.log(2)**2 / (np.log(2) * s_Pb + b_Pb)**2) * s_Pb_std)**2 + ((-np.log(2) / (np.log(2) * s_Pb + b_Pb)**2) * b_Pb_std)**2):.4f} cm^2/g')
#%%
