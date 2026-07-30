# GREEN ALIBI — Development Log

## Entry 1: Project Framing and Motivation

**What this project is.** GREEN ALIBI is an independent satellite-verification study
testing whether Solar-Induced Fluorescence (SIF) — a direct physical proxy for actual
photosynthetic activity — can detect crop and vegetation drought stress earlier than the
vegetation-greenness index (NDVI) that India's official drought-monitoring framework
currently relies on.

**The physics behind it.** NDVI is a reflectance-based index: it measures how much visible
and near-infrared light a leaf's surface reflects, and that reflectance only changes once a
plant's internal structure has already begun to visibly degrade — thinning leaves, reduced
chlorophyll content, canopy stress. SIF measures something physically earlier and more
direct. When a leaf absorbs sunlight for photosynthesis, a small fraction of that absorbed
energy is not converted into chemical energy but is instead re-emitted as fluorescence — a
process governed by the quantum yield of photosynthesis. When a plant is under physiological
stress, its photosynthetic efficiency drops before its outward greenness does, and this
shows up as a measurable change in fluorescence emission well before NDVI shows any decline.
In effect, NDVI shows a plant's alibi — it can still look green — while SIF shows what is
physically happening inside it.

**Why this project exists.** India's drought declaration process, and the crop-insurance
payout mechanism under the Pradhan Mantri Fasal Bima Yojana (PMFBY) that depends on it, is
built substantially on rainfall-deficit and NDVI-based assessment. Both are reflectance- or
precipitation-based indicators, and both are known to respond only after visible crop stress
has already set in. Delayed drought recognition means delayed insurance payouts, at exactly
the point when affected farmers need them fastest. This project treats that delay as an
empirical, testable question rather than an assumption: if SIF captures physiological stress
earlier than NDVI, and if that lag is large and consistent enough to matter, it represents a
concrete, physics-based case for an earlier-warning indicator than the one currently used in
policy.

**Aim.** To independently test, using satellite-derived SIF and NDVI datasets over
drought-affected agricultural districts in India, whether SIF shows a measurably earlier
decline than NDVI during known drought episodes, and whether the resulting lag is large
enough and consistent enough to carry practical early-warning value for drought
declaration and crop-insurance timelines.

**Research Questions.**
RQ1: Does SIF decline measurably earlier than NDVI during documented drought-onset periods
in the study region?
RQ2: Is the SIF–NDVI lag, where it exists, consistent across different districts and crop
types, or does it vary meaningfully by geography and crop physiology?
RQ3: How does the timing of SIF-based stress onset compare against official state
drought-declaration dates for the same districts and years?
RQ4: Does the observed SIF–NDVI lag translate into a practically meaningful early-warning
window — measured in weeks — relevant to real crop-insurance and drought-relief timelines?

**Hypotheses.**
H1: SIF will show a statistically significant decline before NDVI during the same drought
episode, consistent with fluorescence capturing a drop in photosynthetic efficiency ahead
of any visible, reflectance-based greenness loss.
H2: The magnitude and timing of SIF–NDVI divergence will not be uniform across crop types,
since fluorescence response depends on canopy structure and species-specific photosynthetic
pathways.
H3: Official drought declarations will lag behind the SIF-based stress signal, consistent
with the official process's reliance on slower-responding rainfall and NDVI indicators
rather than a direct physiological measure.

**Scope and current status.** This project is at its earliest planning stage. The
foundational tasks ahead are: selecting a study region with a well-documented recent drought
history and reliable official declaration records — likely candidates include the
Marathwada and Vidarbha regions of Maharashtra and the Bundelkhand region spanning Uttar
Pradesh and Madhya Pradesh, all of which have recurring, well-reported drought episodes;
sourcing a usable SIF dataset, most likely the gridded GOSIF product or a TROPOMI-derived
SIF proxy, since native fine-resolution SIF instruments are not designed for
agricultural-field-scale monitoring; sourcing matching NDVI data from MODIS or Sentinel-2
for the same districts and time windows; and identifying accessible official
drought-declaration records and, where possible, PMFBY payout timing data to serve as the
real-world policy benchmark against which the satellite-derived signal will be compared.
None of this data has been acquired yet — this entry marks the start of that process, not
its outcome.

## Entry 2: SIF Data Acquisition, a Cloud-Masking Bug, and the First Seasonal Comparison

