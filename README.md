\documentclass[12pt,jou, a4paper]{apa7}

% Load inputenc before biblatex
\usepackage[utf8]{inputenc}

% Load biblatex with the desired options
\usepackage[style=numeric, backend=biber]{biblatex}

% Essential packages
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{physics}  % For physics notation
\usepackage{braket}   % For quantum notation
\usepackage{indentfirst}
\usepackage{microtype}
\usepackage{subcaption}
\usepackage[font=footnotesize,skip=0pt]{caption}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{sectsty}
\usepackage{newtxtext}
\usepackage[varg]{newtxmath}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}
\usepackage{setspace}

% Add your bibliography file here
\addbibresource{ref.bib}

\captionsetup[subfigure]{justification=centering}
\captionsetup[figure]{format=plain, labelformat=simple, labelsep=colon}
\setlength{\headheight}{14.49998pt}
\addtolength{\topmargin}{-1.05429pt}

% Define royal blue color for headings
\definecolor{midnightblue}{HTML}{045275}
\sectionfont{\large\color{midnightblue}}
% Vector notation
\newcommand{\harpoon}[1]{\overset{\rightharpoonup}{#1}}

% Custom commands
\newcommand{\inst}[1]{$^{#1}$}
\newcommand{\email}[1]{\texttt{#1}}
\setlength{\emergencystretch}{1pt}
\geometry{margin=1in}
\numberwithin{equation}{section}
\setcounter{secnumdepth}{3}

% Redefine the \supercite command to make citations superscripts and smaller
\renewcommand{\supercite}[1]{\textsuperscript{\footnotesize\cite{#1}}}

% Define a short title for headers
\shorttitle{Gamma-Ray Detector Spectra via Ray-Tracing}

% Setup headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\scriptsize Gamma-Ray Detector Spectra via Ray-Tracing}
\fancyhead[R]{\thepage}

% Title and author configuration similar to original
\title{\textcolor{midnightblue}{Ray-Tracing of Gamma-Rays in Analysis of Detector Response Spectra}}

\author{E Eddy Brajcic\textsuperscript{1}, J. Parker\textsuperscript{2}, S. Kupnicki Ruiz-Huidobro\textsuperscript{3} }

\authorsaffiliations{
    {Department of Physics, University of Guelph\\Guelph, Ontario, N1G 2W1, Canada\\\vspace*{5pt}\small(Dated: \today)}
}

\authornote{
  \begin{flushleft}
    ${^1}$Email: ebrajcic@uoguelph.ca\\
    ${^2}$Email: jparke10@uoguelph.ca\\
    ${^3}$Email: skupnick@uoguelph.ca\\
  \end{flushleft}
}
\begin{document}
\subsectionfont{\large\color{midnightblue}}
\frenchspacing
\maketitle
\thispagestyle{fancy} % Apply fancy page style to first page}
\clearpage
\begin{doublespace}
\twocolumn[ 
\begin{@twocolumnfalse}
    \begin{center}        
        \space \textbf{Abstract}\\
    \end{center}
    \noindent This paper presents a novel angular-sampling ray-tracing framework for modeling gamma-ray detector response spectra that bridges the gap between simplified analytical approximations and comprehensive Monte Carlo simulations. We systematically discretize the incident gamma-ray flux over uniform angular grids and implement exact ray-cylinder intersection calculations to accurately model detector geometry effects on spectral features. Our method applies the full Klein-Nishina differential cross section with energy-dependent incoherent-scattering corrections, computing depth-weighted absorption and escape probabilities through a NaI(Tl) scintillation detector. By integrating over angular permutations and applying an energy-dependent Gaussian convolution kernel, we reproduce both the continuum shape and edge features of measured spectra without relying on stochastic sampling. When validated against experimental measurements using a 1.5"$\times$1.5" cylindrical NaI(Tl) detector and a $^{137}$Cs source, our model accurately predicted the Compton edge at 0.480 MeV (within 0.002 MeV of theoretical values) and closely matched the continuum profile. Minor discrepancies in backscatter regions and near the Compton edge highlight the contributions of multiple scattering events not yet incorporated in our single-scatter model. This deterministic approach offers significant advantages in computational efficiency, reproducibility, and interpretability for radiation metrology, medical diagnostics, and innovations in imaging technology.
\end{@twocolumnfalse} 
]
\end{doublespace}
\clearpage
\section{\textcolor{midnightblue}{Introduction}}
\vspace*{-9pt}
Accurate modeling of gamma-ray ($\gamma$-ray) detector responses is essential for quantitative spectroscopy, radiation safety, and nuclear safeguards. In particular, sodium iodide (NaI(Tl)) scintillation detectors remain the workhorse of low-energy gamma spectroscopy due to their high intrinsic efficiency and ease of deployment. When characterizing spectra from a $\gamma$-ray source, however, a rich interplay of $\gamma$-ray transport and detector geometry effects must be captured in order to predict both the continuum and the photopeak response with high fidelity. Traditional approaches—including both closed-form analytic formulas and comprehensive Monte Carlo transport—have their own limitations when modeling detector response. Analytical methods often treat scattering, attenuation, and energy resolution as separate sequential processes, neglecting correlations between scattering angle, energy loss, and escape probability within the detector volume\supercite{res}. Meanwhile, Monte Carlo methods can model such correlations naturally, but typically require extensive particle histories and stochastic sampling, complicating reproducibility and interpretation when subtle geometry or energy-dependent scattering effects dominate\supercite{MC}.\\

In this work we present an angular-sampling ray-tracing framework that bridges these gaps. Our method systematically discretizes the incident gamma-ray flux over a uniform grid of angles and, for each direction, casts rays through a 1.5"$\times$1.5" cylindrical scintillator via exact ray–cylinder intersection via geometric boundary conditions. At each depth step, the model applies the full Klein–Nishina differential cross section—including energy-dependent incoherent-scattering corrections, sampling $n\times m$ combinations of Compton scattering angles $\theta_{cs}$ and uniform azimuthal angles $\varphi_{cs}$ to compute depth-weighted absorption and escape probabilities. This angular sweep yields a set of energy-dependent probabilities that are subsequently convolved with the Klein–Nishina equation under a Gaussian kernel\supercite{conv}. Reproducing both the continuum shape and the edge features without recourse to stochastic sampling.\\

The relationship between Compton scattering angle and photon energy is fundamental to the detector response. For an incident photon of energy $E_{\gamma}$, the energy of a photon scattered by the polar angle relative to the incident photon $E_{\gamma'}$ is given by\supercite{Geist2024}
\begin{equation}
  E_{\gamma'}\left(\theta\right)=\frac{E_\gamma}{1+\alpha\left(1-\cos\left(\theta\right)\right)}
  \label{eq:compton_energy}
\end{equation}
where $\alpha$ is the ratio between the incident $\gamma$-ray' energy and the rest energy of the electron $\left(E_\gamma/m_{e}c^2\right)$. The solid angle distribution of scattered unpolarized photons is governed by the klein-Nishina differential cross section\supercite{MC},
\begin{equation}
  \frac{d\sigma_c}{d\Omega} = \frac{r^2_e}{2}\left(\frac{E_{\gamma'}}{E_\gamma}\right)^{2}\left(\frac{E_{\gamma'}}{E_\gamma}+\frac{E_{\gamma}}{E_\gamma'}-\sin^2\theta\right)\label{eq:KN},
\end{equation}
where $r_e$ is the classical electron radius. The Klein-Nishina equation is further modified by the incoherent scattering function $S\left(x\right)$\supercite{Sx}, taking electron binding effects from the detector material into account becoming
\begin{equation}
  \frac{d\sigma_c}{d\Omega} S\left(x\right),
\end{equation}
where
\begin{equation}
  x=\sin\left(\theta/2\right)\frac{E_\gamma}{hc}.
\end{equation}
By solving for the scattered $\gamma$-ray polar angle in the Compton scattering equation~\eqref{eq:compton_energy}, we now have a function of $\theta\left(E_{\gamma'}\right)$ as
\begin{equation}
  \theta\left(E_{\gamma'}\right) = \cos^{-1}\left(1-\frac{E_{\gamma}-E_{\gamma'}}{\alpha E_{\gamma'}}\right)\label{eq:cse}.
\end{equation}
Using the chain rule, the Klein-Nishina equation~\eqref{eq:KN} can then be transformed into a differential energy cross section to produce a cross sectional energy spectra as by integrating over the azimuthal angle of the differential solid angle $d\Omega=\sin\left(\theta\right)d\theta d\varphi$
\begin{equation}
  \frac{d\sigma_c}{dE_{\gamma'}}=\frac{d\sigma_c}{d\Omega}\frac{d\theta}{dE_{\gamma'}}\frac{d\Omega}{d\theta},
\end{equation}
where
\begin{equation}
  \frac{d\Omega}{d\theta}=2\pi\sin\theta.
\end{equation}
The full Klein-Nishina equation can then be represented in terms of scattering angle or energy from equation~\eqref{eq:cse}\supercite{MC}
\begin{equation}
\frac{d\sigma_c}{dE_{\gamma'}}=\frac{d\sigma_c}{d\Omega}\left(\theta\right)\frac{2\pi\,[1+\alpha(1-\cos\theta)]^2}{E_\gamma\,\alpha}\,S\bigl(x(\theta)\bigr)\label{eq:dsdt}.
\end{equation}
In a detector though, the energy observed in the response spectra is actually the energy that's deposited into an electron by an incident $\gamma$-ray. Therefore, a substitution of $T=E_{\gamma}-E_{\gamma'}$ replacing $E_{\gamma'}$ can be made to reflect this. The finite detector resolution can then incorporated via a Gaussian convolution kernel of the form
\begin{equation}
  g\left(E\right)=\frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{\left(E-\mu\right)^2}{2\sigma^{2}}}\label{eq:gck},
\end{equation}
where $\mu$ is the energy level of the centroid of a characteristic photopeak and $\sigma$ is the standard deviation of the same photopeak determined by the full width half-maximum (FWHM) of a it, which has the relationship\supercite{gamma}
\begin{equation}
  FWHM=2\sqrt{2\ln(2)}\sigma.
\end{equation}
By applying the formulas for a detector's resolution, it's then possible to create an energy dependent $\sigma$ function that operates across the entire detector response spectrum, the resolution formula takes the form of\supercite{gamma}\supercite{res}
\begin{equation}
  R\left(E\right)=\frac{FWHM}{E}\approx\frac{k}{\sqrt{E}}\label{eq:res}.
\end{equation}
Here, $k$ takes the form of a proportionality constant characteristic of the particular detector used. The energy dependent $\sigma$ function is then determined by
\begin{equation}
  \sigma\left(E\right)\approx\frac{k\sqrt{E}}{2\sqrt{2\ln(2)}}\label{eq:sigma}.
\end{equation}\\\\
The detector energy resolution kernel can then be applied to the differential energy cross section from the Klein–Nishina equation~\eqref{eq:KN}.
\begin{equation}
  R\left(T\right)=\int\frac{d\sigma_c}{dT}g\left(T\right)dT\label{eq:KNc}
\end{equation}
Absorption and escape probabilities for the detector are computed via ray-tracing with angular-sampling of the incident angle $\theta_{inc}$ and scattering angle $\theta_{sc}$ relative to the incident $\gamma$-ray, exact ray–cylinder intersections utilizing detector boundary conditions for every permutation of ($\theta_{inc}$,$\theta_{sc}$), and depth-weighted attenuation through the detector can then be performed. Integrating over both all angular permutations yields both escape and absorption probabilities for the incident, characteristic, $0.662$MeV $\gamma$-rays, which—when applied to the primary Compton spectrum and convolution kernel—reproduce measured continuum and edge features with high mathematical rigor\supercite{conv}.
\section{\textcolor{midnightblue}{Methodology}} 
\subsection{\textcolor{midnightblue}{Reference Response Spectrum}}
Before creating a detector response spectrum, a 3-point energy calibration function was made using $6.842~\mu$Ci $^{137}$Cs and $0.850~\mu$Ci $^{60}$Co sealed sources in the form of a powder using a 7S8 Integral Spin Harshaw Na(Tl) scintillation detector with a 1.5"$\times$1.5" cylindrical crystal to convert from channel number to energy in MeV. The sources were placed 9.3cm away from the detector about its centre and a spectrum was recorded over a period of 917 seconds accounting for dead-time. The detector was equipped with a photomultiplier tube, a TC155A preamplifier, and a Spectech UCS 30 universal computer spectrometer which was connected to a computer with Spectrum Techniques 2010 USX MCA software version 1.2.00B. In the software, the minimum channel number was set to 16, a maximum channel number of 1023, a HV of 900V, coarse gain was set at 4, fine gain to 1.75$\times$, and used the PHA ampin mode. Calibration was made on the characteristic 0.662MeV $^{137}$Cs, 1.173MeV $^{60}$Co, and 1.332MeV $^{60}$Co characteristic $\gamma$-ray emission photopeaks. After energy calibration, background measurements were made without any sources for 600 seconds. A detector response spectrum was then recorded with the $6.842~\mu$Ci $^{137}$Cs source for 610 seconds accounting for detector dead-time. Using the FWHM of the photopeak, a Gaussian fit can then be made of it to obtain an estimated amount of counts under the photopeak after background subtraction\supercite{gamma}. Subtraction of the lingering Compton continuum within the photopeak is unnecessary since applying a convolution kernel~\eqref{eq:gck} up until the intersecting area of the convolved spectrum and Gaussian fit of the photopeak becomes significant and then applying simple linear interpolation fully accounts for the observed count data\supercite{gamma}. The convolved response function falls off to 0 estimated counts before the FWHM of the photopeak is reached. Therefore, the channel count data used to create the Gaussian fit for the photopeak remains unaffected.
\begin{figure}[H]
  \centering
  \includegraphics[width=0.46\textwidth]{Cs137Spectrum.png}
  \caption{\scriptsize Convolution of detector response spectrum in addition with Gaussian fit of characteristic 0.662MeV photopeak. The interpolation of the intersecting area of the convolved count data and Gaussian fit accounts for the greater number of observed counts near the tail of the Gaussian. The interpolation of count the data also reaches zero before the FWHM energy of the photopeak.}
\end{figure}
It is important to note that the peak of the convolved Compton continuum does not represent the real Compton edge since the energy resolution~\eqref{eq:res} smears it by a factor directly proportional to the detector's resolution at that energy level. The true Compton edge is still able to be determined by finding the point of greatest descent of the count data or the convolved detector response spectrum within the Compton continuum\supercite{gamma}\supercite{cco}.
\subsection{\textcolor{midnightblue}{Detector Response Modeling}}
Proper modeling of the Compton continuum that reflects the observed spectrum requires that source and detector geometry, source $\gamma$-ray emission characteristics, detector material properties, and detector resolution must be taken into account\supercite{gamma}. Detector resolution, as discussed before is modeled via an energy dependent Gaussian convolution kernel~\eqref{eq:gck}\eqref{eq:sigma}. Combining this with the Klein–Nishina equation and the incoherent scattering function~\eqref{eq:dsdt} results in a detector and source geometry independent relationship for the deposited energy by an electron~\eqref{eq:KNc} that forms part of the metaphorical equation on detector material characteristics\supercite{MC}\supercite{conv}. The incoherent scattering function is normally defined per atom, so to convert to the per electron form used in cross section calculations, the average of the incoherent scattering functions for sodium and iodine weighted by the number of electrons each atom has is used\supercite{Sx}. 
\begin{figure}[H]
  \centering
  \begin{subfigure}{0.45\textwidth}
    \includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{KN.png}
  \end{subfigure}\\

  \begin{subfigure}{0.46\textwidth}
    \includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{KNR.png}
    \end{subfigure}

  \caption{\scriptsize Convolved and unconvolved Klein–Nishina equation with and without the inclusion of the incoherent scattering function $S\left(x\right)$ (a). The ratio of the Klein–Nishina equation with the the incoherent scattering function and the Klein–Nishina equation (add 1 to all y-axis ticks) (b).}
\end{figure}
While thallium is present in the detector crystal and has a higher cross section for interaction than both sodium and iodine, it's present in such low quantities that it doesn't affect the the attenuation in bulk. It's primary purpose is to improve the linearity of the scintillation light output with increasing deposited energy by creating electron holes within the crystal lattice\supercite{np}\supercite{res}\supercite{gamma}. The second part is the aluminum plating of the detector for which simple attenuation of the $\gamma$-rays is used from the Beer-Lambert equation
\begin{equation}
  I=I_{0}e^{-\mu x}\label{eq:bl}
\end{equation}
where $\mu$ is the total linear attenuation coefficient for the material of concern and $x$ is the thickness of the material. 
\begin{figure}[H]
  \centering
  \includegraphics[width=0.47\textwidth]{nai_mass_attenuation_full_range_monotonic.png}
  \caption{\scriptsize Mass attenuation coefficient of photons for different interaction types ranging from photon energies of 1.0KeV to 2.0MeV for NaI. Attenuation data was sourced from\supercite{HUBBELL}.}
\end{figure}
The detector used in this study has a aluminum plating thickness of $\sim$0.5mm on the front of the detector, meaning that the incident 0.662MeV $\gamma$-rays intensity from the $^{137}$Cs source is reduced by $\sim3.35\%$. $^{137}$Cs has a branching decay ratio of 0.851 for 0.662MeV $\gamma$-ray emissions, therefore, the total fluence rate of the characteristic $\gamma$-rays from the source is 215434054 $\gamma$-rays per second. The solid angle intersection of a sphere, representing the flux of $\gamma$-rays at a distance $d$ from the detector, and a cylindrical detector of radius $r$, facing the sphere follows the equation
\begin{equation}
  A=\frac{1}{2}\frac{1-d}{\sqrt{r^{2}+d^{2}}}\label{eq:sai}.
\end{equation}
The attenuation of $\gamma$-rays through air as they travel from the source to the detector can again be approximated using the Beer-Lambert equation~\eqref{eq:bl}.\\

To fully account for detector geometry, first, the incident $\gamma$-rays do not all take the same straight line path towards the detector. Since the source activity is extremely high compared to background radiation and the detector has symmetry across every axis orthogonal to an uniform distribution of incident angles going towards the cylindrical detector can be used and follows the normalized form off
\begin{equation}
  P\left(\theta_{inc}\right)=\frac{\sin\left(\theta_{inc}\right)}{1-\cos\left(\theta_{max}\right)},
\end{equation}
where $\theta_{max}=\tan^{-1}\left(r/d\right)$. The probability of an incident $\gamma$-ray interacting via Compton scattering as a function of electron energy $P_{cs}\left(T\right)$ is the integral of the Beer-Lambert equation~\eqref{eq:bl} with the linear attenuation coefficient for Compton scattering\supercite{gamma}supercite{Geist2024}\supercite{HUBBELL} which is defined as
\begin{equation}
  P_{cs}\left(T\right)=\frac{\frac{d\sigma_{c}}{dT}}{\sigma_{c}}\left[1-e^{-\mu_{c}\ell}\right],
\end{equation}
\begin{equation}
  \mu_{c}=\rho_{e}\sigma_{c}=\rho_{e}\int_{\Omega}\frac{d\sigma_{c}}{d\Omega}d\Omega
\end{equation}
\begin{spacing}{1.0}
Where $\sigma_{c}$ is the total cross section for Compton scattering for a photon of energy $E$, $\rho_{e}$ is the electron density of the material, and $\ell$ is the average path length that each incident $\gamma$-ray of all possible incident angles $\theta_{inc}$ intersecting through the detector. Each path about $\theta_{inc}$ inside the detector can then be sliced into multiple portions where multiple Compton scattering angles $\theta_{cs}$, going from 0 to $\pi$, are weighted by the Klein–Nishina equation~\eqref{eq:KN}. The azimuthal Compton scattering angle $\varphi_{cs}$ is sampled across an uniform distribution from 0 to $2\pi$ as the $\gamma$-rays emitted by $^{137}$Cs are unpolarized\supercite{gamma}. Rays are drawn with the scattering angles through the detector until it hits the detector's boundary. The length of the line $L\left(z,\theta_{cs},\varphi_{cs}\right)$ determines the probability of escape from the detector using the Beer-Lambert equation~\eqref{eq:bl} with the total linear attenuation coefficient of the energy of the scattered $\gamma$-ray $\mu_{tot}\left(E_{\gamma'}\right)$.
\end{spacing}
\scriptsize\begin{equation}
  P_{esc}\left(\theta_{inc}\right)=\frac{1}{2\pi}\sum_{i=0}^{n}\sum_{j=0}^{m}\sum_{k=0}^{q}e^{-\mu_{tot}\left(E_{\gamma'}\right)L\left(z_{i}, \theta_{cs_{j}}, \varphi_{cs_{k}}\right)}.
\end{equation}\normalsize
The probability of absorption, assuming that secondary Compton scattering events stay within the detector afterward is very similar
\scriptsize\begin{equation}
  P_{abs}\left(\theta_{inc}\right)=\frac{1}{2\pi}\sum_{i=0}^{n}\sum_{j=0}^{m}\sum_{k=0}^{q}\left[1-e^{-\mu_{tot}\left(E_{\gamma'}\right)L\left(z_{i}, \theta_{cs_{j}}, \varphi_{cs_{k}}\right)}\right].
\end{equation}\normalsize
\begin{spacing}{1.0}
The combined probability for escape or absorption after undergoing Compton scattering across all incident angles is then
\scriptsize\begin{equation}
  P_{esct}\left(T\right)=P_{cs}\left(T\right)\int_{0}^{\theta_{max}}P\left(\theta_{inc}\right)P_{esc}\left(\theta_{inc}\right)d\theta_{inc}\label{eq:esc},
\end{equation}
\begin{equation}
  P_{abst}\left(T\right)=P_{cs}\left(T\right)\int_{0}^{\theta_{max}}P\left(\theta_{inc}\right)P_{abs}\left(\theta_{inc}\right)d\theta_{inc}\label{eq:pabst}.
\end{equation}\normalsize
The escape probability~\eqref{eq:esc} can then be convolved with a Gaussian kernel~\eqref{eq:gck}\supercite{conv} and multiplied by the number of incident photons from the source that intersect the detector accounting for geometric factors~\eqref{eq:sai} over the same detection live-time used to gather the reference response spectrum of 600 seconds. Finally obtaining a computed spectrum of the Compton continuum for single Compton scatter events of the form
\end{spacing}
\tiny\begin{equation}
  R\left(T\right)=\frac{A_{0}f\tau}{2}\frac{1-d}{\sqrt{r^{2}+d^{2}}}e^{-\mu_{Al}\rho_{Al}x_{Al}-\mu_{Air}\rho_{Air}x_{Air}}\int P_{esct}\left(T\right)g\left(T\right)dT\label{eq:resf}.
\end{equation}\normalsize
Where $A_{0}$ is the activity of the $^{137}$Cs source, $f$ is the decay fraction of the source that results in a 0.662MeV $\gamma$-ray, and $\tau$ represents the total detection time. This expression was then coded in Python with support for multithreading to ray-trace multiple $\gamma$-rays at the same time and executed on a computer using an AMD Ryzen 5800X3D with 32Gb of memory. 300 discretized incident $\theta_{inc}$ angles, 500 polar Compton scattering $\theta_{cs}$ angles, 200 azimuthal Compton scattering $\varphi_{cs}$ angles, and 150 slices across the path length $L$ of the rays intersecting the bounds of the detector was used in the model.\\
\section{\textcolor{midnightblue}{Results}}
After applying the relevant parameters that correspond to the physical detector used to gather the reference response spectrum~\eqref{eq:resf} produced a function matching closely to the observed Compton continuum even when only accounting for single scatter $\gamma$-ray escapes. The model produced a Compton edge of 0.480MeV, just 0.002MeV off of the theoretical value of 0.478MeV.
\begin{figure}[H]
  \centering
  \includegraphics[width=0.47\textwidth]{CC.png}
  \caption{\scriptsize Convolution of Klein–Nishina equation accounting for detector geometry and attenuation characteristics for incident 0.662MeV $\gamma$-rays compared to observed count data.}
\end{figure}
The model most closely reflects the observed count data about the Compton edge and 0.01 to 0.035MeV range. The discrepancy between the estimated Compton edges between figure 1 and 4 appears to be a result of both backscatter and multiple Compton scattering events that the detector picks up which skews the Compton edge to a lower energy of 0.462MeV\supercite{gamma}. After the first Compton scattering event, at greater scattering angles, the energy of the scattered $\gamma$-ray is significantly reduced, increasing the likelihood of photoelectric absorption, which dominates at $\gamma$-ray energies lower than $\sim$0.26MeV in NaI as seen in figure 3\supercite{HUBBELL}. This energy range also shows an increase of counts as the energy deposited into an electron decreases and creates asymmetry in the backscatter peak. Unfortunately, as the FWHM of the backscatter peak is largely affected by the asymmetry, it does not appear that a Gaussian fit of it could be made with ease. The model also leaves many counts around the tail of the Compton edge unaccounted for, we hypothesize these to be a product of 2 absorptions occurring within a similar time interval of the detector's resolving time. One being a high energy Compton scattering event, and the other likely being the photoelectric absorption of a scattered photon with a much lower energy, combining 2 counts into a single energy channel higher in energy than either of the individual interactions.
\begin{figure}[H]
  \centering
  \includegraphics[width=0.47\textwidth]{CCD.png}
  \caption{\scriptsize Plot of convolved observed count data subtracted by the expected Compton spectrum, multiple Compton scatter events appear to produce a secondary spectrum with a shifted edge. The large backscatter peak remains as Compton scattering events outside of the detector geometry that deflect $\gamma$-rays towards the detector were not accounted for.}
\end{figure}
From the reference response spectrum, it's possible to find the total number of counts under the photopeak utilizing the Gaussian fit of it, and by integrating over the Gaussian function, the total number of observed counts was 273969$\pm$7288. A spectrum of absorbed counts was made by applying equation~\eqref{eq:pabst} to the terms in~\eqref{eq:resf} without including the Gaussian convolution kernel as each count present is assumed to have deposited all of their energy within the energy resolution of the photopeak. Integrating over it resulted in an estimated 428873 counts, off by the Gaussian fit of the photopeak by 154904$\pm$7288 counts. This is largely due to the fact that a large portion of the $\gamma$-rays still have a greater cross section for Compton scattering than any other form of interaction after the first Compton scattering event and are likely to still escape after a second Compton scattering interaction\supercite{gamma}\supercite{Geist2024}. While not entirely conclusive due to the backscatter peak, subtraction of the total Compton scattering counts determined by the model from the total observed counts in the reference spectrum leaves a remainder of 269322 counts, leaving plenty of room for extra potential $\gamma$-rays to escape after multiple Compton scattering interactions.This can be proven by observing the escape and absorption probabilities as the trajectories of the scattered $\gamma$-rays change with regard to $\theta_{inc}, \theta_{cs}$, and $\varphi_{cs}$. We observed that the Compton scattering escape and absorption probabilities are at their maximum at high scattered $\gamma$-ray energies that correspond to low Compton scattering angles $\theta_{cs}$ and that absorption via other processes, such as photoelectric absorption, only dominate at $\gamma$-ray energies greater than or equal to 0.292MeV.
\begin{figure}[H]
  \centering
  \includegraphics[width=0.47\textwidth]{ACS.png}
  \caption{\scriptsize Compton absorption spectrum after first Compton scatter interaction. While energies not equal to the characteristic 0.662MeV $\gamma$-ray emission from $^{137}$Cs are present, the time difference between the first scatter interaction and subsequent absorption are so small that they would appear as a single count under the photopeak with an energy of 0.662MeV.}
\end{figure}

\begin{figure}[H]
  \centering
  \includegraphics[width=0.47\textwidth]{interaction_probabilities_kn.png}
  \caption{\scriptsize Escape and absorption probabilities after undergoing a single Compton scatter event as a function of deposited electron energy $T=E_{\gamma}-E_{\gamma'}$. Curves represent absorption and escape probabilities for the sum of all forms of interaction, via Compton scattering, and via all processes minus Compton scattering.}
\end{figure}\newpage
\section{\textcolor{midnightblue}{Future Improvements and Works}}
\subsectionfont{\small\color{midnightblue}}
\subsection{\small\textcolor{midnightblue}{Sources of Error and Mitigation}}
There are a plethora of potential improvements that could be made to both the experimental apparatus as well as the simulation. Starting with the apparatus, the low energy resolution of Na(Tl) detectors compared to others such as HGPE detectors increases count uncertainty by a significant margin and clouds the presence of multiple distinct peak regions, making them almost impossible to discern separately when their FWHM points overlap\supercite{gamma}\supercite{res}. While NaI(Tl) detectors are known for their linear scintillation light output, especially when doped with thallium, they do have a slightly non-proportional response depending on the energy of the interacting photon\supercite{np}.\\ 

A related issue is the presence of coincident X-ray emissions in $^{137}$Cs decay. When $^{137}$Cs undergoes internal conversion, the de-excitation energy can eject a K-shell electron and subsequently emit a Ba K$\alpha$ X-ray (~32 keV). In our NaI(Tl) spectrum, these X-rays appear as a low-energy peak and add counts within the characteristic photopeak, effectively “summing” with the 0.662MeV $\gamma$-rays in the detector. The coincidence of the 32 keV X-ray with the characteristic $\gamma$-ray causes distortion of the photopeak shape, introducing fitting bias\supercite{cco}. Addressing this will require explicitly fitting or subtracting the X-ray peak when analyzing the spectrum, possibly done by fitting a Gaussian to where the coincidence peak would theoretically be and subtracting it from the entire photopeak. The second Gaussian would only need to be another term added to the original model.\\

Another practical error source is energy calibration drift. Scintillator–photomultiplier systems are sensitive to temperature and bias fluctuations, which shift gain and thus the energy–channel relationship. For instance, we observed the $^{137}$Cs photopeak drift from about 0.662 MeV to 0.668 MeV over time. Without real-time correction, this causes systematic peak-position errors\supercite{gamma}. Future work should incorporate continuous calibration checks or temperature stabilization to hold the energy scale fixed.\\

The assumed source geometry is another simplification. We treated the $^{137}$Cs source as a point, but real check sources have finite size and encapsulation. Meaning that $\gamma$-rays are emitted from a distribution of locations, altering the angular distribution at the detector and introduces self-attenuation within the source material\supercite{source}. If the source is sizable (or has a non-negligible thickness of plastic/acrylic housing), the effective solid angle and unscattered intensity differ from the ideal point-source model. A full simulation should include the actual source geometry and encapsulation to account for absorption and buildup. For example, plastic and acrylic housings attenuate low-energy photons and can produce secondary scatter before the $\gamma$-ray even escapes the source. These attenuation layers (the source envelope, any shielding, and even reflective or coupling layers on the detector such as MgO coatings) all affect efficiency and spectral shape\supercite{MgO}. NaI(Tl) crystals are lined with reflective material (e.g. MgO) to maximize light collection. While the MgO reflector boosts photon detection, any surrounding material can also absorb or scatter X-rays and $\gamma$-rays. Each layer thus modulates the detected spectrum, especially at low energies. Neglecting these interfaces can lead to error. Our model should therefore include all material layers (shielding, optical couplers, enclosure walls) along the photon path.\\

Finally, the statistical quality of the data is limited by short acquisition times. Our source counting and background runs were relatively short. $\gamma$-ray counting follows Poisson statistics, so the uncertainty scales as the square root of the counts. Short live-times result in larger statistical fluctuations ($\sqrt{N}$ noise) under the photopeaks and in the background subtraction\supercite{gamma}\supercite{Geist2024}. This adds scatter to the measured spectrum and can obscure fine details. In particular, a short background run yields poor background subtraction and may leave residual counts under the peaks. Increasing the live-time for both source and background measurements would reduce this uncertainty (improving the signal-to-noise as $N/\sqrt{N}$) and producing smoother spectra more comparable to deterministic simulations\supercite{gamma}.\\

Using a larger-volume NaI(Tl) crystal greatly improves the full-energy peak efficiency. A bigger crystal intercepts more $\gamma$-rays, increasing the photopeak count and thereby reducing relative statistical error\supercite{gamma}. This also raises the probability that an incident $\gamma$-ray undergoes full-energy absorption (via the photoelectric effect or multiple scatter within the crystal), making the spectrum contain more full-energy events. In practice, upgrading to a larger scintillator or adding multiple detectors would boost count rates and improve photopeak definition without increasing source activity.\\

Introducing a collimator on the source or detector restricts the angular distribution of incoming photons. This simplifies the geometry (effectively a narrow pencil beam) so that only nearly straight-line paths contribute. Collimation reduces the number of scattered (off-axis) rays and also limits background from backscattered photons\supercite{col}. By forcing a well-defined path, the model need not account for a wide range of angles, and the effective source–detector distance and solid angle become well-defined. Collimation thus can greatly simplify the ray-tracing model and reduce uncertainty from angular misalignment.\\

\subsectionfont{\small\color{midnightblue}}
\subsection{\small\textcolor{midnightblue}{Simulation Improvements}}
In the ray-tracing model we currently follow only single Compton interactions. In reality, a $\gamma$-ray can undergo multiple sequential scatters before escaping or depositing all its energy. Neglecting higher-order scatter leads to underestimation of the continuum and backscatter peaks. A more complete simulation would track photon histories through multiple scatter events. Our model shows that the major difference in total absorbed as well as escaped counts when compared to our reference spectrum signifies that multiple Compton scatter events play a major role\supercite{gamma}. Incorporating multiple Compton scattering events will allow a more accurate reproduction of the Compton continuum and backscatter features.\\

Our current ray-tracing used relatively coarse angle and path sampling due to computer hardware memory limitations. This can introduce ray aliasing errors, especially near boundary regions. Improving the simulation grid with smaller angular steps of $\theta_{inc}, \theta_{cs}$, and $\varphi_{cs}$ will reduce these discretization artifacts. In practice, one would sample the source emission over more incident angles and follow rays more densely across the detector surface. Although this increases computational load, it yields smoother, more accurate spectra.\\

The simulation should include the laboratory environment. Photons that scatter off walls, floors, and nearby equipment can re-enter the detector, adding a background contribution. Any metallic or dense objects near the source can produce characteristic X-rays or backscatter peaks, this includes the metal stand that the $^{137}$Cs sample was placed on. To capture this, the geometry model must place walls and major structures in the simulation and allow photons to scatter or be reflected from them\supercite{gamma}\supercite{Geist2024}\supercite{res}. Including these environmental scatter paths is hypothesized improve the low-energy background match and account for any anomalous peaks such as the 0.184MeV backscatter peak observed.\\

To handle the increased computational demand of multi-scatter and finer discretization, one can leverage graphics processing units (GPUs). GPUs are well-suited to parallel ray-tracing and photon transport. Libraries such as NVIDIA CUDA enable thousands of photons to be traced concurrently. Furthermore, modern GPUs with dedicated ray-tracing (RT) cores; originally meant to produce high fidelity lighting environments in video games, can accelerate the tracing of photon paths similarly to how they speed up optical ray tracing. Porting the simulation code to run on GPUs would dramatically reduce runtime, making high-fidelity models (including all of the above effects) tractable\supercite{gpu}.
\section{\textcolor{midnightblue}{conclusion}}
We have introduced an angular-sampling ray-tracing framework for modeling NaI(Tl) gamma-ray detector response that systematically bridges the gap between analytic approximations and full Monte Carlo simulations. By discretizing the incident flux over a uniform grid of polar and azimuthal angles and applying exact ray–cylinder intersection boundary condition checks, our method naturally incorporates correlations between scattering angle, energy loss, and escape probability—features often neglected in traditional analytic approaches and costly to converge in stochastic Monte Carlo models.\\

Our approach integrates the full Klein–Nishina differential cross section, modified by an energy-dependent incoherent-scattering function, with depth-weighted attenuation and escape probabilities computed via ray-tracing of incident $\gamma$-rays. A Gaussian convolution kernel, derived from the detector's energy resolution, is then applied to the differential energy cross section to reproduce both continuum shapes and edge features deterministically. This angular sweep, combined with a multithreaded Python implementation sampling hundreds of incident and scattering angle permutations, yields a computationally efficient yet rigorous model of single Compton scattering processes.\\

Comparison with a reference 137Cs spectrum acquired on a 1.5"$\times$1.5" NaI(Tl) detector demonstrates excellent agreement: the computed Compton edge at 0.480 MeV is within 0.002 MeV of the theoretical value, and the modeled continuum closely follows the measured counts across the energy range of interest when not including potential backscatter. The observed discrepancies in the backscatter region and near the Compton edge tail point to physical phenomena not yet incorporated in our single-scatter model—specifically multiple scattering events, coincident X-ray summing, and environmental backscatter\supercite{gamma}. These limitations represent clear pathways for future enhancement of the framework.\\

Looking forward, extending the framework to include multiple Compton scatters, finer angular and spatial sampling, and detailed source and environmental geometries will further enhance accuracy. Incorporating GPU-accelerated ray tracing and real-time calibration mechanisms promises to make high-fidelity, reproducible detector response models tractable for rapid analysis in nuclear safeguards, spectroscopy, and radiation safety applications. The deterministic nature of our method offers clear advantages in interpretability and reproducibility, laying the groundwork for next-generation gamma-ray spectroscopy simulation tools.
\section*{}
\vspace*{-8pt}
\printbibliography
\end{document}
