import datetime
import numpy as np
from scipy.optimize import fsolve
from dateutil.relativedelta import relativedelta
import holidays
from typing import List, Dict, Union, Optional
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)