With the project framed in Entry 1, the next task was building the actual satellite
pipeline — sourcing SIF data, sourcing a matching NDVI dataset, and producing the first
real comparison between the two for Marathwada.

**Study region and years finalized.** Marathwada was chosen as the study region — a
personal choice as much as a methodological one, since it is my own home region and has a
well-documented recent drought history. Three years were selected for the season of June
1 to November 1 (day-of-year 153–305, the Kharif growing season): 2015 and 2018, both
documented Marathwada drought years (2015 in particular being the year of the severe
Latur water crisis), and 2020, a comparatively normal monsoon year, as a baseline for
comparison.

**Sourcing SIF data.** GOSIF v2 — a global, 0.05-degree, 8-day solar-induced fluorescence
product derived from OCO-2, MODIS, and reanalysis data (Li & Xiao, 2019), distributed by
the Global Ecology Group at the University of New Hampshire — was identified as the most
usable SIF source, since native fine-resolution SIF instruments are not designed for
field-scale agricultural monitoring. Sixty 8-day GeoTIFF files were downloaded in total (20
each for 2015, 2018, and 2020, covering the same day-of-year range).

**Clipping and scaling.** A script was written to clip each global GeoTIFF to a Marathwada
bounding box (17.5°N–20.5°N, 75.0°E–78.5°E, covering all eight Marathwada districts), and,
critically, to correctly handle GOSIF's raw digital values: a scale factor of 0.0001 needed
to be applied to convert raw pixel values into actual SIF units, and two fill-value codes
(32766 for water bodies, 32767 for non-vegetated or missing data) needed to be masked out
before any averaging. Skipping this step would have silently corrupted every downstream
mean, since the fill values are numerically far outside the real SIF range and would have
dominated any naive average. A second script then aggregated each clipped file into a
single Marathwada-wide mean SIF value per date, also recording the fraction of valid
(non-masked) pixels per date as a data-quality check.

**A serious cloud-masking bug in the NDVI extraction.** NDVI was sourced separately via
Google Earth Engine, computed from MOD09Q1 (MODIS 8-day surface reflectance) so that its
temporal resolution would match GOSIF's 8-day cadence exactly. The first version of this
script computed NDVI directly from raw reflectance bands without applying any cloud-quality
filtering. The resulting NDVI time series was implausibly noisy — during the 2020 season in
particular, NDVI swung from roughly 0.55 down to 0.14 and back up to 0.60 within consecutive
8-day periods, a physically impossible rate of change for cropland vegetation. Comparing
this against the SIF series, which was smooth and phenologically sensible, made clear that
the NDVI series itself was the problem, not the underlying vegetation signal. The cause was
identified as cloud and cloud-shadow contamination: Marathwada's growing season coincides
with the monsoon, and MOD09Q1's raw reflectance, without explicit quality-band filtering,
does not reliably exclude cloud-affected pixels from its "best observation per 8-day window"
selection.

**Fix: switching to MOD13Q1 with explicit quality masking.** The NDVI extraction was rebuilt
around MOD13Q1, NASA's own 16-day Vegetation Index product, which applies a
Maximum-Value-Composite algorithm specifically to suppress cloud contamination, and which
ships with a `SummaryQA` band (0 = good, 1 = marginal, 2 = snow/ice, 3 = cloudy) that was
used to explicitly mask out anything but good-to-marginal-quality pixels. A cropland mask
(MCD12Q1 land-cover product, IGBP classes 12 and 14) was also applied at this stage, so that
forest, urban, and barren pixels within the bounding box would not dilute a signal that is
specifically about crop stress. This traded 8-day temporal resolution for 16-day, but
produced a visibly smooth, physically sensible NDVI curve — a trade worth making, since a
clean 16-day signal is more trustworthy than a noisy 8-day one.

**A second, smaller bug: an Earth Engine clip error.** The corrected script initially failed
with `Image.clip: Can't transform (0.0,0.0)`, caused by calling `.clip()` on an image built
from bands of two different native resolutions (250m NDVI, 500m-derived cropland mask). The
fix was to remove the `.clip()` call entirely, since `reduceRegion()` already restricts its
calculation to the supplied geometry — the clip step was redundant and was the one throwing
the error.

**Merging two time series at different temporal resolutions.** Since SIF (8-day) and NDVI
(16-day, after the fix) no longer shared an identical date grid, the two series were joined
using nearest-date matching per year, rather than an exact date join, so that each 8-day SIF
value was paired with its closest available 16-day NDVI value.

