from scipy.constants import elementary_charge
import toddler.physics.flow


def eV_to_J(eV):
    return eV * elementary_charge


def SEI(power, flowrate_slm):
    return power / toddler.physics.flow.slm_to_moles(flowrate_slm)  # [J/mol]


def SEI_J_per_mol(power, flowrate_slm):
    return power / toddler.physics.flow.slm_to_moles(flowrate_slm)  # [J/mol]


def SEI_J_per_g(power, flowrate_slm, amu):
    return SEI_J_per_mol(power, flowrate_slm) / amu  # [J/g]
