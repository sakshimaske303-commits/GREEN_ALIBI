# Trigger 1 of the Manual for Drought Management (Revised Dec 2016, Table 3.10), on daily rain from 1 June
#   a dry spell sets the trigger whatever the deficit; without one, rainfall must be scanty (60% or more
#   below normal) or SPI below -1.5. A dry spell is consecutive weeks after the normal onset date, each with
#   less than 50% of normal weekly rain: usually 4 weeks, 3 on light soils (Section 3.2.1).
# Days are counted from 1 June (day 0); 30 September is day 121.

import numpy as np
import pandas as pd
from scipy import stats

N_DAYS = 122
# Weeks are IMD standard meteorological weeks (SMW 24 = 11-17 June ... SMW 39 = 24-30 September).
# The normal onset over the region is about 15 June (12 June at Ahmednagar, 15 June at Nagpur; IMD, 2020),
# so dry weeks are counted from the first full week after it, SMW 25 (18-24 June).
ONSET_DAY = 17            # 18 June, start of SMW 25
JULY_DAY = 31             # 2 July, start of SMW 27: sensitivity, dry weeks counted only from July
MONTH_ENDS = [60, 91, 121]  # 31 Jul, 31 Aug, 30 Sep: when the rainfall deviation and SPI are assessed
DRY_SHARE = 0.5
SCANTY_PCT = 60
SPI_LIMIT = -1.5
VARIANTS = {  # name: (dry weeks, first day the weeks are counted from)
    "main: Manual Trigger 1, 4 dry weeks": (4, ONSET_DAY),
    "Manual Trigger 1, 3 dry weeks (light soils)": (3, ONSET_DAY),
    "Manual Trigger 1, 4 dry weeks counted from July": (4, JULY_DAY),
    "Manual Trigger 1, 3 dry weeks counted from July": (3, JULY_DAY),
}
MAIN = list(VARIANTS)[0]


def spi(cum, base_mask):
    # SPI of each year's cumulative rain against a gamma fitted to the base years (McKee et al., 1993)
    a, loc, scale = stats.gamma.fit(cum[base_mask], floc=0)
    return stats.norm.ppf(np.clip(stats.gamma.cdf(cum, a, loc=loc, scale=scale), 1e-6, 1 - 1e-6))


def trigger_day(rain, normal, spi_me, weeks, first_day):
    """rain, normal: (122, n) daily mm; spi_me: (3, n) SPI at the month ends.
    Returns (day the trigger is first met or nan, which arm met it first) for each of the n columns."""
    rain, normal = np.asarray(rain, float).reshape(N_DAYS, -1), np.asarray(normal, float).reshape(N_DAYS, -1)
    spi_me = np.asarray(spi_me, float).reshape(len(MONTH_ENDS), -1)
    n = rain.shape[1]
    spell = np.full(n, np.nan)
    run = np.zeros(n, int)
    for k in range((N_DAYS - first_day) // 7):
        s, e = first_day + 7 * k, first_day + 7 * k + 7
        dry = rain[s:e].sum(0) < DRY_SHARE * normal[s:e].sum(0)
        run = np.where(dry, run + 1, 0)
        spell = np.where(np.isnan(spell) & (run >= weeks), e - 1, spell)
    dev = 100 * (1 - rain.cumsum(0)[MONTH_ENDS] / normal.cumsum(0)[MONTH_ENDS])  # (3, n), + = deficit
    me = np.array(MONTH_ENDS, float)[:, None]
    scanty = np.where(dev >= SCANTY_PCT, me, np.nan)
    low_spi = np.where(spi_me < SPI_LIMIT, me, np.nan)
    arms = np.vstack([spell, np.nanmin(np.where(np.isnan(scanty), np.inf, scanty), 0),
                      np.nanmin(np.where(np.isnan(low_spi), np.inf, low_spi), 0)])
    arms[np.isinf(arms)] = np.nan
    day = np.where(np.all(np.isnan(arms), 0), np.nan, np.nanmin(np.where(np.isnan(arms), np.inf, arms), 0))
    names = np.array(["dry spell", "scanty rain", "SPI below -1.5"])
    first = np.where(np.isnan(day), "", names[np.argmin(np.where(np.isnan(arms), np.inf, arms), 0)])
    return day, first


def day_to_doy(year, day):
    return np.nan if np.isnan(day) else float((pd.Timestamp(year, 6, 1) + pd.Timedelta(days=int(day))).dayofyear)