**A labelling bug caught before it could mislead.** An early version of the comparison plot
labelled 2018 as a "normal monsoon year," when it is in fact the second of the two documented
drought years in this study. This was a conditional-logic oversight (only 2015 had been
explicitly flagged as a drought year in the plotting code) rather than a data error, and was
corrected before any interpretation was drawn from the mislabeled chart.

**First seasonal comparison, and an honest correction of my own overclaim.** With the
corrected pipeline, SIF and NDVI trajectories were plotted for all three years. Visually, a
consistent pattern holds across all three years: SIF begins declining from its seasonal peak
before NDVI does, with NDVI holding near its peak value for a noticeably longer period after
SIF has already started dropping. This is a genuine and replicated pattern, and it directly
supports the project's core premise — that SIF is more responsive to the onset of
post-peak physiological change than NDVI is. However, an initial, more casual visual read of
the three charts led me to claim that this lag was distinctly larger in the two drought
years (2015, 2018) than in the normal year (2020). Checking that claim properly, by computing
each year's decline as a percentage of its own peak value at each subsequent date rather than
just eyeballing the chart, did not support it: the apparent lag was of a broadly similar
magnitude (roughly 15–25 days) across all three years, drought and normal alike, once
measured carefully. That earlier claim is retracted here rather than left standing — the
correct, defensible finding at this stage is that SIF leads NDVI's decline in general, not
that drought years show a demonstrably larger lag than normal years. Establishing whether
drought specifically amplifies this lag will require a proper quantitative lag metric (a
day-of-year-to-threshold comparison or a formal cross-correlation calculation) rather than
visual comparison, and is the next task.

**Status after this entry.** The SIF and NDVI extraction pipelines are both built,
cloud/quality-screened, and cropland-masked, covering three years (2015, 2018, 2020) over
Marathwada. A real, replicated SIF-leads-NDVI pattern has been observed. What remains before
this can be reported as a finding is a rigorous, numeric lag calculation in place of the
visual comparison used so far, and — ideally — at least one additional comparison year to
strengthen the small sample this analysis currently rests on.

## Entry 3: Extending the Observation Window and a Genuinely Surprising Result

Entry 2 ended with an unresolved problem: the first quantitative lag calculation
(comparing how many days after its own peak SIF and NDVI each crossed a series of
decline thresholds) produced results that could not be trusted, because the observation
window — June 1 to November 1 — ended before NDVI had finished declining in two of the
three years. Several thresholds simply never resolved (returned no crossing date at all),
and the ones that did resolve were being averaged unevenly across years, which made any
comparison between drought and normal years unreliable rather than simply inconclusive.

**Extending the window.** The fix was to extend data collection further into the year,
adding seven more 8-day GOSIF periods (day-of-year 313, 321, 329, 337, 345, 353, and 361)
for all three years, pushing the observation window from November 1 out to late December.
The same clipping and aggregation scripts built in Entry 2 picked up these additional
21 files without any code changes, since both were written to scan for whatever GOSIF
files exist in the raw data folder rather than assuming a fixed date range. The NDVI
extraction script's end date was likewise extended from November 1 to December 31, and
the same MOD13Q1 cloud-screened, cropland-masked pipeline was re-run for the longer
window.

**The extension worked as intended.** With the longer window, both the SIF and NDVI
seasonal curves now taper down smoothly through day 350-360 in all three years, with no
sign of the noise or truncation that motivated this fix. More importantly, every single
threshold (90%, 80%, 70%, 60%, and 50% of seasonal peak) now resolves to an actual
crossing date for all three years — the earlier problem of unresolved, missing thresholds
is gone, and the year-to-year comparison can now be made on genuinely equal footing.

**The result, once the comparison is fair, does not support the hypothesis as originally
framed.** Mean lag across all five thresholds came out to 21.6 days for 2015 (drought),
8.4 days for 2018 (drought), and 28.5 days for 2020 (the normal-monsoon comparison year).
Averaged by group, the two drought years show a smaller mean lag (15.0 days) than the
single normal year (28.5 days) — the opposite of what H1 predicted. This is not an
artifact of the earlier truncation problem: with the extended window, 2020's lag at the
70%, 60%, and 50% thresholds forms a smooth, consistently large curve (36.9, 38.9, and
39.5 days respectively) rather than a single anomalous spike, which is what would be
expected if this were still a data-window artifact. The result appears to be genuine.

