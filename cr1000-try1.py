#!/usr/bin/env python

import cr1000
import ecospec
import time

data_set_id = time.strftime("%Y%m%d%H%M%S")
since_time  = time.strftime("%Y-%m-%dT06:00:00.00")

data_logger = cr1000.CR1000(data_set_id, 0, ecospec.EcoSpec.DATA_PATH, ecospec.EcoSpec.LOG_PATH, since_time, ecospec.EcoSpec.CR1000_HOST)

exit(0)
