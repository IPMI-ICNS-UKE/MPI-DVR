# MPI-DVR
3D Direct Volume Rendering (DVR) for real time-capable 3D visualization of Magnetic Particle Imaging (MPI) data.

This repository contains the Python code and MPI image data sets associated to our manuscript *Combining Direct 3D Volume Rendering and Magnetic Particle Imaging to Advance Radiation-Free Real-Time 3D Guidance of Vascular Interventions*, to be published in *CardioVascular and Interventional Radiology*:

```
@article{Weller2019,
	author = {Weller, Dominik and Salamon, Johannes M and Fr{\"o}lich, Andreas and M{\"o}ddel, Martin and Knopp, Tobias and Werner, Rene},
	title = {Combining Direct {3D} Volume Rendering and Magnetic Particle Imaging to Advance Radiation-Free Real-Time {3D} Guidance of Vascular Interventions},
	journal = {{C}ardio{V}ascular and {I}nterventional {R}adiology},
	year = {2019},
	volume = {NN},
	number = {NN},
	pages = {(in print)},
	doi = {10.1007/s00270-019-02340-4}
}
```

## Requirements
The provided code has been tested with Python 3.6.6 on Windows 10 Home. The following Python packages are required (lower versions may also be sufficient):
- H5py >= 2.9.0
- Matplotlib >= 3.0.3
- Numpy >= 1.13.0
- pyqt >= 5.6.0
- spyder >= 3.3.1
- VTK >= 8.1.0

## Program start
To start the visualization program, run the main file in the Spyder editor. Load the .mdf/.mha data you wish to view into the reader using the "Load MDF"/"Load MHA" button. Pressing the play button will start the visualization process. In order to create screenshots, it is necessary to specify a saving directory beforehand. The implemented UI allows for interactive control of essential visualization parameters (e.g. image value threshold, opacity, color) and playback settings. 

The MPI data sets provided in the subsection “MPI data” represent the use cases illustrated in the corresponding publication. The exact visualization parameters that were used in each case are documented below. They can be applied manually via the program interface. 

## Visualization parameters
### Aneurysm
- Image size: 100 x 100 x 100 
- Bolus color map: min=0.02, max=0.055
- Roadmap color: ‘blue’
- Opacity roadmap: (0, 0.0), (0.020, 0.00), (0.025, 0.2), (0.101, 0.2)
- Opacity bolus: (0, 0.0), (0.016, 0.0), (0.017, 0.7), (0.191, 0.7)

### Middle cerebral artery
- Image size: 100 x 100 x 100
- Bolus color map: min=0.05, max=0.1
- Roadmap color: ‘blue’
- Opacity roadmap: (0.000, 0.0), (0.010, 0.0), (0.045, 0.8), (0.100, 0.8)
- Opacity bolus: (0.000, 0.0), (0.020, 0.0), (0.021, 0.8), (0.191, 0.8)

### Hepatic artery
- Image size: 100 x 100 x 100
- Bolus color map: min=0.02, max=0.065	
- Roadmap color: ‘blue’
- Opacity roadmap: (0, 0.0), (0.020, 0.00), (0.025, 0.2), (0.101, 0.2)
- Opacity bolus: (0, 0.0), (0.010, 0.0), (0.02, 0.3), (0.0.04, 0.6), (0.1, 0.6)
