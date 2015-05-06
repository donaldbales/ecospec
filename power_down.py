#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import ecospec
import piface

x = piface.PiFace()

x.power_down(ecospec.EcoSpec.POWER_RELAY)
