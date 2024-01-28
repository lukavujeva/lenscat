import os
import copy
import re
import numpy as np
import astropy.units as u
import requests

from astropy.coordinates import SkyCoord
from ligo.skymap.postprocess import crossmatch as ligoskymap_crossmatch

def convert_to_astropy_unit(table):
    """
    TODO: convert this to a proper docstring

    Loop over the column names of the given table,
    if a column name contains a pair of square bracket,
    convert that column with the proper astropy unit if possible. 
    After the conversion, the square bracket will be removed from the name.
    Note that changes are made **in-place**.

    For example, suppose we have the following column names in a table:
    ["Name", "RA [deg]", "DEC [deg]"]

    After invoking this function, the table will have the following column names
    ["Name", "RA", "DEC"]
    and the second and third columns will have a unit of deg
    """
    _regex = r"\[([A-Za-z0-9_]+)\]"
    column_names = copy.deepcopy(table.columns)
    for colname in column_names:
        m = re.search(_regex, colname)

        if m is not None:
            unit_name = m.group(1)
            # Search for this in astropy.units
            if unit_name in dir(u):
                unit = eval(f"u.{unit_name}")
                # Assign unit
                table[colname].unit = unit
                # Rename column
                new_name = re.sub(_regex, '', colname).strip()
                table.rename_column(colname, new_name)

def parse_skymap_str(skymap_str):
    # If skymap_str points to a valid filepath,
    # do nothing and return
    if os.path.exists(skymap_str):
        return skymap_str

    _supported_GWTC1_event_list = [
        "GW150914",
        "GW151012",
        "GW151226",
        "GW170104",
        "GW170608",
        "GW170729",
        "GW170809",
        "GW170814",
        "GW170817",
        "GW170818",
        "GW170823",
    ]
    if skymap_str in _supported_GWTC1_event_list:
        # skymap_str points to an event in GWTC-1
        dcc_url_template = "https://dcc.ligo.org/public/0157/P1800381/007/{}_skymap.fits.gz"
        url = dcc_url_template.format(skymap_str)
        if requests.options(url).ok:
            return url
    elif skymap_str.startswith('S'):
        # Maybe skymap_str is the name of a superevent
        gracedb_skymap_url_template = "https://gracedb.ligo.org/api/superevents/{}/files/{}.multiorder.fits"

        # Try using bilby skymap if possible
        url = gracedb_skymap_url_template.format(skymap_str, "Bilby")
        if requests.options(url).ok:
            return url
        
        # If bilby skymap is not available, try bayestar next
        url = gracedb_skymap_url_template.format(skymap_str, "bayestar")
        if requests.options(url).ok:
            return url

    # Exhausted all possible resolutions, give up
    raise ValueError(f"Does not recognize {skymap_str}")

def crossmatch_with_catalog(skymap, catalog):
    coordinates = SkyCoord(catalog["RA"], catalog["DEC"])
    crossmatch_res = ligoskymap_crossmatch(skymap, coordinates)

    return crossmatch_res

def filter_catalog_by_type(catalog, type):
    return catalog[catalog["type"] == type]

def convert_from_ICRS_to_healpy_convention(RA, DEC):
    """
    TODO: convert this to a proper docstring

    Convert (RA, DEC) complying to the ICRS standard to
    the healpy convention where \theta runs from 0 at the north
    pole to \pi at the south pole, and $\phi$ runs from 0 to 2\pi

    Input: RA, DEC
    Output: theta, phi
    """
    return np.pi/2 - np.deg2rad(DEC), np.deg2rad(RA)

def plot_catalog(catalog, filename="catalog.png"):
    import healpy as hp
    from matplotlib import pyplot as plt

    # Filter catalog by type
    galaxy_lenses = filter_catalog_by_type(catalog, "galaxy")
    cluster_lenses = filter_catalog_by_type(catalog, "cluster")

    # Fiducial value for plotting
    _NSIDE = 32 
    plt.figure(dpi=300)
    # Set up a blank canvas, rotated by 180 deg so that 0 is at the left margin
    hp.mollview(np.zeros(hp.nside2npix(_NSIDE))+4.5, rot=180, cbar=False, min=-1, max=5, bgcolor="none", cmap="Greys")
    hp.projscatter(*convert_from_ICRS_to_healpy_convention(galaxy_lenses["RA"], galaxy_lenses["DEC"]), lonlat=False, color="cyan", s=15, label="Galaxy", alpha = 0.7)
    hp.projscatter(*convert_from_ICRS_to_healpy_convention(cluster_lenses["RA"], cluster_lenses["DEC"]), lonlat=False, color="magenta", s=15, label="Cluster", alpha = 0.7)
    hp.graticule(alpha=0.4, color="grey")
    plt.legend(labelcolor="white", facecolor="dimgrey")
    plt.title("Lenses included in "+r"${\tt lenscat}$", fontsize=18, color="white")
    plt.savefig(filename, transparent=True)
