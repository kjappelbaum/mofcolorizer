# -*- coding: utf-8 -*-
# pylint:disable=line-too-long
"""Featurization code. Copied from the colorml package to make the installation a bit less of a pain"""
from __future__ import absolute_import, print_function

import os
from pathlib import Path

import numpy as np
import openbabel as ob
import pandas as pd
import pybel
from mofid.run_mofid import cif2mofid
from pymatgen.io.cif import CifParser
from six.moves import zip

# This code relies on my fork of molsimplify which outputs the sum and the average RACs
from molSimplify.Informatics.MOF.MOF_descriptors import get_MOF_descriptors

from .utils import make_temp_directory, temp


class FeaturizationException(Exception):
    pass


def get_primitive(datapath, writepath):
    """Generate primitive structure which is needed for molsimplify"""
    s = CifParser(datapath, occupancy_tolerance=1).get_structures()[0]  # pylint:disable=invalid-name
    sprim = s.get_primitive_structure()
    sprim.to('cif', writepath)


def openbabel_count_bond_order(mol, bo=2):  # pylint:disable=invalid-name
    """Count how often bond order bo occures in openbabel molecule mol"""
    count = 0
    mole = mol.OBMol
    for bond in ob.OBMolBondIter(mole):
        if bond.GetBO() == bo:
            count += 1
    return count


def openbabel_count_aromatic_rings(mol):
    """Calculate aromatic rings in an openbabel molecule"""
    count = 0
    mole = mol.OBMol
    for ring in mole.GetSSSR():
        # Note: the OB implementation is wrong. It assumes that if all
        # atoms in the ring are aromatic then the ring itself must be
        # aromatic. This is not necessarily true.
        if ring.IsAromatic():
            count += 1
    return count


def openbabel_count_aromatic(mol):
    """Calculate aromatic bonds in an openbabel molecule"""
    carboncounter = 1
    double_cc = 1
    mole = mol.OBMol
    for bond in ob.OBMolBondIter(mole):
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        symbol1 = atom1.GetAtomicNum()
        symbol2 = atom2.GetAtomicNum()

        if symbol1 == symbol2 == 6:
            carboncounter += 1
            if bond.IsDouble():
                double_cc += 1

    return double_cc / carboncounter - 1


def get_group_counts(mol):
    """Calculate the groups that are already implemented in openbabel based on an openbabel mol"""
    mole = mol.OBMol
    group_dict = {
        'primary_amide': 0,
        'secondary_amide': 0,
        'tertiary_amide': 0,
        'ester': 0,
        'carbonyl': 0,
    }
    for bond in ob.OBMolBondIter(mole):
        if bond.IsPrimaryAmide():
            group_dict['primary_amide'] += 1
        elif bond.IsSecondaryAmide():
            group_dict['primary_amide'] += 1
        elif bond.IsTertiaryAmide():
            group_dict['tertiary_amide'] += 1
        elif bond.IsEster():
            group_dict['ester'] += 1
        elif bond.IsCarbonyl():
            group_dict['carbonyl'] += 1

    return group_dict


def get_molecular_descriptors(smiles):
    """get heuristics from strings using openbabel"""
    mymol = pybel.readstring('smi', smiles)

    descriptordict = {}

    group_counts = get_group_counts(mymol)
    desc = mymol.calcdesc()
    db_ratio = openbabel_count_aromatic(mymol)
    aromatic_rings = openbabel_count_aromatic_rings(mymol)

    descriptordict.update(group_counts)
    descriptordict['logP'] = desc['logP']
    descriptordict['MR'] = desc['MR']
    descriptordict['dbratio'] = db_ratio
    descriptordict['aromatic_rings'] = aromatic_rings
    descriptordict['dbonds'] = desc['dbonds']
    descriptordict['abonds'] = desc['abonds']

    return descriptordict


def get_smiles_features(cif):
    """Use openbabel to calculate some features based on the smiles which we get from MOFid"""
    # make sure that the output is automatically deleted.
    with make_temp_directory() as temp_dir:
        mofid = cif2mofid(cif, temp_dir)
    name = mofid['cifname']

    linker_descriptors = []

    try:
        for linker in mofid['smiles_linkers']:
            linker_descriptors.append(list(get_molecular_descriptors(linker).values()))
            # super inefficient to do this all the time. But i do not know if i'll change the descriptorlist ...
            keys = list(get_molecular_descriptors(linker).keys())
            mean_keys = [s + '_mean' for s in keys]
            sum_keys = [s + '_sum' for s in keys]

        linker_descriptors = np.array(linker_descriptors)
        means = np.mean(linker_descriptors, axis=0)
        sums = np.mean(linker_descriptors, axis=0)

        mean_dict = dict(list(zip(mean_keys, means)))
        sum_dict = dict(list(zip(sum_keys, sums)))

        result_dict = {}
        result_dict['name'] = name

        result_dict.update(sum_dict)
        result_dict.update(mean_dict)

        return result_dict
    except Exception as e:  # pylint:disable=invalid-name, broad-except
        print(e)
        return None


def get_moldesc(cifs):
    """featurizers the linkers"""
    result_list = []
    for cif in cifs:
        result_list.append(get_smiles_features(cif))
    try:
        df = pd.DataFrame(result_list)  # pylint:disable=invalid-name
    except Exception as e:  # pylint:disable=broad-except
        print(e)
        df = result_list  # pylint:disable=invalid-name

    return df


def get_racs(cif):
    """Assumes that cif is primitive. As there is no way in molsimplify to stop writing stuff, we do it in some temporary directory"""
    featurization_list = []
    # need to catch and handle exceptions

    with make_temp_directory() as temp_dir:
        full_names, full_descriptors = get_MOF_descriptors(
            cif,  # inputstructure
            3,  # scope
            path=temp_dir,  # stuff will be dumped here
            xyzpath=os.path.join(temp_dir, 'file.xyz'),
        )
        full_names.append('filename')
        full_descriptors.append(Path(cif).stem)
        featurization = dict(zip(full_names, full_descriptors))
        featurization_list.append(featurization)

    df = pd.DataFrame(featurization_list)  # pylint:disable=invalid-name
    keep = [val for val in df.columns.values if ('mc' in val) or ('lc' in val) or ('f-lig' in val) or ('func' in val)]
    df = df[['filename'] + keep]  # pylint:disable=invalid-name

    # Now, we need to employ a workaround because the feature names changed mc_CR -> mc with open sourcing the MOF RACs code
    mc_features = [val for val in df.columns.values if 'mc' in val]
    # if we use the old version, all should have CRY in name, in the new version no feature should have CRY in name
    if not 'CRY' in mc_features[0]:
        mc_features_new = [val.replace('mc', 'mc_CRY') for val in mc_features]
        replacement_dict = dict(zip(mc_features, mc_features_new))
        df.rename(columns=replacement_dict, inplace=True)
    # need to generate sums and differences
    return df


def merge_racs_moldesc(df_moldesc, df_racs):
    """Merge df assuming that the filename columns are filename and racs"""
    df_merged = pd.merge(df_racs, df_moldesc, left_on='filename', right_on='name')
    return df_merged


def get_color_descriptors(cif):
    """Orchestrate the featurization"""
    try:
        with temp() as tempfile:
            tempname = tempfile.name
            get_primitive(cif, tempname)
            moldesc = get_moldesc([tempname])
            racs = get_racs(tempname)
        df_features = merge_racs_moldesc(moldesc, racs)
        return df_features
    except Exception as e:  # pylint:disable=invalid-name
        raise FeaturizationException('Could not featurize the structure due to  {}'.format(e))