**An additional complication: the two drought years do not behave alike.** 2015's mean
lag (21.6 days) is roughly two and a half times 2018's (8.4 days), despite both being
documented Marathwada drought years. This suggests that "drought year" as a simple binary
label may be too coarse a category for this analysis — the two droughts likely differed in
onset timing, severity, or duration in ways that matter for this specific comparison, and
a sample of two drought years is nowhere near enough to characterize that variation, let
alone average over it meaningfully.

**What does still hold up.** Across all three years — drought and normal alike — SIF
consistently begins its post-peak decline before NDVI does, with NDVI holding near its
peak value for a longer stretch after SIF has already started dropping. This part of the
finding is robust and replicated three times over, and it supports the project's core
premise: SIF is a more temporally responsive proxy for the onset of physiological decline
than NDVI is. What the data does not support, at least not with this sample, is the more
specific claim that drought stress amplifies this lag relative to a normal season. If
anything, the limited evidence available points the other way, though with only three
years (two drought, one normal) this is far too small a sample to treat as a confident
finding in either direction — it is a genuine, honestly-reported non-result on the
drought-amplification question, not a confirmed contrary finding.

**Status after this entry.** The SIF-leads-NDVI decline pattern is now a solid, three-times
replicated observation for Marathwada, extending across the full growing season through
December. The specific hypothesis that drought years show a larger SIF-NDVI lag than
normal years is not supported by this data, and the two drought years studied differ from
each other by more than either differs from the normal year, which complicates any binary
drought/non-drought framing of this particular comparison. This is being reported as it
stands rather than adjusted to fit the original hypothesis — the honest result here is a
replicated SIF-leads-NDVI pattern with an inconclusive, and possibly contrary, relationship
to drought severity specifically, at this sample size.


# Development Log — Entry 4

**Topic: Catching and fixing a boundary precision problem — from a bounding box to the real Marathwada**

After I had a complete, extended-window lag analysis behind me (June–December, 2015/2018/2020, all fifteen threshold-year combinations resolved), I moved on to what I'd been putting off: actually looking at SIF spatially instead of only as a whole-region average. I built a first script, `map_sif_spatial.py`, to plot the raw clipped SIF rasters for a single day (day-of-year 273, right around the point where the seasonal decline is well underway) side by side for all three years, on a shared colour scale.

The first version of that map genuinely looked good — a visibly concentrated low-SIF (red) patch sitting in the west-southwest part of my study area in 2015 and 2018, and a much greener 2020 panel. That's roughly where I'd expect stress to show up if the underlying idea — that SIF flags drought earlier and more precisely than NDVI — has any spatial coherence to it, not just a temporal one.

But looking at that map made me actually stop and ask a question I should have asked much earlier: what is my study area, exactly? Up to this point, every single script in this project — the GOSIF clipping, the NDVI extraction in Earth Engine, all of it — had been built around one rectangle: 75.0–78.5°E, 17.5–20.5°N. I picked those numbers early on as "roughly Marathwada" and never went back to check them against anything more precise than my own eyeballing of a map.

So I actually opened Earth Engine's Code Editor and added the two lines I'd never bothered to add before — `Map.centerObject()` and `Map.addLayer()` — just to draw that rectangle and actually look at it zoomed in, instead of trusting it blindly. And once I did, the problem was obvious: the box, while covering all eight Marathwada districts, also ate a meaningful chunk of Telangana (parts of Nizamabad, Bidar, and Adilabad districts), touched Solapur, and clipped a corner of Yavatmal. None of those are Marathwada. They also don't share Marathwada's drought history — Solapur and the Telangana districts sit in different rainfall regimes entirely. Every mean SIF and mean NDVI value I had computed up to that point had quietly been an average over Marathwada-plus-a-noticeable-slice-of-somewhere-else, not over Marathwada alone.

I decided this wasn't something I could let go, given how central "this is a Marathwada-specific finding" is to the whole point of this project. A rectangle can never actually match Marathwada's real outline anyway — the region has an irregular shape, with Nanded pushing east and Osmanabad pushing south — so the right fix wasn't to fiddle with the rectangle's corners, it was to stop using a rectangle at all.

