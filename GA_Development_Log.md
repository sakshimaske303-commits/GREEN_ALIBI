# GREEN ALIBI — Development Log

This is my working log for GREEN ALIBI. I am testing whether Solar-Induced Fluorescence (SIF), which is tied to photosynthesis, catches crop drought stress earlier than NDVI, the greenness index that India's drought monitoring relies on. The entries are in the order I wrote them, one per phase of the work: framing the research question, building the SIF and NDVI pipelines, fixing the study boundary, bringing in rainfall, adding a second lag method, reviewing my own code, extending the study from 3 years to 9, and finally to an out-of-sample test on 2001–2014. Each entry records what I found and decided at the time, including results that did not support my hypotheses and errors I later corrected.

> **Note on numbers.** Entries are kept as written at the time, so earlier entries contain numbers that were later corrected or reinterpreted. Entries 24–27 describe the current state: the seasonal lead depends on how each curve is normalised and, for GOSIF, is shared with NIRv; the methods were tested unchanged on 2001–2014; district drought is classified against each district's own rainfall baseline (15 drought district-years, not 17); Trigger-1 dry spells are counted only within the monsoon; and the district alarm comparison was corrected in Entry 27, so the district alarm counts in Entries 24–26 are superseded. Where an earlier entry disagrees with Entries 24–27 or `GA_Research_Paper.md`, the later one holds.

## Index

