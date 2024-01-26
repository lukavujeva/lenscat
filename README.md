# $\texttt{lenscat}$
![license](https://img.shields.io/github/license/lenscat/lenscat)
[![GitHub release](https://img.shields.io/github/v/release/lenscat/lenscat.svg)](https://github.com/lenscat/lenscat/releases)

A public and community-maintained catalog of known strong gravitational lenses. 

![Known Lenses](lenscat_galclust.png)

## Quickstart

The catalog is available as a _plain csv file_ under [lenscat/data/catalog.csv](https://github.com/lenscat/lenscat/blob/main/lenscat/data/catalog.csv).

We also provide a _python package_ `lenscat`, available in pypi. Simply do
```bash
pip install lenscat
```
to install the latest version. The code converts the catalog in the csv file into a `Table` object in `astropy`. To access the table, simply run
```python
import lenscat
lenscat.catalog
```
<img width="623" alt="catalog" src="https://github.com/lenscat/lenscat/assets/55488840/253744e4-5860-4456-a016-fa7c5745205f">

The code also implements `crossmatch()`, a wrapper to the `crossmatch()` function in `ligo.skymap`, to cross-match a gravitational-wave (GW) skymap with the catalog. For example, to cross-match the GW skymap of GW170817 with the catalog, simply run
```python
import lenscat
lenscat.crossmatch("GW170817")
```
where the code will automatically download the skymap from the internet. Refer to the documentation for more details.
<img width="899" alt="crossmatch" src="https://github.com/lenscat/lenscat/assets/55488840/38b78d6c-99e1-41d9-ae19-4c33186dd57e">

## Format

['name'] = Names of galaxies/galaxy clusters \
['RA [deg]'] = RA in dergees \
['DEC [deg]'] = DEC in degrees \
['zlens'] = Lens redshift (if known) \
['type'] = Type of lens (i.e. galaxy or galaxy cluster) \
['grading'] = Grading whether it is a confirmed lens or a probable lens (see individual references for internal ranking systems) \
['ref'] = Reference to the corresponding catalogue or study

## References

This catalog contains the known strong lenses from the following studies:

  - GLQ Database:
    https://research.ast.cam.ac.uk/lensedquasars/index.html

  - CLASH (Postman+2012):
    https://archive.stsci.edu/prepds/clash/

  - MUSES Cluster Followups (Richards+2020):
    https://cral-perso.univ-lyon1.fr/labo/perso/johan.richard/MUSE_data_release/

  - RELICS
    https://relics.stsci.edu/clusters.html

  - 37 Clusters from SDSS Giant Arcs Survey
    https://iopscience.iop.org/article/10.3847/1538-4365/ab5f13

  - An Extended Catalog of Galaxy–Galaxy Strong Gravitational Lenses Discovered in DES Using Convolutional Neural Networks
    https://iopscience.iop.org/article/10.3847/1538-4365/ab26b6#apjsab26b6t5

  - The AGEL Survey: Spectroscopic Confirmation of Strong Gravitational Lenses in the DES
    and DECaLS Fields Selected Using Convolutional Neural Networks
    https://arxiv.org/ftp/arxiv/papers/2205/2205.05307.pdf

  - LSD Survey
    https://web.physics.ucsb.edu/~tt/LSD/

  - (COSMOS) LensFlow: A Convolutional Neural Network in Search of Strong Gravitational Lenses
    https://ui.adsabs.harvard.edu/abs/2018ApJ...856...68P/abstract

  - SLACS. XIII. Galaxy-scale strong lens candidates
    https://ui.adsabs.harvard.edu/abs/2019yCat..18510048S/abstract

  - RINGFINDER: Automated Detection of Galaxy-scale Gravitational Lenses in Ground-based Multi-filter Imaging Data
    https://iopscience.iop.org/article/10.1088/0004-637X/785/2/144

## See also
[Master Lens Database](https://test.masterlens.org/index.php)

## Acknowledgements
This project was supported by the research grant no. VIL37766 and no. VIL53101 from Villum Fonden, and the DNRF Chair program grant no. DNRF162 by the Danish National Research Foundation.

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 101131233.
