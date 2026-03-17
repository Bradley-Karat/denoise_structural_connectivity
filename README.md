# Denoising structural connectivity

## Overview
This toolbox provides a function for denoising streamline count data derived from diffusion MRI tractography. Count data is often complicated by heteroskedastic noise, complicating the application of MPPCA for denoising. Using matrix biwhitening, this tool transforms the input matrix such that the noise is homoskedastic, where MPPCA can be used to seperate signal and noise. The toolbox relies on the [BiPCA python package](https://github.com/KlugerLab/bipca).

## Download and usage


## References
* "Population-level denoising of brain connectivity data using random matrix theory"
* Stanley, J. S., Yang, J., Li, R., Lindenbaum, O., Kobak, D., Landa, B., & Kluger, Y. (2025). Principled PCA separates signal from noise in omics count data. https://doi.org/10.1101/2025.02.03.636129

‌