1. [Entry 1](#entry-1)
2. [Entry 2](#entry-2)
3. [Entry 3](#entry-3)
4. [Entry 4](#entry-4)
5. [Entry 5](#entry-5)
6. [Entry 6](#entry-6)
7. [Entry 7](#entry-7)
8. [Entry 8](#entry-8)
9. [Entry 9](#entry-9)
10. [Entry 10](#entry-10)
11. [Entry 11](#entry-11)
12. [Entry 12](#entry-12)
13. [Entry 13](#entry-13)
14. [Entry 14](#entry-14)
15. [Entry 15](#entry-15)
16. [Entry 16](#entry-16)
17. [Entry 17](#entry-17)
18. [Entry 18](#entry-18)
19. [Entry 19](#entry-19)
20. [Entry 20](#entry-20)
21. [Entry 21](#entry-21)
22. [Entry 22](#entry-22)
23. [Entry 23](#entry-23)
24. [Entry 24](#entry-24)
25. [Entry 25](#entry-25)
26. [Entry 26](#entry-26)
27. [Entry 27](#entry-27)

## Entry 1

I am running GREEN ALIBI as an independent satellite study. The main goal is to test whether Solar-Induced Fluorescence (SIF), which is closely linked to photosynthesis, picks up crop drought stress earlier than NDVI, the greenness index that India's drought monitoring uses. NDVI is a reflectance index. It measures how much visible and near-infrared light the canopy reflects, so it changes only once the canopy has started to thin, and by then much of the damage is done. SIF tracks something earlier. When a plant absorbs sunlight, a small part of that energy is not used for photosynthesis and is given off again as fluorescence, and the size of that part depends on the quantum yield of photosynthesis. Under stress the plant's internal efficiency drops before its greenness changes, so SIF should drop before NDVI does. That was the idea I set out to test: NDVI can give a stressed crop a green alibi, while SIF should show what is happening inside the leaf.

India's drought declarations, and the crop-insurance payouts under the Pradhan Mantri Fasal Bima Yojana, depend on rainfall deficits and NDVI-based satellite checks. Both respond only after crops are visibly damaged, so recognition comes late, and so does the money that farming families need most during the dry period. I want to treat this delay as a question to test, not something to assume. The data goal is to check whether SIF catches plant stress before NDVI, and whether the lag is large and consistent enough to matter. If it is, that would be a physical case for updating the warning tools. If it is not, that is worth knowing too.

The plan is to use satellite SIF and NDVI over drought-affected farming districts in India, measure the timing difference, and check whether the lag would give useful early warning for drought declarations and crop insurance. This gives four research questions. RQ1: does SIF drop measurably earlier than NDVI during documented drought onset in the study region? RQ2: is the SIF–NDVI lag the same across districts and crop types, or does it vary with geography and crop physiology? RQ3: how does the timing of SIF-based stress onset compare with official state drought declaration dates for the same districts and years? RQ4: does the SIF–NDVI lag give an early warning window, in weeks, that matters for crop insurance and drought relief timelines?

I had three hypotheses before starting. H1: SIF drops significantly earlier than NDVI during the same dry spell, because fluorescence responds to a fall in photosynthetic efficiency before any visible change in leaf colour. H2: the size and timing of the SIF–NDVI difference varies between crop types, because fluorescence depends on canopy structure and photosynthetic pathway. H3: official drought declarations come well after the SIF stress signal, because the official process relies on rainfall gauges and greenness indices and not on direct measures of plant function. I will check all three when I have numbers.

The first step is choosing a study area with a well-documented drought history and good official records. The candidates are Marathwada and Vidarbha in Maharashtra, and Bundelkhand across Uttar Pradesh and Madhya Pradesh, since all of them have regular, well-reported droughts. For SIF I plan to use either the gridded GOSIF product or TROPOMI, because SIF instruments in space are not designed to resolve single fields anyway. For NDVI I need MODIS or Sentinel-2 data over the same districts and time windows. I also need official drought declaration documents and, if possible, PMFBY payout timing records as the policy benchmark. I have no data yet; this entry is only the starting point. Download scripts come next.

## Entry 2

Next I built the actual pipeline: find SIF data, find matching NDVI, and make the first comparison for Marathwada.

I chose Marathwada as the study region. It is my home region, and it has a well-documented drought history. I picked three years and the window from 1 June to 1 November (day of year 153 to 305), which covers the main Kharif season. 2015 and 2018 are documented drought years, 2015 being the year of the Latur water crisis, when water had to be brought in by train. 2020 was a fairly normal monsoon and serves as the baseline.

For SIF I used GOSIF v2, a global 0.05-degree, 8-day SIF product built from OCO-2, MODIS and weather reanalysis by Li and Xiao at the University of New Hampshire. It is the most practical choice, since the SIF instruments themselves are not made for field-scale work. I downloaded 60 8-day GeoTIFFs, 20 for each of 2015, 2018 and 2020.

**Clipping and scaling.**

I wrote a Python script that crops each global file to a Marathwada bounding box, 17.5°N to 20.5°N and 75.0°E to 78.5°E, which covers all 8 districts. Raw values are multiplied by the 0.0001 scale factor to get SIF units, and two fill values are masked first: 32766 (water) and 32767 (non-vegetated or missing). These fill values are far outside the real SIF range, so leaving them in would ruin any average. A second script averages each clipped image into one regional mean per date and records the fraction of valid pixels at each time step as a quality check.

Then I hit a cloud masking bug in the NDVI code. I first took NDVI from the MOD09Q1 8-day surface reflectance product in Google Earth Engine, to match GOSIF's 8-day timing. The first version computed NDVI straight from the bands with no cloud mask, and the series was far too noisy. In 2020 it went from about 0.55 down to 0.14 and back up to 0.60 within consecutive 8-day windows, which cropland cannot do. The SIF series over the same period was smooth and made sense, so the problem was in my NDVI script and not in the crops. The cause was cloud and cloud-shadow contamination. The Kharif season is the monsoon, and MOD09Q1 does not reliably drop cloudy pixels without explicit quality filtering.

The fix was to rebuild the NDVI extraction around MOD13Q1, NASA's 16-day vegetation index product, which uses a maximum value composite to reduce cloud effects. Its SummaryQA band (0 good, 1 marginal, 2 snow or ice, 3 cloudy) let me keep only good and marginal pixels. I also added a cropland mask from MCD12Q1 (IGBP classes 12 and 14), so that forest, urban and barren pixels do not dilute the crop signal. This means giving up 8-day resolution for 16-day, but the 16-day curve is smooth and makes physical sense, and a clean 16-day series is more useful than a noisy 8-day one.

A second, smaller bug: Earth Engine gave the error `Image.clip: Can't transform (0.0,0.0)` because I was clipping a combined image made of two layers at different native resolutions, 250m NDVI and the 500m cropland mask. `reduceRegion()` already limits the calculation to the geometry, so the `.clip()` was not needed. Removing it fixed the error.

**Merging 2 time series at different temporal resolutions.**

SIF is 8-day and the cleaned NDVI is 16-day, so the dates do not line up. I joined them by nearest date within each year, so each 8-day SIF value is paired with the closest 16-day NDVI value.

There was also a labelling bug. An early version of the comparison plot labelled 2018 as a normal year, because only 2015 had been flagged as a drought year in the plotting code. I fixed it before drawing any conclusions from the chart.

Then the first seasonal comparison. I plotted SIF and NDVI for all three years. In each year SIF starts to fall from its seasonal peak before NDVI does, and NDVI stays near its peak for longer after SIF has started dropping. The pattern repeats in all three years and fits the idea that SIF responds earlier to the post-peak decline.

I also have to correct something I claimed too quickly. Looking at the three charts, I first said the lag was larger in the drought years, 2015 and 2018, than in 2020. To check, I calculated each year's drop as a percentage of its own peak at every later date. The numbers did not support it. The lag was roughly 15 to 25 days in all three years, and drought did not make it bigger. I am taking that claim back here. What I can say is that SIF's decline leads NDVI's in general. To test whether drought changes the lag, I need a proper lag measure, such as a day-of-year threshold method or cross-correlation, instead of reading curves by eye. That is the next task.

**Status after this entry.**

Both pipelines are built. SIF and NDVI are quality-screened and cropland-masked for 2015, 2018 and 2020 over Marathwada. SIF leads NDVI in all three years, but I cannot report that as a result until a numeric lag calculation replaces the visual comparison. I would also like at least 1 more year, since three years is a very small sample.

## Entry 3

Entry 2 ended with an open problem. My first quantitative lag script compared how many days after its own peak SIF and NDVI each crossed a set of decline thresholds, but the results could not be trusted. The window, 1 June to 1 November, ended before NDVI had finished declining in 2 of the 3 years. Several thresholds never got a crossing date at all, and the ones that did were averaged unevenly across years, so the drought-versus-normal comparison was unreliable. I dropped that first check.

The fix was a longer window. I added 7 more 8-day GOSIF periods, day of year 313, 321, 329, 337, 345, 353 and 361, for all three years, which moves the cutoff from 1 November to late December. The clipping and aggregation scripts from Entry 2 picked up the 21 new files without any code change, because they read whatever files are in the raw data folder instead of assuming fixed dates. I also moved the NDVI end date from 1 November to 31 December and reran the same MOD13Q1 cloud-screened, cropland-masked extraction.

With the longer window both curves taper smoothly through day 350 to 360 in all three years, the truncation is gone, and every threshold from 90%, 80%, 70%, 60% down to 50% of the seasonal peak now has a crossing date in every year. So the years can be compared on the same footing.

The results did not support H1 as I had framed it. The mean lag over the 5 thresholds was 21.6 days for 2015 (drought), 8.4 days for 2018 (drought) and 28.5 days for 2020 (normal). The two drought years average 15.0 days, against 28.5 days for the normal year, which is the opposite of what H1 predicted. This is not left over from the old window problem. With the extended window, 2020's lag at the 70%, 60% and 50% thresholds is 36.9, 38.9 and 39.5 days, a smooth and consistent pattern, while a window error would show up as one odd value. The result looks real.

There is another complication. The two drought years are very different: 2015's mean lag of 21.6 days is about 2.5 times 2018's 8.4 days, even though both are documented drought years. A simple drought or no-drought label is too coarse for this. The two droughts probably differed in onset timing, severity or duration in ways that matter here. Two drought years are not enough to describe that variation, let alone average over it, so I need more years.

The main pattern still holds. In all three years, drought and normal, SIF starts its post-peak decline before NDVI, and NDVI stays near its peak for longer after SIF has started to drop. This supports the main premise that SIF responds earlier than NDVI to the start of the decline. But this sample does not support the more specific claim that drought makes the lag larger. If anything, the little evidence I have points the other way, but with 2 drought years and 1 normal year that is too small a sample for a conclusion in either direction. I am treating the drought amplification question as a non-result for now.

**Status after this entry.**

The SIF-leads-NDVI pattern holds in all 3 years for Marathwada, over the full season through late December. The idea that drought years show a larger SIF–NDVI lag is not supported. The 2 drought years differ from each other by more than either differs from the normal year, which makes a simple drought versus non-drought comparison hard to use. So the result is a repeated SIF-leads-NDVI pattern with no clear link to drought severity at this sample size.

## Entry 4

With the extended June to December lag analysis done for 2015, 2018 and 2020, and all 15 threshold-year combinations resolved, I moved on to a task I had been putting off: looking at SIF spatially and not only as one regional average. I wrote map_sif_spatial.py to plot the clipped SIF rasters for day of year 273, when the seasonal decline is well under way. The 3 years are shown side by side on one shared colour scale, so the comparison is fair.

The first map showed a clear low-SIF patch (dark red) in the west-southwest of the study area in 2015 and 2018, while 2020 was much greener. That is roughly where I would expect drought stress if the signal is coherent in space as well as in time.

But the map made me ask a basic question I should have asked much earlier: what exactly is my study area? Until now every script, the GOSIF clipping and the NDVI extraction in Google Earth Engine, used one rectangle, 75.0–78.5°E and 17.5–20.5°N. I picked those limits at the start from a general map and never checked them against real boundaries.

In the Earth Engine Code Editor I added `Map.centerObject()` and `Map.addLayer()` to draw the rectangle. The problem was clear. The box covered all 8 Marathwada districts, but also a large part of Telangana (parts of Nizamabad, Bidar and Adilabad), part of Solapur and a corner of Yavatmal. None of these are in Marathwada, and Solapur and the Telangana districts have different rainfall regimes. So every mean SIF and NDVI value so far included a large area from outside the region.

I had to fix this, because the study is about Marathwada. Adjusting the rectangle would not help, since Marathwada has an irregular shape, with Nanded extending east and Osmanabad south. The right fix was to use the actual district boundaries.

I switched to Earth Engine's FAO GAUL 2015 level-2 boundaries, filtered them to Maharashtra, selected the 8 Marathwada district names, and merged them into one polygon that replaces the rectangle in the NDVI script.

My first run of this had a bug. There was a gap where Beed should be. I had filtered on the current name 'Beed', but GAUL 2015 uses the older spelling 'Bid', so nothing matched. The script ran without errors and simply returned 7 districts instead of 8. I only noticed because I looked at the map. I fixed the name and added a `.size()` count right after the filter, which prints the number of matched districts, so a naming problem like this will show up as a wrong count next time.

The NDVI boundary was done first, and it matches a published reference map of Marathwada's districts. The SIF side needed more work. The old GOSIF clipping script used rasterio's window-based cropping, which can only cut rectangles. I exported the Marathwada polygon from Earth Engine as a GeoJSON file and rewrote clip_gosif.py to use `rasterio.mask.mask()` with that polygon. Every pixel outside the district outlines is now NaN, so Telangana, Solapur and Yavatmal no longer enter the averages.

I then reran the whole chain in order, clip_gosif.py, aggregate_sif.py, compare_sif_ndvi.py and lag_analysis.py, with the new boundaries.

I expected the conclusion might change, but it did not. Mean SIF by year was 0.137 for 2015, 0.151 for 2018 and 0.219 for 2020, the same drought-versus-normal order as before. The seasonal curves still show SIF declining before NDVI in all 3 years. The lags changed a little but tell the same story: 24.2 days for 2015, 5.1 days for 2018 and 25.5 days for 2020. The drought-year average of 14.6 days is still well below the normal year's 25.5 days, so H1 is again not supported. The difference between 2015 and 2018 is even larger with the correct boundary than with the rectangle.

This is a useful check. Two independently built study areas, a rough rectangle and the actual district boundary, give the same qualitative answer, so the earlier result was not caused by the clipping. It does not make the drought amplification hypothesis right. It does mean that rejecting H1 is not a side effect of including the wrong pixels.

Some gaps remain. I have no ground data to confirm that the low-SIF patch on the map is cropland and not some other land cover in the same mixed pixels. And the sample is still only 3 years, which limits how far any of this can be generalised.

Next step: regenerate the spatial SIF map from the corrected rasters, which the boundary fix has already overwritten. That only needs the existing script to be rerun. After that I will build the interactive Folium version for the dashboard.

## Entry 5

With the GOSIF layers re-clipped to the 8-district polygon and NDVI re-extracted the same way in Earth Engine, I regenerated the day-273 spatial map for 2015, 2018 and 2020, expecting to see Marathwada's real outline. It did not change. The map from map_sif_spatial.py still looked like a fully filled rectangle, the same as the old run.

There were 2 possibilities. Either the boundary fix had not changed the raster data, or the clipping worked and the plotting script was not showing the masked areas. I did not want to guess.

So I wrote a small separate diagnostic script. It opens one clipped SIF layer, plots it, and draws the Marathwada boundary polygon as a blue outline on the same axes. If coloured pixels appear outside the blue line, the clipping failed. If they stop exactly at the line, the clipping is correct and the rectangle comes from somewhere else.

The overlay was clean. The pixels stop exactly at the boundary everywhere, including the small notches and the eastward extension near Nanded. So the clipping fix from the last entry works on the raster data, and the problem was in the plotting script.

In map_sif_spatial.py I found that, after fixing clip_gosif.py, I had never updated the plotting script. It still used a fixed rectangular extent from the bounding-box version and never drew the district boundaries. The NaN mask outside the districts was in the data, but nothing in the plot made those areas show as empty, so the 3 panels looked like full rectangles.

I rewrote the script to take each raster's real extent from its metadata instead of a hardcoded rectangle, and to draw the boundary outline on every panel, keeping the shared colour scale and the panel spacing fix from earlier. I also saved the output under a new version suffix and did not overwrite the old image, the same habit I use for my Google Drive exports, so it is clear which figure is the corrected one.

The new figure shows Marathwada's real outline in all 3 panels, with data only inside the districts. The pattern itself did not change. In 2015 and 2018 there is a clear, spatially coherent low-SIF zone along the western side of Aurangabad district and down through the Latur–Osmanabad belt. In 2020 almost the whole region has high SIF, with only a small lower patch in the far south.

A note for my workflow: a figure that looks plausible is not a verified figure. I could easily have accepted the rectangular version because the processing had already been fixed. It did not look broken, it just was not showing what it should. The separate overlay test is what showed that the map script was the last outdated piece. I now check outputs against an independent overlay.

Two gaps remain. The map is a single snapshot (DOY 273), not a time series through the season. And the low-SIF zone has not been checked against ground-level drought reports from district offices. It matches what I would expect from Marathwada's drought geography, but matching expectations is not the same as being confirmed by field data, so I am not treating this map as more than it is.

## Entry 6

Until now I had taken the usual description that 2015 and 2018 were drought years and 2020 a normal monsoon, without checking the numbers myself. Before writing the final report I downloaded CHIRPS daily rainfall in Earth Engine for the same Marathwada area and the same June to December window as the SIF and NDVI work. I also pulled 20 years, 2001 to 2020, as a climatology, because comparing the 3 study years only with each other says nothing about what a normal year looks like.

The 20-year mean for the season is 826.4 mm (standard deviation 158.8 mm). 2015 had 648.9 mm, 21.5% below normal. 2018 had 674.8 mm, 18.3% below normal. 2020 had 1066.6 mm, 29.1% above normal. So the drought and normal labels I was using are now backed by my own data: 2015 and 2018 had large rainfall deficits and 2020 was a wet monsoon year.

Putting these next to the lag results shows something that does not fit a simple story. The rainfall deficits in 2015 (-21.5%) and 2018 (-18.3%) are only about 3% apart, but the mean SIF–NDVI lag was 24.2 days in 2015 and 5.1 days in 2018. If the size of the rainfall deficit drove the lag, these 2 dry years should have similar lags, and they do not. Whatever makes the lag differ between the two droughts, it is not the total monsoon deficit.

I am recording this as a limitation. It could be the timing of the rainfall failure (missing rain in early June and missing rain in late September could affect SIF and NDVI differently even with the same seasonal total), soil that was already dry from the previous year, or something else that is not in my data. I cannot test these ideas with what I have.

The rainfall check still helps. The drought-year labels now come from my own calculation with the same setup, not from news reports. And the earlier conclusion that drought does not make the SIF–NDVI lag larger now rests on actual CHIRPS numbers, which confirm that both drought years really had poor rainfall.

## Entry 7

After checking the district rainfall numbers, I wanted a map of the rainfall data like the SIF maps, so I could see where the rain failed and compare it with where SIF was low. A table with 1 number per district does not show the geography.

I made the maps in 3 steps. First, an interactive Folium choropleth that colours the 8 districts by rainfall anomaly, with toggles for each of the 3 years, so it can be explored in a browser. Second, a static GeoPandas and matplotlib version with the 3 years side by side and the anomaly value written inside each district, which works better for the paper.

These 2 maps make one point clear. In 2015 the western and southern districts (Aurangabad, Bid, Jalna, Latur and especially Osmanabad) had much less rain than normal, while Hingoli and Nanded in the east were close to normal. In 2018 the same west–east split appeared, more strongly. Aurangabad and Bid had deficits beyond 35%, while Hingoli and Nanded got more rain than normal. The regional figure for 2018, an 18% deficit, is correct, but it hides the fact that the drought was mostly in the west and south and the east was close to normal. Calling the whole region a drought year oversimplifies an uneven situation.

The third map was the one I had planned from the start: SIF in the top row and rainfall anomaly in the bottom row for all 3 years, so both patterns can be compared directly. The low-SIF area in the southwest in 2015 and 2018 sits over the largest rainfall deficits in the same years, and the areas with extra rain in 2020 are the same ones with high SIF.

Nanded is a good example. Its rainfall barely dropped in either drought year, and its SIF stayed higher than in the other districts in both 2015 and 2018. That is reassuring, because two separate satellite products, one measuring a faint plant emission and the other estimating rainfall from different sensors, point to the same places for the same reasons.

There was one layout bug. In the combined figure the main title and the 6 panel titles overlapped. Moving the main title up did not help, so I made the maps slightly smaller to leave room at the top and added title padding to each subplot.

These maps are not a statistical test. I did not calculate a correlation or regression between district rainfall deficits and SIF across the 3 years. It would not mean much anyway: there are only 24 pairs (8 districts over 3 years), and they are not independent, because neighbouring districts in the same monsoon share the same weather. So the maps are a visual consistency check, and I will describe them that way.

## Entry 8

Entry 7 ended with a limitation: the SIF and rainfall maps were only a visual match, with no statistical test. I did not want to leave that open, so I ran the numbers.

I merged `sif_by_district.csv` and `rainfall_anomaly_by_district.csv` from `data/processed/` on year and district, which gives 24 rows (8 districts times 3 years). I ran a Pearson correlation for a linear relationship and a Spearman rank correlation in case the relationship is not linear.

Pearson r was 0.837 (p < 0.001) and Spearman rho was 0.857 (p < 0.001). Both show a clear positive relationship: where and when rainfall is lower, SIF is lower.

The independence problem from Entry 7 still applies. 24 rows looks like a reasonable sample, but the 8 districts in one year are not independent, because they are neighbours and share the same monsoon. The effective number of independent cases is closer to 3 (1 per year) than to 24. I am reporting the correlation as computed, with that caveat.

This puts a number behind the visual check from Entry 7. It does not change the result from Entries 3, 4 and 6 that a worse drought does not simply increase the SIF–NDVI lag. The correlation is about SIF and rainfall matching across places and years, which is a different question from the timing lag, and I am keeping the 2 separate.

## Entry 9

Rereading the Physical Basis section of my paper, I noticed something about GOSIF that I had written down but not thought through. GOSIF is not a direct measurement from a single satellite. It is a statistical model that takes sparse OCO-2 SIF soundings and fills the gaps using MODIS reflectance and weather reanalysis. That description is correct. What I had not written down is what it means here: the MODIS reflectance that GOSIF uses to fill the gaps between OCO-2 passes is also the source of the NDVI I am comparing it with.

So in this study SIF and NDVI are not fully independent. Wherever OCO-2 has no direct sounding, the GOSIF value is predicted partly from the same MODIS data that gives the NDVI. This does not mean the SIF-before-NDVI result is wrong, and it does not mean GOSIF is a poor product. It is widely used because OCO-2 soundings alone are too sparse to cover a region like Marathwada. But part of the shared signal between the 2 variables comes from the choice of product. I do not have the time or data right now to work out how much of the lag is plant physiology and how much comes from this shared input.

I am recording this as a limitation.

## Entry 10

Since Entry 3 I have reported the large difference between the 2015 lag (24.2 days) and the 2018 lag (5.1 days), but rereading my draft today I saw that I never tried to explain it.

I cannot prove the reason with my current data, but I can list possible ones. Both years had almost the same rainfall deficit, so if total water loss drove the lag, the two lags should be similar, and they are not. There are 3 possible explanations, none of which I can test right now. The rain may have failed early in June in one year and late in September in the other. NDVI's 16-day sampling may have caused a timing error in 1 of the years. Or farmers may have grown different crops in the 2 seasons. I have no crop calendars or sowing data to check these, so I am recording them as 3 open possibilities and not choosing one.

## Entry 11

I went back through the raw data files, not only the text, and found another error.

Since Entry 4, `data/processed/clipped/` has held 2 files for every date: the old rectangle crop, `GOSIF_<year><doy>.tif`, from the first script, and the correct polygon-masked file, `GOSIF_<year><doy>_clipped.tif`. Having both is fine in itself. But `aggregate_sif.py` searched for `"GOSIF_*.tif"` and then filtered names with the regex `r"GOSIF_(\d{4})(\d{3})\.tif"`. That regex expects `.tif` straight after the date, so every `_clipped.tif` file failed it and was skipped without any warning, while the old rectangle files matched. So `marathwada_sif_timeseries.csv` had been built from the unclipped data all along, even though I thought the fixes in Entries 4 and 5 had updated everything.

I missed this in Entry 4. The yearly SIF means I reported there as a check, 0.137 for 2015, 0.151 for 2018 and 0.219 for 2020, are correct values for the old rectangle files. My check was comparing the old data with itself, because the script never read the new files.

The district-level results were not affected. `zonal_stats_sif.py`, which I used for the district maps and the SIF–rainfall correlation, names the `_clipped.tif` files directly instead of using a glob pattern. So the Pearson 0.837, the Spearman 0.857 and the district maps were correct.

I changed `aggregate_sif.py` to search for `GOSIF_*_clipped.tif` with the regex `r"GOSIF_(\d{4})(\d{3})_clipped\.tif"`, so it loads only the polygon-clipped outputs from `clip_gosif.py`, whatever else is in the folder. Then I reran the analysis and regenerated `marathwada_sif_timeseries.csv`, `marathwada_sif_ndvi_merged.csv`, `sif_ndvi_lag_by_threshold.csv` and `final_summary_rainfall_lag.csv`, and the 2 main figures, `sif_vs_ndvi_seasonal_v2.png` and `sif_ndvi_lag_by_threshold.png`.

The main results did not flip. The corrected lags are 24.3 days for 2015, 6.9 days for 2018 and 28.7 days for 2020 (previously 24.2, 5.1 and 25.5). The drought-year mean went from 14.6 to 15.6 days, and the normal year from 25.5 to 28.7 days. SIF still declines before NDVI in all 15 threshold-year combinations. Drought years still have a shorter lag than the normal year, so H3 is still rejected. The biggest change is 2018, from 5.1 to 6.9 days, about 35%, which matters because it is the smallest lag in the study.

The old rectangle files are still in `data/processed/clipped/`. I am leaving them for now as a record of what the bug was reading, but they have to be deleted before the GitHub repository is final. Their presence is why this bug stayed hidden, and any new script with a loose `GOSIF_*.tif` pattern would pick them up again.

## Entry 12

Every lag value so far, including after the Entry 11 fix, comes from one method, threshold crossing. That method mainly captures when the decline starts, especially at the 90% and 80% thresholds, and it cannot tell me whether the results hold if the question is asked another way. So I wanted a second method.

I used time-lagged cross-correlation. I rescaled SIF and NDVI to 0-1, kept only the decline after the peak, put both on a daily grid, removed the mean, and found the shift that gives the highest correlation. This asks a different question. It does not look for when the decline starts, but for the single shift that best matches the whole shape of the 2 curves. If both methods agree, the result is more reliable.

I caught a problem in the first run. I allowed lags up to 60 days, and 2 of the 3 years had their peak close to that limit (2020 peaked at day 56 of 60). This is a known artefact. At lags close to the length of the series, too few days overlap, so the peak reflects the edge of the search window and not a real best match. I capped the maximum lag at N/4 of the decline period, a standard rule, which is about 32 days here, and reran. The peaks for all 3 years now sit well inside the search range.

The best lags were 13 days for 2015, 4 days for 2018 and 7 days for 2020. All 3 are positive, with peak correlations of 0.99, 0.99 and 0.99, and none sits at the search limit. So this second method also shows SIF declining before NDVI in all 3 years, which supports H1.

Not everything matched. The threshold method ranks the lags 2020 (28.7 days), 2015 (24.3 days), 2018 (6.9 days). Cross-correlation ranks them 2015 (13 days), 2020 (7 days), 2018 (4 days). Both put 2018 lowest, but they disagree on whether 2015 or 2020 has the largest lag, which is exactly the comparison H3 depends on. So the direction, SIF before NDVI, is supported by 2 methods, but the exact day counts and the ranking of years are uncertain, because 2 reasonable methods give different orders. The paper says both.

The threshold numbers stay as they are. Cross-correlation is an additional check, not a replacement.

## Entry 13

Once the paper draft and logs were stable, I went back through the code the way a reviewer would, without treating "it runs and the numbers look right" as the end. I found four gaps: no uncertainty estimates for the lags; the non-independence of the district correlation was stated but never measured; the Google Earth Engine data acquisition was not scripted; and RQ3 had never been answered in the paper. This entry records how I handled each one, including an approach that did not work.

My first bootstrap attempt failed. I ran a moving block bootstrap on the interpolated daily SIF and NDVI series, cutting each year's decline curve into overlapping 10-day blocks, resampling them with replacement, recomputing the cross-correlation lag, and repeating this 2,000 times. Every confidence interval came out as [0.0, 0.0]. That is not a narrow interval, it is a broken result, and reporting it as "exactly zero, plus or minus nothing" would have been wrong.

The reason is that the decline curves are strongly non-stationary: they trend downward through the whole season. Shuffling blocks of a trending series destroys the trend, so the resampled series no longer looked like a decline curve and the cross-correlation was picking up noise around zero lag. I was measuring what happens when the signal is removed, not the uncertainty in the signal.

So I switched to case resampling. Instead of shuffling points on the daily grid, I resampled which of the original 17 8-day observations go into each year's curve, with replacement, then re-interpolated and reran the cross-correlation from Entry 12. This keeps the shape of the decline in every replicate and captures a real source of uncertainty: during the monsoon you do not know in advance which overpass dates will be cloud-free.

The results: 2015, 13 days (95% CI 5 to 20); 2018, 4 days (0 to 9); 2020, 7 days (0 to 32). Every pair of years overlaps, so the ranking discussion from Entry 12 is not something the data can support with confidence. The direction holds. The lag was non-negative in 100% of replicates for every year and strictly positive in 84.5% to 99.9% of them. So this strengthens H1 and at the same time weakens confidence in the exact day counts. The paper reports both, instead of single point estimates that look more precise than they are.

Next, a spatial test. The paper had always said that the 24 district-year observations behind r = 0.837 are not independent because the 8 districts are neighbours, but I had never measured it. I built a Queen contiguity weights matrix from the FAO GAUL district polygons (a mean of 3.25 neighbours per district) and ran Moran's I with a 9,999-permutation test for mean SIF and for rainfall anomaly, separately for each year.

All 6 year-by-variable combinations were significant (p below 0.05), with I from 0.26 to 0.55 against an expected value of −0.14 under spatial randomness. This does not change the correlation coefficient, and the spatial pattern itself is real and consistent with the SIF maps in Section 4.3. It does mean I can now state that the effective sample size is closer to 3 than to 24, based on a measurement.

Then the Earth Engine script. The NDVI, cropland mask and CHIRPS rainfall extractions had all been run by hand in the Earth Engine Code Editor from the start of the project, and every version of my Limitations section said so. I wrote src/acquisition/gee_data_acquisition.py using the earthengine-api and geemap packages. It rebuilds what Section 3.1 of the paper describes: SummaryQA-filtered MOD13Q1, the MCD12Q1 cropland mask (classes 12 and 14), CHIRPS seasonal totals and the 20-year climatology, all over the FAO GAUL Marathwada polygon.

This file has limits. I do not have an authenticated Earth Engine account on the machine I was using, so I have not run it and cannot confirm that it reproduces my original Code Editor output. What it does is turn a manual step described only in prose into a version-controlled script that anyone with Earth Engine access can run and check. I wrote this distinction into the Limitations section, so the file does not suggest more than it does.

Last, RQ3. The research questions in GA_Project_Report.md framed the policy motivation partly around the official drought declaration timeline, not only the rainfall deficit, but section 4 of GA_Research_Paper.md never ran that comparison. The old section 3.5 compared against the rainfall deficit only. I searched for verifiable Maharashtra drought declaration dates for each study year. For 2018 it was straightforward: the state declared drought in 151 talukas across 26 districts, including all 8 Marathwada districts, on 31 October 2018, as reported by Zee News and EPW that week.

For 2015 I could not find a clear single date. Coverage of the 2015 Marathwada drought is dominated by reporting on the 2016 Latur water crisis, not a dated 2015 Kharif declaration. So I reported the comparison for 2018 only and stated this limitation, instead of using a plausible date I could not verify.

The 2018 numbers: SIF crossed its 90%-decline threshold on 8 September 2018, NDVI on 12 September 2018, and the declaration came on 31 October 2018, 53 and 49 days later. This changed how I see the result. The SIF–NDVI gap, the focus of the paper, is 3 to 4 days. The gap between satellite and declaration is about 7 weeks. These are very different scales. For RQ3 the more important finding is that any satellite signal comes well before the current 7-week institutional process, and SIF would only be a small improvement on that. The policy case in the paper is now stated at that size.

The core numbers did not change. Everything in this entry is either a precision improvement (bootstrap intervals, Moran's I) or a new comparison (RQ3) that I should have run from the start, and the claims are now stated with more modest confidence than in earlier drafts.

## Entry 14

Every version of my Limitations section repeated the same point: 3 years, 2 droughts and 1 normal season, is too small a sample, and the 2 drought years differ a lot from each other. Instead of only stating this, I decided to add more years: 2016, 2017, 2019, 2022 and 2023. That brings the study to 8 years.

**First step: getting the raw data.**

GOSIF v2's 8-day product covers 2000 to 2024, so all 5 new years are available. I wrote src/acquisition/download_gosif_new_years.py to download them with the same DOY-153-to-361 window used for 2015, 2018 and 2020, and kept the same file naming, so the existing clip_gosif.py picks up the new files without changes. In src/acquisition/gee_data_acquisition.py I extended the STUDY_YEARS list to all 8 years and added 2 CSV exports, for regional and for district rainfall, because the original script only printed rainfall totals to the console. That was fine when I copied 3 numbers by hand, but not for 8 years.

One problem: the GOSIF server returns a 403 Forbidden error for every request from the network I was working on, with or without a browser user-agent header. It is the same kind of IP range block that stopped Sentinel Hub in my DOUBLE_JEOPARDY project. So the download has to run on my own machine at home, as that project's satellite downloads did.

**What is not yet done:**

Neither script has been run. The GOSIF download needs a normal home internet connection, and the Earth Engine extraction needs my authenticated personal Earth Engine account, the same requirement the original acquisition script already had. Every number in the project at this point is still the original 3-year result from the first pass. This entry is only the start of the expansion. The next entry will cover what comes back once both scripts have run and I rerun the pipeline on 8 years instead of 3: clipping, lag analysis, cross-correlation, bootstrap intervals and Moran's I. That will update every downstream document.

## Entry 15

I ran download_gosif_new_years.py first. All 135 files (5 years times 27 composites) downloaded on the first attempt, since this time it ran on my own connection. gee_data_acquisition.py was different. Each of the next 3 problems was a bug in code that had never been run before.

**Bug 1: no registered Cloud project.**

Earth Engine now requires `ee.Initialize(project=...)` with a registered Google Cloud project ID. My script only had a bare `ee.Initialize()` and a commented-out `ee.Authenticate()`, both written before Google added that requirement. I added both, with my own Earth Engine project ID.

**Bug 2: MODIS clip against the wrong projection.**

The NDVI extraction failed with a projection transform error when clipping a MOD13Q1 image on its native sinusoidal grid (SR-ORG:6974) against the Marathwada polygon in EPSG:4326. Some district boundary geometries do not transform cleanly onto that grid. The `.clip()` was not needed anyway, because the `reduceRegion()` call after it already limits the mean to the same geometry, so I removed it.

Bug 3 was a missing district. The script finished with no errors, but when I counted the rows, the district rainfall export had 56 rows instead of 64 (8 districts times 8 years). The MARATHWADA_DISTRICTS list used the spelling "Beed", but FAO GAUL 2015 stores the district as "Bid" in its ADM2_NAME field.

`ee.Filter.inList()` does not raise an error when a name matches nothing. It just leaves it out. So the district was missing from the merged region boundary and from every district-level export for all 8 years. I checked the spelling against the district GeoJSON in data/raw/, fixed the list, and ran the extraction again. Then I counted the rows in the output CSV by hand: 8 districts times 8 years gave 64 rows, with all 8 names present. All downstream analyses use this corrected table.

Next I ran rainfall_analysis.py on the corrected 8-year regional totals, and it gave the most unexpected result of this expansion. I used the same drought threshold as the original study, about half a standard deviation below the 2001–2020 mean. 2015 (−21.5%, z = −1.12) and 2018 (−18.3%, z = −0.95) are still the 2 driest years. None of the 5 new years comes close: 2016 was +9.5%, 2017 −1.1%, 2019 +13.3%, 2022 +36.8% and 2023 −3.7%, all within about 1 standard deviation of normal. So over the 8 years only 2 qualify as drought years by my definition. The original 3-year sample was 67% drought years only because of which years I happened to pick first, far more than Marathwada's actual climate. This goes into the limitations. It does not change the drought-year findings, but it shows the original sample was not representative. The 8-year record gives a much better picture of a normal year here.

I also replaced the hardcoded `DROUGHT_YEARS = {2015, 2018}` in the lag, cross-correlation and bootstrap scripts with a set derived from the rainfall anomaly output. It still gives the same 2 years, but the classification is now computed from the data, which matters more with 8 years than with 3.

**Still pending as of this entry:**

clip_gosif.py and aggregate_sif.py, which turn the raw GOSIF rasters into the SIF time series, still need to run on all 216 raw files (27 composites times 8 years). This has to happen on my own machine, because moving 11+ gigabytes of raw rasters is not worth it. Each clipped output is under 40 kilobytes, so only those need to go anywhere else for the dashboard or plots. After that I need to rerun the lag analysis, cross-correlation, bootstrap intervals, Moran's I and district correlations on all 8 years. Until then the project still has the original 3-year numbers.

## Entry 16

I ran clip_gosif.py and zonal_stats_sif.py on all 216 raw GOSIF files on my own machine, as with the downloads in Entry 15. Neither script needed any change for the 5 new years, because both find files with a glob pattern and have no hardcoded year lists. I wrote them that way when I only had 3 years, and it paid off here.

The outputs have the expected size. marathwada_sif_timeseries.csv has 216 rows (27 composites times 8 years) and sif_by_district.csv has 64 rows (8 districts times 8 years), matching the rainfall tables from Entry 15. That is a simple check that no year or district was dropped on the SIF side.

With the 8-year SIF data in place I reran every downstream script: compare_sif_ndvi.py, lag_analysis.py, cross_correlation_lag.py, bootstrap_lag_uncertainty.py, sif_rainfall_correlation.py, spatial_autocorrelation.py and rq3_official_declaration_comparison.py. I also replaced the remaining hardcoded `DROUGHT_YEARS = {2015, 2018}` with the rainfall-derived classification from Entry 15, so the classification is the same everywhere. And I fixed 2 deprecation warnings: `matplotlib.cm.get_cmap` became `matplotlib.colormaps[...].resampled(...)`, and geopandas's `.unary_union` became `.union_all()`.

The most notable result is 2018. Every lag method, threshold crossing, cross-correlation and the bootstrap, shows 2018 behaving differently from the other years. Its mean threshold-crossing lag is slightly negative, −1.1 days, against 4.2 to 23.8 days in every other year. Its cross-correlation lag is exactly zero. Only 8.1% of its bootstrap replicates are positive, against 42 to 97 percent for the other years. A fourth check, the RQ3 comparison against the 2018 declaration, shows NDVI crossing its 90%-decline threshold *before* SIF that year, the reverse of what the 3-year study found. I have no crop type, sowing date or other data that could explain why 2018 is different, so I am recording it as an unexplained result. I am not guessing a cause and not averaging it into the drought-year group.

The other main result: only 2 of the 8 years are drought years. Entry 15 found this from rainfall alone, and it holds with the SIF data added too. The original 3-year sample, 2/3 drought years, was much more drought-heavy than Marathwada's 8-year record.

**Weaker, but still real, at the larger sample.**

The district SIF–rainfall correlation dropped from r = 0.837 (n = 24) to r = 0.567 (n = 64). It is still significant, but this is a clear weakening, not a rounding difference, and I report it that way. Moran's I gives a mixed picture. Rainfall is spatially clustered in all 8 years, as it was in all 3 originally. SIF is clustered in only 4 of the 8 years. So the clustering is real in some years and not detectable in others, a more qualified result than the original "significant in all 3 years".

I rewrote the district ranking section. Nanded, the highest-SIF district in all 3 original years, is highest in only 2 of 8 years now. Aurangabad is highest in 4 of 8, and 2 other districts once each. The "consistently highest" statement from the 3-year study does not hold with the larger sample, and I say so.

The bottom of the ranking is more stable. Osmanabad has the lowest SIF in 7 of the 8 years, with Bid lowest in 2018. Bid in 2018 is also the lowest single SIF value in the study, and that year had its worst rainfall deficit. The earlier claim that every year's lag is positive also no longer holds at 8 years, because 4 years now tie at exactly zero days.

This completes the sample expansion. Every number in the project is now the 8-year result, not a mix of old and new.

## Entry 17

I found a real bug during a slow, line-by-line read of cross_correlation_lag.py and bootstrap_lag_uncertainty.py. Both scripts search for the lag that best lines up SIF and NDVI, but in both files the search range was written as `np.arange(0, max_lag + 1)`. It only checked lags from zero upward, so neither script could ever return NDVI leading SIF, whatever the data showed. The data never said "never negative". The code never looked there.

This changes what "SIF's lag is never negative" means. Earlier entries and the paper reported the cross-correlation lag as never negative and the bootstrap as 100% non-negative in every year. Both statements were true only because the search range excluded the other answer before looking at a single number. That is not a finding.

In cross_correlation_lag.py I changed `lags = np.arange(0, max_lag + 1)` to `lags = np.arange(-max_lag, max_lag + 1)` and added a small `lagged_corr()` helper that handles positive, negative and zero lags as 3 separate cases, since numpy slicing with a negative shift has to go the other way. I made the same 2-sided change in the `lag_from_daily()` function in bootstrap_lag_uncertainty.py and updated its boundary check (`abs(lag) >= len(sif_c) - 4`), so it also guards against too few overlapping points on the negative side. Then I reran both scripts on the merged SIF/NDVI data.

The corrected numbers change the result, not just the wording. Cross-correlation lag by year: 2015 at 4 days, 2016 at 2 days, 2017 at 27 days, 2018 at −4 days, 2019 at 18 days, 2020 at 0 days, 2022 at −9 days, and 2023 at −10 days. With the 1-sided search, 2018, 2020, 2022 and 2023 all came out at exactly zero because zero was the lowest value allowed. Now 3 of those 4 years, 2018, 2022 and 2023, are negative, meaning NDVI leads SIF in those years by this method, and only 2020 is a true tie. So instead of "SIF leads in half the years and ties in the other half", it is now "SIF leads in 4 years, ties in 1, and NDVI leads in 3".

The bootstrap backs this up. In 2022 and 2023, 99.4% and 99.1% of replicates are below zero, a clear result in the NDVI-leads direction. 2018 leans the same way with 87.4% of replicates negative, but its confidence interval still includes zero, so it is less certain than 2022/2023. I also redid the pairwise comparison of years. Of the 28 possible year pairs, 24 still overlap, but 4 pairs no longer do: 2015 vs 2022, 2015 vs 2023, 2017 vs 2022, and 2017 vs 2023. So the 2 clearest SIF-lead years are now statistically different from the 2 clearest NDVI-lead years, which the 1-sided search could never have shown.

I then fixed every place that repeated the "never negative" framing: the methodology, results, abstract, discussion, limitations and conclusion of GA_Research_Paper.md; both figures, cross_correlation_lag.png and cross_correlation_lag_bootstrap_ci.png; the 2 dashboard pages that show these numbers; GA_Executive_Summary.md; and README.md. The bug is described in each place, as with the Beed/Bid boundary bug and the Earth Engine Cloud project bug earlier in this log. This one changes a scientific finding, not just a processing detail.

I also found a leftover from Entry 16 that I had said was fixed but was not: clip_gosif.py still used `boundary.geometry.unary_union` instead of `union_all()`. I had missed this one file. It is fixed now.

## Entry 18

The journal's desk rejection gave 5 reasons, and 1 of them I could not argue with: no field validation. Everything in this study, all 8 years of it, compares satellite with satellite (SIF vs NDVI) or satellite with a rainfall product (SIF vs CHIRPS). Nothing was checked against what actually happened to crops on the ground. I do not have the budget or the time for a farm survey across 8 districts and 8 years, so I looked for the next best option.

The Ministry of Agriculture & Farmers Welfare publishes Area/Production/Yield statistics by district, season and crop, for every year since 1997-98. The government has already collected these. Getting the file took longer than expected. The first site I found, dataful.in, charged ₹1499 for the CSV. The same dataset is free on the India Data Portal (indiadataportal.com) with only an email sign-in, so I downloaded it there: crop-wise-area-production-yield.csv, 455,359 rows, all of India, 1997-98 to 2022-23.

I wrote src/analysis/crop_yield_validation.py to filter it to the 8 Marathwada districts and the Kharif season, the monsoon crop cycle that the SIF and NDVI curves track. First I had to map district names, because 2 districts were renamed in 2023 and the dataset uses the new names for all years: Aurangabad appears as "Chhatrapati Sambhajinagar" and Osmanabad as "Dharashiv". I mapped both back to the names used in the rest of the project.

For the check I used the same z-score method as for the CHIRPS rainfall baseline (Section 3.5), applied to yield. For every crop with at least 10 of the 26 years present in a district, I scored each year against that crop's own 26 year mean and standard deviation, averaged all crop scores in a district-year into one Yield Anomaly Index, and averaged the 8 districts into one Marathwada value per year. 16 crops qualified, mostly the main Kharif crops I expected: cotton, soyabean, jowar and tur.

The yield anomaly correlates with my rainfall anomaly at r = 0.935, p = 0.002, which suggests the index measures something real. Against mean SIF it is r = 0.669, p = 0.10, in the right direction but not significant with n = 7 years (2023 has no published yield yet, so it drops out). The most relevant result: the 2 drought years, 2015 and 2018, have a mean yield anomaly of −1.08, against +0.11 for the 5 normal years with yield data. Harvests were worse in the years I classify as drought years from rainfall and satellite data alone. A Welch's t-test gives t = −2.87, p = 0.13. That is not significant, which is what I would expect with only 2 drought years, the same small-sample problem that affects H3. I report it as a consistent signal in the expected direction, not as proof.

This is not a field survey. It is yield statistics, 1 end-of-season number, so it says nothing about SIF's timing within the season. But it is an external, government-sourced check that the years and region I call stressed from satellite data were years when Marathwada produced less. I added it as Section 4.11 and updated the Abstract, Limitations and Conclusion: it supports the drought classification in direction but does not reach significance.

## Entry 19

Two more items from the limitations list today: 2021, the 1 year my 8-year expansion did not include, and the single pooled regional rainfall baseline that Section 6 already flagged. Both needed Earth Engine. This time I exported NDVI and rainfall for 2021, and a per-district climatology, from the Code Editor in the browser instead of the local Python script, which is quicker when I only need a couple of exports.

2021 first. I wanted to check why I had skipped it instead of leaving that unexplained. 2021 had 969.95 mm of seasonal rainfall, z = +0.90 against the usual 2001-2020 baseline, a wetter-than-normal year and not a drought year. So I had not left out a drought season. I still cannot add 2021 as a ninth study year, because I do not have its SIF data. GOSIF is not on Earth Engine, so the raw GeoTIFFs have to be downloaded by hand from the UNH data page and run through clip_gosif.py like every other year, and I have not done that yet. NDVI and rainfall for 2021 are in data/raw/.

The per-district climatology was more interesting. I pulled each district's own 2001-2020 mean and standard deviation instead of using 1 pooled value for all. The districts differ a lot. Osmanabad averages 704.9 mm and Nanded 1009.0 mm over the same 20 years, while all of them had been compared with the pooled 826.4 mm. So a district that is normally wetter or drier than the region was being judged against a baseline that was not its own normal.

I wrote district_climatology_anomaly.py to see how much this matters. It recomputes every district-year z-score against the district's own baseline and compares the two. 6 of the 64 district-years change their drought/normal classification depending on the baseline: Nanded and Hingoli in 2015, Aurangabad in 2017, and Aurangabad, Bid and Osmanabad in 2023. The 2 series still correlate at r = 0.840, so it is mostly a rescaling and not a reordering, but 6 changed classifications is not nothing. The study's drought-year definition (Section 3.5) uses a single regional number, so it is unaffected: 2015 and 2018 stay the drought years. But it is a limitation of the district-level correlation and Moran's I results in Sections 4.5 and 4.8, and now I have a number for it instead of a vague caveat. I updated the limitations bullet in Section 6 and the dataset introduction in Section 3.1 to say this.

## Entry 20

Today I finished 2021 as the ninth study year, not just the rainfall and NDVI part that had been in data/raw/ since Entry 19. Downloading the raw GOSIF files took 3 tries. First I took the Monthly tier by mistake instead of the 8day tier, 7 files instead of the 27 8-day composites the threshold method needs. On the second try I downloaded 19 files named GOSIF_2002<doy>.tif.gz instead of 2021. I must have misread the year while scrolling a long sorted list where every filename looks the same. I deleted those, and on the third try searched for "2021" with Ctrl+F instead of scrolling. That got all 27 files, DOY 153 through 361, the same as every other year.

Processing them locally ran into a disk space problem that had nothing to do with the science. Each file unzips to ~52MB, so all 27 at once is over a gigabyte, on top of the rest of the project. I changed clip_gosif.py to work 1 file at a time: unzip, clip to the Marathwada boundary, delete the decompressed raster, move to the next. Peak disk use is now under 100MB instead of 1.4GB. The clipping itself is unchanged. All 27 clipped fine, with a 47.75% valid pixel fraction, the same as every other year with the same boundary polygon.

One thing needed care. My working copy has the raw GOSIF files for only some of the 8 original years, because I never needed to move all of them off my machine. So I could not just rerun aggregate_sif.py and zonal_stats_sif.py as in Entry 16. They read whatever files are in the folder and overwrite the output, so they would have replaced the 8-year outputs with 2021 data only. Instead I applied their per-file calculation to the 2021 rasters and appended the new rows to the existing CSVs, and checked that every other year's rows were the same before and after. I did the same for the consolidated NDVI file and the district rainfall file, using the anomaly calculation (mean=826.4mm, std=158.8mm, the same pooled baseline as every other year in this study) on the 2021 district rainfall from Entry 19.

With 2021 merged into marathwada_sif_ndvi_merged.csv and sif_rainfall_district_merged.csv as real rows, not a side file (bringing them to 243 composite rows and 72 district-year rows), I reran the downstream chain: compare_sif_ndvi.py, lag_analysis.py, cross_correlation_lag.py, bootstrap_lag_uncertainty.py, spatial_autocorrelation.py, sensitivity_checks.py, final_summary.py and crop_yield_validation.py. I added 2021 to the STUDY_YEARS list of the yield script too, since the government yield data go up to the 2022-23 season and include 2021. None of these scripts had hardcoded year lists left after the Entry 15 cleanup, so they all picked up the ninth year from the merged files, which is why I wrote them that way in Entry 16.

2021 looks like an ordinary normal year on every check. Mean threshold-crossing lag: 13.1 days, in the middle of the normal-year range and far from 2018's −1.1 days. Cross-correlation lag: +14 days, r=0.984, with a normal decline curve. Yield Anomaly Index: −0.13, close to 0, unlike the −1.08 average of the 2 drought years. The rainfall z-score is positive in all 8 districts, not only for the region (+0.90, as found in Entry 19). The district-climatology flip count stays at exactly 6, now out of 72 rows instead of 64, so 2021 adds no new flips. Moran's I for 2021 rainfall is significant, as in every year, and for SIF it is not, matching the roughly half-significant pattern of the other years.

So n is now 9, not 8 with an asterisk. Every table, script output and figure in outputs/figures/ has been regenerated from the 9-year merged data. The paper text has not been updated yet: the dataset description in Section 3.1, "8 years" in the abstract, every count of n=8 or n=64 in Sections 4.5-4.11, and the Limitations bullet about 2021 being unprocessed all need to change before the paper goes back to JAG. That is the next step.

## Entry 21

Today I went through GA_Research_Paper.md section by section and fixed every place that still said "8 years" or "n=64", or gave a statistic from the old 8-year run: Highlights, Abstract, §3.1, §3.5, §3.9, §4.1 through §4.11, Discussion, Limitations and Conclusion. Every new number came from the Entry 20 rerun, not from memory. I also caught a few things. §4.1 said "SIF declined ahead of NDVI in six of eight years", a qualitative call with no clear numeric rule behind it, so I opened the regenerated seasonal figure and counted. It matches the "8 of 9" in §4.2, with 2018 the one exception. In §4.7 I had first written "SIF ahead in about two-thirds of the years", which did not match my own year-by-year classification, so I changed it to the actual split: 4 years SIF ahead with clear confidence, 2 years NDVI ahead with clear confidence, and 3 years too close to call. And §4.8's Moran's I range had a typo, 0.21 where the real minimum (2019, 0.2577) rounds to 0.26.

The 4 companion documents, GA_Highlights.md, GA_Executive_Summary.md, Policy_Brief.md and README.md, quote the same statistics, so a leftover "8 years" in any of them would make the package inconsistent even with the paper fixed. I fixed everything grep found in all 4: the "7 of 8"/"3 of 8" counts in GA_Highlights.md and a crop-yield bullet that was in the paper but not in the highlights; the findings table and year-by-year summary in GA_Executive_Summary.md; the numbers throughout Policy_Brief.md, plus a crop-yield paragraph it never had, even before 2021 (it still said crop yield "has not been checked" although §4.11 already existed); and the Key Findings section of README.md, plus 3 other spots in that file (the 1-line project description at the top, the sample-expansion sentence, and a comment in the repo structure tree). I also checked GA_Cover_Letter.md and GA_Author_Statement.md. The cover letter had the same "8 growing seasons" line, now fixed. The author statement does not mention year counts.

So the stale-numbers problem is closed: the paper and all 5 companion documents match the n=9 pipeline. What is left cannot be fixed with more years or reruns. GOSIF is a modelled SIF product that shares MODIS reflectance input with the NDVI it is compared with, and that comes with the data source. 2018 remains unexplained on every method I have tried. The crop-yield check in §4.11 will stay below conventional significance while there are only 2 drought years, and adding normal years does not fix a small sample on the drought side. And RQ3 stays a single-year comparison, because 2018 is still the only year with a clean official declaration date. These stay in the paper as permanent limitations.

## Entry 22

A full audit of the repo found a bug bigger than the search-range one in Entry 17. Every NDVI row in my 9-year file had a day-of-year one less than its own date column: 2015-06-10 was labelled 160 when it is actually day 161. The cause is in gee_data_acquisition.py and the Code Editor .js file. `img.date().getRelative("day", "year")` counts from zero (1 January = 0), while GOSIF's filenames use normal 1-based day-of-year. My original 3-year NDVI export, done by hand in the Code Editor back in Entry 2, had the right labels (161, 177...). The bug only came in when I rewrote the extraction as a Python script for the 8-year expansion.

One day mattered this much because compare_sif_ndvi.py matched each 8-day SIF date to the *nearest* 16-day NDVI date, and every other SIF date sits exactly 8 days from 2 NDVI composites (SIF 169 is 8 days from both NDVI 161 and 177). With the wrong label the tie always went to the later NDVI composite, whose window starts after the SIF composite has already ended. So half the SIF dates got NDVI from the next period, NDVI looked about 8 days earlier than it was, and every lag shrank by about 8 days.

To check that this is the cause, I ran the current SIF data against the original 3-year NDVI file (correct labels) and got 24.3 / 6.9 / 28.7 days threshold-crossing and 13 / 4 / 7 days cross-correlation for 2015 / 2018 / 2020, exactly the values in Entry 11 and Entry 12. So the SIF side never changed. The drop in Entry 16 that I blamed on the Bid boundary fix was actually this date bug arriving in the same pass. That explanation was wrong, and it is now corrected in the paper.

Fixes: `.add(1)` on the day-of-year in both Earth Engine scripts; `doy` recomputed from the `date` column in all 11 NDVI CSVs; and compare_sif_ndvi.py now pairs each SIF composite with the NDVI composite whose 16-day window contains it (`direction="backward"`) instead of the nearest one, so there is no tie to break. sensitivity_checks.py's alternative is now interpolation at each composite's centre date. While rerunning I also gave the bootstrap its own random seed per year (sharing one stream meant adding 2021 had silently changed 2022 and 2023's bootstrap numbers), fixed the Moran's I seed (p-values were moving slightly between runs), fixed the RQ3 script's `%-d` date format that crashes on Windows, and relabelled its "90% of seasonal peak" events, because a 0.9 threshold is 10% of the way down from the peak, not 90%.

Corrected results, rerun on my own machine: threshold-crossing lag 24.3, 31.8, 29.6, 6.9, 25.2, 28.6, 21.1, 13.1, 12.2 days (2015-2023). SIF leads in all 9 years, and the drought mean is 15.6 vs 23.1 for normal years, so H3 is still not supported. Cross-correlation: 13, 11, 16, 4, 26, 7, 22, −1, −2 days; 2019's 26 sits at its ±26-day search edge. Bootstrap: only 2015 and 2016 have intervals that exclude zero, and no year supports NDVI leading (2022 is 52.5% negative, 2023 80.5%, and both intervals include zero). 3 of 36 year-pairs do not overlap. RQ3: SIF crosses the 0.9 threshold on 8 Sep 2018 and NDVI on 12 Sep, 53 and 49 days before the declaration.

This undoes "2018 breaks the pattern on every method", "NDVI leads in 2018, 2022, 2023", "99%+ of replicates below zero" and "NDVI crossed first in 2018". None of those hold. As in Entry 17, the paper describes the change in Section 3.3 and Section 6. The audit also showed that the 0.9 threshold is crossed in early-to-mid September in wet years too, so the "7 weeks before the declaration" result is about seasonal timing and is not a drought alarm. The paper now says that.

## Entry 23

*1 October 2026*

This was the last round on the limitations list, and it changed what the paper claims. I went through every open item one at a time and reran everything from a single script, `run_all.py`, so every number below comes from one end-to-end pass rather than a chain of scripts run by hand.

Data handling first. The GOSIF files for 2021 and 2022 had a half-pixel (0.025°) longitude offset; fixing the grid moved the regional lag by less than 0.1 day and district lags by at most 1.0 day. I had also been using two different rainfall sources for different anomalies, so I moved everything onto CHIRPS seasonal totals (1981–2023) with one 2001–2020 baseline. NDVI is now dated by the mean per-pixel `DayOfYear` of each MOD13Q1 composite and interpolated onto the SIF composite centre dates, and SIF is weighted by each cell's cropland fraction (MCD12Q1 classes 12 and 14). Together these change individual years' lags by −2.5 to +2.6 days and flip no direction; almost all of that comes from the NDVI timing, not the weighting.

Baseline sensitivity. Six study years sit inside the 2001–2020 baseline, so I reran the drought classification against 2001–2014, 1981–2014 and 1991–2020, and for every cut-off from −0.3 to −0.75. Only 2015 and 2018 are drought years in every case. Under z < −1.0 only 2015 is left, which is too few to compare anything.

Main lag on the corrected pipeline (threshold-crossing, mean of 0.9–0.5): 21.7, 34.2, 28.5, 8.0, 25.4, 27.1, 20.3, 11.8 and 11.1 days for 2015–2023. All nine positive; of 43 crossings, one goes the other way (2019 at 0.9, −1.3 days). The residual bootstrap keeps every year above zero, 2018's interval is [3.9, 19.8], and only 3 of 36 year-pairs have non-overlapping intervals. Cross-correlation gives 10, 12, 14, 4, 0, 9, 20, −1, −3: SIF ahead in six years, a tie in 2019, and a small NDVI lead in 2022 and 2023. The curves are flat (r at zero shift is already 0.975–0.993), and only 2015 and 2016 have intervals that exclude zero, with 2018 sitting on it.

Method dependence. I recomputed the regional lag under 40 combinations of SIF weighting, NDVI timing, smoothing and lag metric. "SIF leads in all nine years" holds in 8 of 8 mean-threshold variants and 0 of 8 cross-correlation variants. Drought years have the smaller lag in 34 of 40, and 2018 is the smallest in 22 of 40. So the direction holds for methods that read points on the decline, and not for whole-curve alignment.

TROPOMI cross-check. GOSIF is partly built from MODIS reflectance, so it isn't fully independent of NDVI. I pulled TROPOSIF v2.1 soundings for 2018–2020 (630,091 over Marathwada, 53% past the cloud filter) and built 8-day composites. TROPOMI tracks GOSIF at r = 0.91–0.97, puts SIF first in all three years and gives 2018 the smallest lead, but the lags are 12.8, 43.8 and 45.3 days against GOSIF's 8.0, 25.4 and 27.1, about 1.6–1.7 times larger. Direction and ranking carry over; the size doesn't.

District lag and H2. All 72 district-years have SIF first (median 17.7 days, range 2.4–43.6). District means run from 13.4 (Osmanabad) to 21.7 (Jalna). The two-way ANOVA gives p = 0.055 and the Friedman test p = 0.043, so H2 is only weakly supported. Cross-correlation is less consistent at district level: 52 SIF lead, 4 ties, 16 NDVI lead.

H3 and the 2018 question. Drought years average 14.8 days against 22.6 for normal years, the opposite of H3; the continuous version gives r = 0.19 (p = 0.62), and at district level it's 14.9 vs 19.7 (p = 0.083). I checked whether rainfall timing explains 2018's small lag (monthly totals, rainfall centroid, longest dry spell). None of them correlate with the lag at p < 0.05, regionally or by district. 2018 stays small and unexplained.

District seasonal SIF. District SIF on day 273 correlates with the rainfall anomaly at r = 0.53 (p < 0.0001; p = 0.001 with year-clustered errors), and season-mean SIF at r = 0.74. With district and year fixed effects it isn't significant (p = 0.37). Rainfall and season-mean SIF are both spatially clustered (Moran's I) in all nine years, so the clustered and fixed-effects versions are the ones I'm relying on. Osmanabad has the lowest SIF in 8 of 9 years (Bid in 2018).

Crop-yield sensitivity. The Yield Anomaly Index tracks rainfall at r = 0.93. Against SIF it's r = 0.67 (p = 0.071), and 0.80–0.85 once I removed zero yields and outliers or used area-weighted, detrended or major-crops-only versions. Drought years average −1.08 against +0.07 (p = 0.15; all variants 0.18–0.23). Right direction, not significant with two drought years.

Drought-specific signal (H4). This is the analysis I should have run much earlier. A seasonal lag only says when each index starts its normal decline, not when it leaves normal. So I standardised each year's SIF and NDVI against the normal years at each composite date and set an alarm at two consecutive composites below a z threshold from 1 July. At regional scale z < −3 is the only threshold with no false alarm in a normal year. In 2015 both indices fire on 24 August; in 2018 NDVI fires on 25 September and SIF on 3 October, eight days later. Across the 17 drought district-years (55 normal), both flag 12 at z < −3, SIF with 1 false alarm and NDVI with 5; where both fire, NDVI is earlier in 7, the same in 4 and later in 1 (median 8 days earlier). SIF's AUC reaches 0.75 on 23 July, one composite before NDVI, but NDVI's AUC is higher from 31 July to 19 October. H4 is not supported.

Rainfall Trigger-1 and declarations. I approximated the Manual for Drought Management's Trigger-1 (deficit over 25% plus a dry spell of 21 days or more, after 1 July). It never fired at region level, and fired in 4 of 17 drought district-years plus one normal one. In 3 of those 4, both satellite alarms came first (NDVI 24–86 days, SIF 16–78 days). Against declarations, both alarms came 52.5 days before the 2015 one; for the 2018 final declaration SIF was 27.5 days ahead and NDVI 35.5. But a declaration follows field verification, so a satellite signal will precede it almost by construction. The rainfall trigger is the comparison that means something.

What this changes. The paper now separates two questions I had been treating as one. SIF's seasonal decline does start before NDVI's, in every year and every district-year, and TROPOMI agrees on the direction. But SIF does not leave its normal range earlier than NDVI in a drought year; NDVI is usually first, and SIF's only edge is fewer false alarms at the strictest threshold. So SIF leads the seasonal decline but it is not an earlier drought alarm. For policy, satellite anomalies may add lead time to a rainfall trigger, but nothing here says SIF adds more than NDVI already does. I rewrote the title, abstract, highlights, discussion and conclusion around that, put the five preprint corrections into one short section (3.14), and left the remaining limitations as they are: two drought years, method dependence, lags close to the 8/16-day sampling interval, thresholds chosen during the study, GOSIF–MODIS dependence, ~5 km scale on a mixed cropland mask, non-independent districts, an approximated trigger, and declarations that are late by design.

## Entry 24

Review pass and fixes. I went through the whole project again like an outside reviewer would and found a few things that change the story, so I fixed what I could without new downloads.

Normalisation. My threshold lag scales each series from its seasonal minimum to its peak. But NDVI never comes back down to its June level after the monsoon (post-peak floor 0.23–0.59 on that scale; SIF 0.00–0.28), so NDVI crosses every threshold later just because of where its floor sits. I added `normalisation_sensitivity.py`, which also scales each series from its peak to its own post-peak minimum, plus an asymmetric double-logistic end-of-season date. Decline-scaled lags: 9.6, 13.4, 10.6, 3.5, −5.5, 8.8, −1.2, −1.0, 0.4 days (2015–2023), so SIF is first in 6 of 9, not 9 of 9. Districts: 52 of 72, median 2.3 days, and the district effect disappears (Friedman p = 0.97 vs 0.043), so H2 is now not supported. The double-logistic dates swing from −30 to +41 days and the fits are unstable, so I only report them as a check. Cross-correlation, which does not care about scale, agrees more with the decline-scaled numbers. TROPOMI stays SIF-first under both scalings (10.4, 10.3, 27.7 days decline-scaled).

District drought baseline. District drought-years are now classified against each district's own rainfall baseline (15 drought, 57 normal) instead of the regional one (17/55), which is kept as a sensitivity check. H4 at z < −3: SIF flags 12, NDVI 13; where both flag, same date 6, NDVI earlier 5, SIF earlier 1; false alarms SIF 2, NDVI 4. At z < −1.5 NDVI is earlier in 13 of 15. H4 still not supported, and now it is the main question of the paper.

Rainfall trigger. The dry-spell counter used to run to December, so post-monsoon dry weather counted as a monsoon dry spell. Now it only counts 1 July – 30 September (the old version is kept as a variant). The trigger never fires for the region and fires in 2 of 15 drought district-years (Aurangabad 2018 on 3 Oct, Bid 2018 on 17 Sep) plus Bid 2017. I also wrote `gee_chirps_dryspell_area.py` + `rainfall_trigger_pixel.py` for a per-pixel version, which still needs to be run in Earth Engine.

Bootstrap. The threshold-lag bootstrap now resamples residuals in blocks of three and centres replicates on the reported lag. Intervals changed (2018 [2.8, 16.1]); 8 of 36 year pairs now separate; drought minus normal −7.8 days with a measurement-only interval [−9.9, +1.8].

Other checks. `ndvi_coverage_check.py`: 23 of 117 regional NDVI composites have under 25% clear cropland pixels, but dropping them changes no lag direction. `tropomi_drought_signal.py` runs H4 on TROPOMI but only has two normal years, so it is illustrative for now. Rainfall: June–September totals give the same two drought years; August 2023 was very dry (z = −2.52) and 40 talukas were declared in drought on 31 Oct 2023; 2001–2004 and 2014 would also be drought years, so going back before 2015 is the main way to get more drought cases. `crop_yield_validation.py` now uses season-mean SIF, the same measure as `crop_yield_sensitivity.py`: r = 0.88 (p = 0.004), and 0.80–0.85 across the sensitivity versions; the old r = 0.67 came from day-273 SIF alone. A full `run_all.py` rerun on my laptop (49/49 steps ok) reproduced every other number in the paper.

Figures and docs. Redid the RQ3 timeline (both drought years, alarms, trigger, declarations), the rainfall bar chart (z labels, criterion line), the anomaly curves (z = −3 line), the bootstrap and yield plots, and the graphical abstract. Map scripts now use colour scales symmetric about zero and the study-area map gets a locator inset once the state outlines are exported. Rewrote the paper around H4 as the main question, with a literature section, the normalisation result, and supplementary figures; updated the executive summary, highlights, policy brief, README, CITATION abstract, cover letter and dashboard pages to match; removed the proof-screenshot popovers and made the dashboard offer the .md documents when the PDFs are absent. Added `requirements-lock.txt` and new scripts to `run_all.py`.

Still to do (needs my machine or Earth Engine): full `run_all.py` rerun with the log committed; `gee_vi_obsdate.py` (NDVI vs EVI vs NIRv, to see whether the remaining lead is an NDVI property); the per-pixel trigger; more TROPOMI years; 2001–2014 extension; regenerating the maps; removing stale files and the decompressed raw GeoTIFFs.

## Entry 25

Two checks from my finish plan, both run in the Earth Engine Code Editor and then analysed with the existing scripts.

EVI and NIRv. I wanted to know whether the small SIF lead that survives the decline-range scaling is real or just NDVI being slow. I exported EVI and NIRv (NDVI x NIR reflectance) from the same MOD13Q1 composites, same masks, same observation dates; the NDVI column matched my old NDVI file exactly. NIRv declines before NDVI in 9 of 9 years (+22.8 days season-scaled, +9.9 decline-scaled) and EVI in 9 and 8 (+17.1, +7.7), as much as SIF does (+20.9, +4.3). Compared directly, SIF is first against NIRv in only 4 of 9 years season-scaled and in none decline-scaled. So the lead is an NDVI property (saturation, slow return to baseline), not a fluorescence one. The main conclusion does not change; this answers the obvious question about NDVI.

Trigger-1 per pixel. I ran the dry-spell trigger in every CHIRPS pixel instead of on district-averaged rain. It reached 25% of a district's area only in Aurangabad 2018 (40%), Bid 2018 (35%) and Bid 2017 (72%, a normal year). In 2015 it fired in at most 7% of any district. So the trigger is rare because of the rule itself in this region, not because of averaging. Timing against the alarms is the same as before: in Aurangabad 2018 NDVI came first (8.5 days), SIF 0.5 days before; in Bid 2018 both came 0.5 days after.

Updated the paper (methods 3.4 and 3.10, results 4.6 and 4.9, discussion, limitations, conclusion, abstract, highlights), the summaries, README, CITATION, dashboard pages and the graphical abstract.

## Entry 26

Out-of-sample test on 2001–2014, the last item in my finish plan. Two drought years was the biggest weakness, and 2001, 2002, 2003, 2004 and 2014 are drought years under the same rule, so I ran everything on those years without changing anything: same drought rule, same alarm rule and thresholds, same cropland weighting (each year's MCD12Q1 map), same NDVI screening and observation-day dating, same lag scalings. The only difference is that the anomalies are standardised against the normal years of 2001–2014, so nothing from 2015–2023 leaks in. I downloaded GOSIF for 2001–2014 (378 files) and exported NDVI/EVI/NIRv and cropland fractions in the Code Editor. `out_of_sample_2001_2014.py` first re-extracted 2015 and got the main series back exactly (largest difference about 1e-16), and `--check` mode reproduces every main alarm and lag exactly.

What came out. Districts (40 drought, 72 normal district-years): the same picture as 2015–2023. Where both flagged a drought district-year, NDVI was earlier in 22 of 37 at z < −1, 17 of 22 at z < −1.5 and all 13 at z < −2; SIF earlier in 10, 1 and 0. SIF again had fewer false alarms (16 vs 25 at z < −1.5). Region (5 drought, 9 normal years): the vegetation anomalies were weaker than in 2015 and 2018, and here SIF came out slightly ahead. At z < −3 SIF flagged 2001 (17 Sep) and 2002 (25 Sep), NDVI only 2002 on the same date, and no normal year was flagged by either; at z < −1.5 SIF was first in four drought years and NDVI in none. Over both periods SIF flags four of seven drought years at z < −3 and NDVI three, coinciding twice with NDVI earlier once, and at district level NDVI is earlier far more often. H4 stays not supported, but the regional evidence is less one-sided than in 2015–2023.

Seasonal lags reproduce: season-scaled SIF leads NDVI in 14 of 14 years (+27.4 days) and NIRv leads NDVI by almost the same (+26.6); decline-scaled NIRv declines before SIF in 11 of 14 years (−6.4 days). The lead is not larger in drought years (+28.3 vs +26.9 season-scaled), so H3 is not supported with five drought years either.

I kept the extracted 2001–2014 SIF series in `data/processed/oos_sif_*.csv` and added `data/raw/*.tif.gz` to `.gitignore`, so the GOSIF archives stay out of the repository and the test still reruns from the CSVs. Updated the paper (new sections 3.14 and 4.11 with Tables 5 and 6, abstract, highlights, Table 1, discussion, limitations, conclusion, revision note), the executive summary, policy brief, README, CITATION, cover letter and the dashboard.

## Entry 27

A final check of the whole repository before export, and one real error.

The district alarm comparison was dating every district NDVI alarm one composite too early. In `drought_signal_analysis.py` the district SIF and NDVI series go into two `pivot_table`s, one row per district-year and one column per SIF composite date. No district has an NDVI observation before the first SIF composite centre (day 156.5; the earliest NDVI observation day is 161.4), so that column is empty in the NDVI table and `pivot_table` dropped it. The SIF table kept 27 columns, the NDVI table had 26, and both were dated with the same 27 composite dates, so each NDVI anomaly was read one composite (8 days) before its real date. I checked it by hand on Aurangabad 2018: the NDVI anomaly first stays below −3 on day 260.5, but the table said 252.5. The out-of-sample script had the same line. The regional series were not affected, because they go through `pivot`, which keeps empty columns. The fix keeps every composite date in both tables (`dropna=False` and `reindex`) and asserts that the columns match.

What changed. Districts, 2015–2023, z < −3: SIF flags 12 and NDVI 13 as before, but where both flag, SIF is earlier in 7, the same in 2 and NDVI earlier in 3 (it was 1, 6 and 5). At z < −1.5 it is 2, 4 and 9 (was 1, 1 and 13); at z < −2, 4, 4 and 6 (was 2, 2 and 10). In 11 of the 12 at z < −3 the difference is at most one composite. With the regional baseline, z < −3 gives 5, 4 and 3. The date-by-date AUC now reaches 0.75 on 23 July for SIF and 31 July for NDVI. Out of sample, at z < −1.5 it is 5, 11 and 6 (was 1, 4 and 17), and at z < −2, 0, 7 and 6 (was 0, 0 and 13). Rainfall trigger: in Aurangabad 2018 both alarms came 15.5 days before the trigger; in Bid 2018 SIF came 0.5 days after it and NDVI 8.5 days after. Hit and false-alarm counts, all regional alarms and every seasonal lag are unchanged.

So the district result is no longer "NDVI was usually first". The two alarms are mostly within one composite of each other, with no consistent winner. Since NDVI is a 16-day product interpolated onto 8-day SIF dates, I also wrote `alarm_dating_sensitivity.py`, which reruns the alarm test with NDVI taken as observed (the last NDVI value available by the end of each SIF composite) instead of interpolated, because the interpolated value already contains part of the next NDVI observation. With that dating SIF is first in both regional drought years at z < −3 (by 8 days each) and in 8 of 12 district-years. The direction of a one-composite difference therefore depends on a dating choice, and I now report H4 as not supported in the sense that neither index gives a consistently earlier alarm the data can resolve.

TROPOMI against NIRv. My paper said that without a TROPOMI comparison against NIRv I could not separate a fluorescence lead from an NDVI effect, but I already had both series. `tropomi_vs_reflectance.py` computes it: TROPOMI declines before NIRv in all three years (5.4, 7.8 and 13.1 days season-scaled; 4.6, 1.2 and 12.5 decline-scaled) and before EVI by 3.0–20.8 days, and in 23 of 24 year-and-scaling cases across the four TROPOMI variants. GOSIF not leading NIRv is partly built in, since GOSIF is predicted from MODIS reflectance. Three years are too few to call this a fluorescence lead, but they are enough that I can no longer write that the whole lead is an NDVI effect. The paper now says this for GOSIF only and reports the TROPOMI result as open.

Smaller fixes from the same check: the cut-off statement now says the −0.3 to −0.75 range holds for the main 2001–2020 baseline (with the 1981–2014 baseline, 2018 drops out at −0.7); the cross-correlation is described as running over the post-peak decline, not the whole curve; the out-of-sample text says no vegetation data from 2015–2023 enter the test, since the drought rule keeps its 2001–2020 rainfall baseline; and the README says the GOSIF files need to be downloaded once before `run_all.py`. Updated the paper (abstract, highlights, 3.9, 3.11, 3.14, 4.1, 4.2 with Table 2, 4.6, 4.9, 4.11 with Table 5, discussion, limitations, conclusion, revision note), the executive summary, CITATION, cover letter, policy brief, README, dashboard, graphical abstract and both portfolio pages.
