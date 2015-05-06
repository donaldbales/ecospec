#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import ecospec
import piface

x = piface.PiFace()

x.retract_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)

