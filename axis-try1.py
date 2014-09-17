#!/usr/bin/env python

import axis_q1604
import ecospec
import time

data_set_id = time.strftime("%Y%m%d%H%M%S")

camera = axis_q1604.AxisQ1604(data_set_id, 0, ecospec.EcoSpec.DATA_PATH, ecospec.EcoSpec.LOG_PATH, ecospec.EcoSpec.AXIS_Q1604_HOST)

exit(0)
