#!/usr/bin/env python
# encoding: utf-8

################################################################################
#
#   RMG - Reaction Mechanism Generator
#
#   Copyright (c) 2002-2009 Prof. William H. Green (whgreen@mit.edu) and the
#   RMG Team (rmg_dev@mit.edu)
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
################################################################################

"""
This script contains unit tests of the :mod:`rmgpy.statmech.rotation` module.
"""

import unittest
import math
import numpy

from rmgpy.statmech.rotation import *
import rmgpy.constants as constants

################################################################################

class TestLinearRotor(unittest.TestCase):
    """
    Contains unit tests of the LinearRotor class.
    """
    
    def setUp(self):
        """
        A function run before each unit test in this class.
        """
        self.inertia = 11.75
        self.symmetry = 2
        self.quantum = False
        self.mode = LinearRotor(
            inertia = (self.inertia,"amu*angstrom^2"), 
            symmetry = self.symmetry, 
            quantum = self.quantum,
        )
        
    def test_getRotationalConstant(self):
        """
        Test getting the LinearRotor.rotationalConstant property.
        """
        Bexp = 1.434692
        Bact = self.mode.rotationalConstant.value_si
        self.assertAlmostEqual(Bexp, Bact, 4)
        
    def test_setRotationalConstant(self):
        """
        Test setting the LinearRotor.rotationalConstant property.
        """
        B = self.mode.rotationalConstant
        B.value_si *= 2
        self.mode.rotationalConstant = B
        Iexp = 0.5 * self.inertia
        Iact = self.mode.inertia.value_si * constants.Na * 1e23
        self.assertAlmostEqual(Iexp, Iact, 4)
        
    def test_getLevelEnergy(self):
        """
        Test the LinearRotor.getLevelEnergy() method.
        """
        B = self.mode.rotationalConstant.value_si * constants.h * constants.c * 100.
        B *= constants.Na
        for J in range(0, 100):
            Eexp = B * J * (J + 1)
            Eact = self.mode.getLevelEnergy(J)
            if J == 0:
                self.assertEqual(Eact, 0)
            else:
                self.assertAlmostEqual(Eexp, Eact, delta=1e-4*Eexp)
    
    def test_getLevelDegeneracy(self):
        """
        Test the LinearRotor.getLevelDegeneracy() method.
        """
        for J in range(0, 100):
            gexp = 2 * J + 1
            gact = self.mode.getLevelDegeneracy(J)
            self.assertEqual(gexp, gact)
    
    def test_getPartitionFunction_classical(self):
        """
        Test the LinearRotor.getPartitionFunction() method for a classical
        rotor.
        """
        self.mode.quantum = False
        Tlist = numpy.array([300,500,1000,1500,2000])
        Qexplist = numpy.array([72.6691, 121.115, 242.230, 363.346, 484.461])
        for T, Qexp in zip(Tlist, Qexplist):
            Qact = self.mode.getPartitionFunction(T)
            self.assertAlmostEqual(Qexp, Qact, delta=1e-4*Qexp)
            
    def test_getPartitionFunction_quantum(self):
        """
        Test the LinearRotor.getPartitionFunction() method for a quantum
        rotor.
        """
        self.mode.quantum = True
        Tlist = numpy.array([300,500,1000,1500,2000])
        Qexplist = numpy.array([72.8360, 121.282, 242.391, 363.512, 484.627])
        for T, Qexp in zip(Tlist, Qexplist):
            Qact = self.mode.getPartitionFunction(T)
            self.assertAlmostEqual(Qexp, Qact, delta=1e-4*Qexp)
            
    def test_getHeatCapacity_classical(self):
        """
        Test the LinearRotor.getHeatCapacity() method using a classical rotor.
        """
        self.mode.quantum = False
        Tlist = numpy.array([300,500,1000,1500,2000])
        Cvexplist = numpy.array([1, 1, 1, 1, 1]) * constants.R
        for T, Cvexp in zip(Tlist, Cvexplist):
            Cvact = self.mode.getHeatCapacity(T)
            self.assertAlmostEqual(Cvexp, Cvact, delta=1e-4*Cvexp)
            
    def test_getHeatCapacity_quantum(self):
        """
        Test the LinearRotor.getHeatCapacity() method using a quantum rotor.
        """
        self.mode.quantum = True
        Tlist = numpy.array([300,500,1000,1500,2000])
        Cvexplist = numpy.array([1, 1, 1, 1, 1]) * constants.R
        for T, Cvexp in zip(Tlist, Cvexplist):
            Cvact = self.mode.getHeatCapacity(T)
            self.assertAlmostEqual(Cvexp, Cvact, delta=1e-4*Cvexp)
       
    def test_getEnthalpy_classical(self):
        """
        Test the LinearRotor.getEnthalpy() method using a classical rotor.
        """
        self.mode.quantum = False
        Tlist = numpy.array([300,500,1000,1500,2000])
        Hexplist = numpy.array([1, 1, 1, 1, 1]) * constants.R * Tlist
        for T, Hexp in zip(Tlist, Hexplist):
            Hact = self.mode.getEnthalpy(T)
            self.assertAlmostEqual(Hexp, Hact, delta=1e-4*Hexp)
    
    def test_getEnthalpy_quantum(self):
        """
        Test the LinearRotor.getEnthalpy() method using a quantum rotor.
        """
        self.mode.quantum = True
        Tlist = numpy.array([300,500,1000,1500,2000])
        Hexplist = numpy.array([0.997705, 0.998624, 0.999312, 0.999541, 0.999656]) * constants.R * Tlist
        for T, Hexp in zip(Tlist, Hexplist):
            Hact = self.mode.getEnthalpy(T)
            self.assertAlmostEqual(Hexp, Hact, delta=1e-4*Hexp)

    def test_getEntropy_classical(self):
        """
        Test the LinearRotor.getEntropy() method using a classical rotor.
        """
        self.mode.quantum = False
        Tlist = numpy.array([300,500,1000,1500,2000])
        Sexplist = numpy.array([5.28592, 5.79674, 6.48989, 6.89535, 7.18304]) * constants.R
        for T, Sexp in zip(Tlist, Sexplist):
            Sact = self.mode.getEntropy(T)
            self.assertAlmostEqual(Sexp, Sact, delta=1e-4*Sexp)
    
    def test_getEntropy_quantum(self):
        """
        Test the LinearRotor.getEntropy() method using a quantum rotor.
        """
        self.mode.quantum = True
        Tlist = numpy.array([300,500,1000,1500,2000])
        Sexplist = numpy.array([5.28592, 5.79674, 6.48989, 6.89535, 7.18304]) * constants.R
        for T, Sexp in zip(Tlist, Sexplist):
            Sact = self.mode.getEntropy(T)
            self.assertAlmostEqual(Sexp, Sact, delta=1e-4*Sexp)

    def test_getSumOfStates_classical(self):
        """
        Test the LinearRotor.getSumOfStates() method using a classical rotor.
        """
        self.mode.quantum = False
        Elist = numpy.arange(0, 2000*11.96, 1.0*11.96)
        densStates = self.mode.getDensityOfStates(Elist)
        sumStates = self.mode.getSumOfStates(Elist)
        for n in range(1, len(Elist)):
            self.assertAlmostEqual(numpy.sum(densStates[0:n]) / sumStates[n], 1.0, 3)

    def test_getSumOfStates_quantum(self):
        """
        Test the LinearRotor.getSumOfStates() method using a quantum rotor.
        """
        self.mode.quantum = True
        Elist = numpy.arange(0, 4000.*11.96, 2.0*11.96)
        densStates = self.mode.getDensityOfStates(Elist)
        sumStates = self.mode.getSumOfStates(Elist)
        for n in range(1, len(Elist)):
            self.assertAlmostEqual(numpy.sum(densStates[0:n+1]) / sumStates[n], 1.0, 3)

    def test_getDensityOfStates_classical(self):
        """
        Test the LinearRotor.getDensityOfStates() method using a classical
        rotor.
        """
        self.mode.quantum = False
        Tlist = numpy.array([300,400,500])
        Elist = numpy.arange(0, 4000.*11.96, 1.0*11.96)
        for T in Tlist:
            densStates = self.mode.getDensityOfStates(Elist)
            Qact = numpy.sum(densStates * numpy.exp(-Elist / constants.R / T))
            Qexp = self.mode.getPartitionFunction(T)
            self.assertAlmostEqual(Qexp, Qact, delta=1e-2*Qexp)

    def test_getDensityOfStates_quantum(self):
        """
        Test the LinearRotor.getDensityOfStates() method using a quantum rotor.
        """
        self.mode.quantum = True
        Tlist = numpy.array([300,400,500])
        Elist = numpy.arange(0, 4000.*11.96, 2.0*11.96)
        for T in Tlist:
            densStates = self.mode.getDensityOfStates(Elist)
            Qact = numpy.sum(densStates * numpy.exp(-Elist / constants.R / T))
            Qexp = self.mode.getPartitionFunction(T)
            self.assertAlmostEqual(Qexp, Qact, delta=1e-2*Qexp)

    def test_repr(self):
        """
        Test that a LinearRotor object can be reconstructed from its repr()
        output with no loss of information.
        """
        exec('mode = {0!r}'.format(self.mode))
        self.assertAlmostEqual(self.mode.inertia.value, mode.inertia.value, 6)
        self.assertEqual(self.mode.inertia.units, mode.inertia.units)
        self.assertEqual(self.mode.symmetry, mode.symmetry)
        self.assertEqual(self.mode.quantum, mode.quantum)
        
    def test_pickle(self):
        """
        Test that a LinearRotor object can be pickled and unpickled with no
        loss of information.
        """
        import cPickle
        mode = cPickle.loads(cPickle.dumps(self.mode))
        self.assertAlmostEqual(self.mode.inertia.value, mode.inertia.value, 6)
        self.assertEqual(self.mode.inertia.units, mode.inertia.units)
        self.assertEqual(self.mode.symmetry, mode.symmetry)
        self.assertEqual(self.mode.quantum, mode.quantum)