I switched to Earth Engine's FAO GAUL 2015 level-2 administrative boundaries dataset, filtered it to Maharashtra state and to the eight district names that make up Marathwada, and merged them into a single precise polygon to replace the rectangle everywhere in the NDVI extraction script.

The first time I ran this, I immediately found a bug in my own fix: when I drew the new polygon, there was a visible gap right where Beed district should have been — the rest of Marathwada filled in correctly, but Beed was just missing. I'd filtered on the district name `'Beed'`, which is the name almost everyone uses today, but the FAO GAUL 2015 dataset — being older — stores this district under its earlier spelling, `'Bid'`. Since my filter string didn't match anything in the dataset, that one district silently dropped out of the geometry, and nothing warned me about it — the script ran without error, it just quietly returned seven districts instead of eight. I only caught it because I happened to look at the map instead of trusting the script's silence. I fixed the name and added an explicit count check (`.size()`) after the filter, printing the number of matched districts, so if this ever happens again with any dataset naming quirk, I'll get a number that's wrong instead of a shape that's wrong and easy to miss.

With the NDVI side fixed and confirmed against an academic reference figure of Marathwada's district boundaries I found online, I still had the SIF side to correct. The GOSIF clipping script had been using `rasterio`'s window-based cropping, which is inherently rectangular — it has no way to represent an irregular polygon boundary. To fix it properly, I exported the same precise Marathwada polygon out of Earth Engine as a GeoJSON, brought it into my local project, and rewrote `clip_gosif.py` to use `rasterio.mask.mask()` against that polygon instead of a bounding-box window. Every pixel that falls outside the real Marathwada district outlines — including everything that used to leak in from Telangana, Solapur, and Yavatmal — is now set to NaN rather than being included in the regional mean.

I re-ran the full chain after that: `clip_gosif.py`, then `aggregate_sif.py`, then `compare_sif_ndvi.py`, then `lag_analysis.py` — all four in sequence, on the corrected boundary, for both datasets.

The result I was bracing for was that the numbers might shift and possibly change my conclusion. That's not what happened. The sanity-check SIF means by year (2015: 0.137, 2018: 0.151, 2020: 0.219) preserved the same drought-vs-normal ordering as before. The seasonal SIF-vs-NDVI trajectories still showed SIF's decline consistently preceding NDVI's decline in all three years. And the lag numbers, while not identical to the earlier (contaminated) run, told the same story: mean lag across thresholds was 24.2 days for 2015, 5.1 days for 2018, and 25.5 days for 2020 — drought-year average (14.6 days) still smaller than the normal year's (25.5 days), so the hypothesis that drought amplifies the SIF-to-NDVI lag is, again, not supported. If anything, the gap between my two drought years (2015 and 2018) came out even more pronounced with the cleaner data than it had with the contaminated rectangle.

I'm treating that as a genuinely useful result rather than a disappointing one. Getting the same qualitative answer from two different, independently-built definitions of the study region — a rough rectangle and a precise administrative boundary — is a real check on whether the earlier finding was actually a signal or just an artifact of sloppy clipping. It held up. That doesn't make the drought-amplification hypothesis correct, but it does mean I can now say with more confidence that its rejection isn't a mistake caused by including the wrong pixels.

What I still don't have: any ground-truth confirmation that the specific low-SIF patch I saw in the spatial map genuinely lines up with cropland rather than some other land-cover class sitting inside the same pixels, and the sample is still only three years, which limits how far I can generalize any of this. Both of those are honest limitations I'm carrying into the next stage rather than papering over.

Next step: regenerate the spatial SIF map using the now-corrected clipped rasters (the underlying files were already overwritten by the boundary fix, so this should just be a re-run, not a rewrite), and then move on to the interactive Folium version.


# Development Log — Entry 5

**Date: 30 July 2026**
**Topic: Verifying the boundary fix actually worked — and fixing the map script itself**

With the boundary-precision correction from the previous entry done — GOSIF re-clipped with the real eight-district polygon instead of a rectangle, NDVI re-extracted the same way — the obvious next step was to regenerate the spatial comparison map for day-of-year 273 across 2015, 2018, and 2020, this time expecting it to visibly show Marathwada's actual irregular outline instead of a plain box.

It didn't. When I reran `map_sif_spatial.py`, the output still looked like a smooth, fully-coloured rectangle, no different in shape from the version I'd made before the fix. That was worrying in a specific way: either the boundary correction hadn't actually taken effect on the raster data, or it had taken effect but the plotting script wasn't showing it. Those are two very different problems, and I didn't want to guess which one I was looking at.

So instead of trusting either a good-looking or a bad-looking picture, I built a small, separate diagnostic script whose only job was to answer that question directly: it opened one clipped SIF file, plotted it, and drew the actual Marathwada boundary polygon as a blue outline directly on top of the same axes, in the same coordinate space. If the coloured data extended past that blue line anywhere, the masking had failed. If it stopped exactly at the line, the masking was correct and the earlier "looks like a rectangle" impression was something else.

The overlay came back clean — the SIF data stopped exactly at the boundary line everywhere, including at the smaller notches and the eastward hook near Nanded. So the clipping fix from the previous entry was genuinely working. That meant the problem was in the map script, not the data.

Looking at `map_sif_spatial.py` again, the reason became obvious: I'd fixed `clip_gosif.py` to mask against the real polygon, but I'd never gone back and updated the multi-panel comparison script to match. It was still displaying each raster using a fixed rectangular extent left over from before the boundary fix, and it never drew the boundary outline at all — so even though the underlying array had the correct NaN pattern outside the real district shapes, nothing in the plotting code made that visible at this scale across three side-by-side panels.

I rewrote the script to pull each raster's own true bounds directly from its file (rather than a hardcoded rectangle) and to draw the same boundary polygon outline on every panel, on top of the shared colour scale and the panel-spacing fix from earlier. I also renamed the output file with a version suffix rather than overwriting the old one silently, the same habit I've been using for the Google Drive exports, so there's no ambiguity later about which image is the corrected one.

The regenerated figure now shows what it should: all three panels display Marathwada's real, irregular outline, data confined exactly within it. The pattern itself held up well under this more careful rendering — 2015 and 2018 both show a distinct, spatially coherent low-SIF zone concentrated in the western edge of Aurangabad district running down through the Latur–Osmanabad belt, while 2020 is overwhelmingly high-SIF (green) across almost the entire region, with only a small patch of lower values in the south.

The lesson I'm taking from this one is less about the map itself and more about process: a figure looking visually plausible isn't the same as it being verified. I could have looked at the first regenerated (still-rectangular) version, decided it was "probably fine since the underlying pipeline was fixed," and moved on — the picture wasn't obviously wrong, it just wasn't showing what it should have been showing. Building the standalone overlay check instead of trusting my own read of the image is what actually caught that the map script itself was the remaining stale piece.

What's still outstanding: this is a single day-of-year snapshot (DOY 273) rather than a full seasonal animation, and the low-SIF zone I'm seeing still hasn't been checked against any actual ground-level drought impact reporting for these districts — it's consistent with what I'd expect from known Marathwada drought geography, but "consistent with expectation" is not the same as "confirmed." Both are worth flagging honestly rather than treating this map as more conclusive than it is.

# Development Log — Entry 6

**Date: 30 July 2026**
**Topic: Bringing in rainfall as an independent, measured driver — validating (and complicating) the drought labels**

Up to this point, "2015 and 2018 were drought years, 2020 was a normal monsoon year" had been a label I was carrying in from general knowledge about Marathwada, not something I had actually measured within this project. Before moving on to writing anything up, I wanted to close that gap, so I brought in CHIRPS daily precipitation data through Earth Engine — the same region, the same June-to-December window I'd been using for SIF and NDVI — and, alongside the three study years, pulled a twenty-year (2001–2020) climatology for the same window so I'd have an actual normal to compare against, rather than comparing the three years only to each other.

The result was a genuine, useful validation: the twenty-year mean was 826.4 mm for the season, with a standard deviation of 158.8 mm. Against that, 2015 came in at 648.9 mm (−21.5% below normal), 2018 at 674.8 mm (−18.3% below normal), and 2020 at 1066.6 mm (+29.1% above normal). So the drought/normal labels I'd been using throughout this project are now backed by measured precipitation deficit, not assumption — both 2015 and 2018 were real, substantial rainfall shortfalls, and 2020 was a genuinely wet year by comparison.

But putting this number next to the SIF-NDVI lag results from earlier made something else visible that I hadn't expected, and I think it's worth recording honestly rather than leaving out because it doesn't simplify the story. 2015's rainfall deficit (−21.5%) and 2018's (−18.3%) are close to each other — a difference of only about three percentage points. But the mean SIF-to-NDVI lag in those same two years was 24.2 days in 2015 versus just 5.1 days in 2018 — nowhere close to each other. If the size of the rainfall deficit were what drove the size of the lag, I'd expect these two similarly-dry years to produce a similarly-sized lag, and they don't. Whatever is producing the very different lag behaviour between these two drought years, it isn't simply explained by how much rainfall was missing that season.

I'm treating this as an honest limitation to state plainly rather than something to explain away. It's possible the answer is about timing within the season (a deficit concentrated early versus late in the monsoon could affect the SIF-NDVI relationship very differently even at the same total shortfall), or about the starting soil moisture condition heading into each season, or about something else this dataset doesn't capture at all. I don't have the data in this project to test any of those explanations yet, and I'm not going to guess at one just to make the story tidier.

What this rainfall addition does give me, concretely: the drought-year framing that runs through this entire project is no longer just inherited knowledge, it's independently measured within the same pipeline as everything else. And the finding that "drought amplifies the SIF-NDVI lag" is not supported still stands, now on a firmer footing — with actual rainfall data in hand, it's clear this isn't a case of one of my "drought years" secretly not being that dry after all.

# Development Log — Entry 7
**Topic: Mapping rainfall the same way I mapped SIF — and seeing how well the two match up spatially**

With the district-level rainfall anomaly numbers already validated at the regional level, I wanted the same kind of spatial view for rainfall that I'd already built for SIF — not just a single number per district printed in a table, but something visual, and something that let me directly compare where the rainfall deficit sat against where the SIF stress showed up.

I built this in three layers, matching the pattern I'd already established for SIF. First, an interactive Folium choropleth — each of the eight districts colored by its rainfall anomaly percentage, with a layer for each of the three years, hoverable and clickable, matching the same style as the SIF-by-district Folium map. Second, a static version of the same thing using GeoPandas and matplotlib — three panels side by side, one per year, with each district's exact anomaly percentage labeled directly on the map, meant for the paper rather than the browser.

The two on their own already told a clear story. In 2015, the western and southern districts — Aurangabad, Bid, Jalna, Latur, and especially Osmanabad — all showed rainfall well below normal, while Hingoli and Nanded in the east were only mildly below normal. In 2018, that same west-to-east pattern showed up again, but sharper: Aurangabad and Bid were both more than 35% below normal, while Hingoli and Nanded actually had a rainfall surplus that year. That's worth sitting with for a second — the region-wide number I'd computed earlier called 2018 an 18% deficit year, and that's true on average, but it hides that the deficit was almost entirely concentrated in the west and south, while the east was doing fine or better. "Drought year" as a single label for the whole region flattens something that was actually quite unevenly distributed on the ground.

The third piece was the one I actually wanted from the start: a combined figure with SIF on top and rainfall anomaly underneath, same three years, side by side, so the two could be read against each other directly instead of me trying to hold both maps in my head at once. Putting them together made the spatial correspondence obvious in a way the separate maps didn't quite manage — the deep red, low-SIF zone in the southwest in 2015 and 2018 sits almost exactly on top of the deep red, rainfall-deficit zone in the same two maps, and the same districts that turned green with rainfall surplus in 2020 are the same ones that turned green with healthy SIF that year. Nanded, which barely dipped in rainfall in either drought year, is also the district that stayed comparatively green in SIF in both of those years. That's a genuinely reassuring, physically coherent picture — two independently measured satellite products (a fluorescence signal and a precipitation product, from entirely different sensors) pointing at the same places for the same reasons.

Building the combined figure surfaced a small but real presentation bug: the overall figure title and the six individual panel titles were rendering too close together, visually merging into each other. I fixed the spacing by giving the subplot grid more headroom (reducing how much of the figure height the panels themselves occupy) and adding explicit padding to each panel's own title, rather than just nudging the suptitle position by itself — the two titles need separated space, not just separated coordinates.

What I'm not claiming from this: visual correspondence between two maps, however striking, is not a statistical test. I haven't run any actual correlation or regression between district-level rainfall anomaly and district-level SIF across the three years — with only three years and eight districts, that would be a weak analysis anyway (an n of 24 district-year pairs, but not independent since districts within a year are spatially correlated with each other). What I have is a visual, physically-motivated consistency check, and I'm describing it as exactly that and nothing stronger.

