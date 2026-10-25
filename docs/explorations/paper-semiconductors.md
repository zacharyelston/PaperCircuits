# Paper semiconductors: an exploration

Sheet: [out/T3-oxide-wafer.pdf](../../out/T3-oxide-wafer.pdf). Status: exploration, nothing built yet. Nothing here is part of the [page standard](../page-standard.md).

## The question

Can a class make its own semiconductor parts from layers on a sheet and a chemical treatment ("doping"), and use them to learn how chips are made?

Real chips are made in batches, and the same four steps could be done on paper:

1. **Wafer:** process one big sheet all at once.
2. **Dicing:** cut it into many small parts, called dies.
3. **Yield:** test every die and count how many work.
4. **Binning:** sort the working dies by how well they work.

## In short

- **Real silicon doping can't be done in a classroom.** It needs furnaces at 800–1200 °C and toxic dopant gases. No paper route imitates it.
- **Paper isn't a semiconductor.** In every route below, paper is the carrier, the frame or the electrolyte. The active layer is something else.
- **Two routes are worth building:**
  1. **Copper(I) oxide (Cu₂O) grown on copper foil** on a hot plate. It's a real p-type semiconductor that rectifies, and the material of the first commercial metal rectifiers. One foil sheet is the wafer. This is the **T3** sheet.
  2. **PEDOT:PSS on paper.** It's a conducting polymer whose conductivity really changes when it's doped and de-doped, at 1–2 V. It makes paper transistors rather than diodes, so it needs a sheet of its own later.
- **Three are not worth it now:**
  - the aluminium electrolytic rectifier: it rectifies, but it's wet and isn't a semiconductor
  - point contacts: they can't be made in a batch
  - ZnO/CuO junctions: they need lab chemistry

## The ideas

### Semiconductors

- **Metals** have plenty of free charges, so they conduct well.
- **Insulators** have almost none.
- **Semiconductors** sit between. They have few free charges, and the number changes with impurities, light and heat. That's what makes them useful: their conductivity can be set by design.

### Electrons, holes, n and p

Current in a semiconductor is carried by two kinds of charge:

- **Electrons**, which are negative. A material where they carry most of the current is **n-type**.
- **Holes**, which are places where an electron is missing. They move like positive charges. A material where they carry most of the current is **p-type**.

### Doping

Doping is adding a tiny, controlled amount of impurity to set how many carriers there are, and which kind. In silicon, light doping is about one dopant atom per 100 million silicon atoms. Phosphorus gives spare electrons (n-type), and boron gives holes (p-type) ([Wikipedia: Doping](https://en.wikipedia.org/wiki/Doping_(semiconductor))).

Doping doesn't always mean adding atoms:

- **Cu₂O** is p-type by itself. Missing copper atoms (copper vacancies) leave holes behind ([Biccari et al. 2013](https://ar5iv.arxiv.org/html/1310.5341)). How many vacancies form depends on how the oxide is grown: temperature, air and cooling. Here, the recipe is the doping.
- **PEDOT:PSS** is a polymer, PEDOT, that is oxidised ("p-doped"), with the PSS holding the balancing negative charge. Push positive ions into it from an electrolyte and it is de-doped: its conductivity falls. Pull them out and the conductivity comes back ([Wikipedia: OECT](https://en.wikipedia.org/wiki/Organic_electrochemical_transistor)).

### Junctions and rectifying

A **junction** is where two different materials meet. Charges cross it more easily one way than the other. A diode is a junction that **rectifies**: it passes current much more easily in one direction.

There are two kinds that matter here:

- **p–n junction:** p-type meets n-type. Silicon diodes and LEDs are p–n junctions (L01, L06).
- **Metal–semiconductor (Schottky) junction:** a metal meets a semiconductor. Crystal radio detectors work this way ([Wikipedia: Crystal detector](https://en.wikipedia.org/wiki/Crystal_detector)). So does the copper oxide rectifier: Brattain's 1951 review puts its barrier at the copper/Cu₂O interface, at about 0.5 V ([Brattain 1951](https://link.aps.org/doi/10.1103/RevModPhys.23.203)).

No real diode is perfect. The useful measure is how much better a part conducts forward than backward.

## Why not real doping

Silicon is doped in two ways:

- **Diffusion:** wafers are heated in a furnace, typically 800–1200 °C, with a dopant source ([Baidu wiki: diffusion furnace](https://b2bwiki.baidu.com/en/encyclopedic/semiconductor-diffusion-furnace)). Sources include phosphine, arsine and diborane gases ([Wikipedia: Doping](https://en.wikipedia.org/wiki/Doping_(semiconductor))). A dopant-source maker describes diborane, phosphorus oxychloride (POCl₃) and phosphine as toxic and corrosive ([Techneglas](https://www.techneglas.com/dopant-sources/dopant-advantages/)).
- **Ion implantation:** dopant ions are accelerated and fired into the wafer ([Wikipedia: Doping](https://en.wikipedia.org/wiki/Doping_(semiconductor))).

Neither is possible or safe in a classroom, and paper burns far below those temperatures. The routes below are honest substitutes: they make real junctions or real changes in doping, but in other materials and at kitchen temperatures.

## The candidates

### 1. Copper(I) oxide on copper foil: chosen for T3

**What it is**

- **Growing the oxide:** heat copper in air and it grows a black skin of copper(II) oxide (CuO). Underneath lies a red-orange layer of copper(I) oxide, Cu₂O.
- **History:**
  - Cu₂O is the classic homemade solar cell ([sci-toys](https://sci-toys.com/scitoys/scitoys/echem/echem2.html)).
  - It's the material of Grondahl's copper oxide rectifier, reported in 1926 ([Experimental Wireless, Jan 1928](https://www.worldradiohistory.com/UK/Experimental-Wireless/20s/Experimental%20Wireless-1928-01.pdf)).
  - Copper oxide rectifiers were used for decades before silicon. Each disc blocked "rarely more than a few volts", so discs were stacked in series ([Wikipedia: Metal rectifier](https://en.wikipedia.org/wiki/Metal_rectifier)).
- **As a semiconductor:** Cu₂O is p-type, with a band gap of about 2.1 eV ([Biccari et al. 2013](https://ar5iv.arxiv.org/html/1310.5341)).

**Where the junction is**

- **The rectifying junction** is at the copper/Cu₂O interface, inside each die ([Brattain 1951](https://link.aps.org/doi/10.1103/RevModPhys.23.203)).
- **The top contact** only has to reach the oxide. Grondahl pressed lead onto it. Current passed more easily from the lead into the copper than the other way ([Experimental Wireless, Jan 1928](https://www.worldradiohistory.com/UK/Experimental-Wireless/20s/Experimental%20Wireless-1928-01.pdf)).
- **T3 uses a dot of 6B pencil instead.** We haven't found that combination reported anywhere, so whether it rectifies, and which way, is a bench question.

**Materials**

- Bare copper foil, 0.1–0.2 mm, uncoated (craft or roofing copper)
- A single-coil electric hot plate, 1000 W or more. The sci-toys write-up found an 1100 W burner works and doubts a 700 W one gets hot enough.
- Washing-up liquid and a kitchen scouring pad
- Old scissors, a ruler, a fine permanent marker, a craft knife or fine sandpaper, and a 6B pencil
- A multimeter with a diode range

**Steps** (T3 sheet 3 has the full procedure)

1. **Clean:** scrub the foil bright with washing-up liquid and the scouring pad, and rinse it.
2. **Oxidise:** heat it at full power. It turns orange, purple and red, then black. Keep it there about 30 minutes after the coil glows, so the black layer is thick, because a thin coat stays stuck ([sci-toys](https://sci-toys.com/scitoys/scitoys/echem/echem2.html)).
3. **Cool slowly:** switch off and leave it on the plate for about 20 minutes. Copper and CuO shrink at different rates, so the black layer flakes off. Cooling it fast keeps the black stuck.
4. **Rinse:** rinse gently under the tap, rubbing with fingers only. Don't scrub or flex it, or the Cu₂O layer may be damaged ([sci-toys](https://sci-toys.com/scitoys/scitoys/echem/echem2.html)).
5. **Mark:** rule the streets, scrape a bare-copper contact (S) on each die, and draw a pencil-dot top contact (T).
6. **Test, cut, bin:** test every die, dice, test again, and bin.

**Left out on purpose**

- **Acid and lye.** Friedrichs strips the black CuO with hydrochloric (muriatic) acid and degreases with lye ([Friedrichs](https://hpfriedrichs.com/radioroom/cu-diode/rr-cu-diode.htm)). Both are corrosive. T3 relies on slow cooling instead.
- **Lead contacts.** Lead is toxic. Pencil graphite replaces it.

**Hazards**

- **Heat:** the coil runs at red heat. A dull red glow means over about 525 °C ([Wikipedia: Draper point](https://en.wikipedia.org/wiki/Draper_point)). That means burns and a fire risk:
  - An adult runs the plate.
  - Put it on a heatproof board, with nothing flammable nearby.
  - Move copper only with tongs.
  - Hot copper looks just like cold copper.
- **Flying flakes:** the black flakes can fly a few inches as the copper cools ([sci-toys](https://sci-toys.com/scitoys/scitoys/echem/echem2.html)). Everyone nearby wears goggles and keeps their face away.
- **Fumes:** ventilate the room, by an open window or an extractor.
  - Clean the copper first, so no grease burns.
  - Use uncoated foil only. Never heat copper tape: its glue would burn.
  - Never heat zinc, brass or galvanised steel. Friedrichs warns of zinc fumes ([Friedrichs](https://hpfriedrichs.com/radioroom/cu-diode/rr-cu-diode.htm)), which cause metal fume fever ([Wikipedia: Metal fume fever](https://en.wikipedia.org/wiki/Metal_fume_fever)).
- **The oxide itself:** Cu₂O carries the hazard statements H302+H332 (harmful if swallowed or inhaled) and H318 (serious eye damage) ([Wikipedia: Copper(I) oxide](https://en.wikipedia.org/wiki/Copper(I)_oxide)). Wash hands, wipe flakes up with damp kitchen roll, and keep food away.
- **Sharp edges:** cut foil is sharp, and craft knives are for adults.

**Expected behaviour**

- **A wide spread between dies.** Friedrichs's best junctions started conducting at "a few tenths of a volt" and reached forward/reverse ratios of 10:1 or better. But they were leaky, and about a dozen pipe caps failed before some worked ([Friedrichs](https://hpfriedrichs.com/radioroom/cu-diode/rr-cu-diode.htm)). That spread is the yield lesson.
- **On a meter's diode range:** expect a forward reading of a few tenths of a volt and a higher reverse reading. A good die may read OL in reverse.
- **Light changes the readings.** Cu₂O is light-sensitive: the sci-toys cell gives 50 µA at 0.25 V in sunlight, from a 0.01 m² plate. Test every die under the same light.
- **The middle and the edge may differ.** A hot plate doesn't heat evenly, so dies from hot and cool parts of the foil may behave differently. That shows up as a pattern on the wafer map, as it does in a real fab.

**Verdict:** chosen. It's cheap and real, one sheet is processed at once, and the variability is itself the lesson.

### 2. PEDOT:PSS on paper: the second choice

**What it is**

- **The material:** PEDOT:PSS is a conducting polymer sold as a water-based dispersion. It's p-doped as made.
- **The transistor:** in an organic electrochemical transistor (OECT), a positive gate voltage pushes cations from an electrolyte into the polymer. That de-dopes it and turns the current down ([Wikipedia: OECT](https://en.wikipedia.org/wiki/Organic_electrochemical_transistor)).
- **On paper:**
  - Nilsson and colleagues printed these on paper, running below 2 V with on/off ratios up to 10⁵ ([Nilsson et al., SPIE 5051](https://journals.spiedigitallibrary.org/conference-proceedings-of-spie/5051/0000/All-organic-electrochemical-device-with-bistable-and-dynamic-functionality/10.1117/12.484380.full)).
  - Sozen and colleagues drew 200 PEDOT:PSS devices on 80 g/m² copy paper with a pen plotter. Refillable marker pens carried the inks, graphite made the electrodes, and the paper itself was the gate's electrolyte ([Sozen et al. 2024](https://doi.org/10.1002/smsc.202400063)).
  - Across those 200 devices, resistance was 191 kΩ ± 47 kΩ, about 25 %, which the authors put down to the paper. That's a ready-made yield experiment.

**Treatment that raises conductivity:** glycerol and sorbitol, both food-safe, raise PEDOT:PSS conductivity. Reported gains run from 2× to over 1000×, depending on processing ([sorbitol, 2017](https://eurekamag.com/research/083/369/083369012.php); [glycerol](https://scholars.lib.ntu.edu.tw/handle/123456789/155690?&locale=en)). This is usually called secondary doping. One study argues sorbitol is a processing aid rather than a dopant, because the gain comes as it evaporates ([Nardes et al. 2008](https://heibib.ub.uni-heidelberg.de/search/Record/1684196213)).

**Materials**

- PEDOT:PSS dispersion (for example Clevios PH 1000) and a refillable marker or a fine brush
- Copy paper
- 6B pencil and 5 mm copper tape
- An AA cell for the gate
- A hot plate at 60 °C, or a hair dryer

**Steps** (a proposal, not yet tried)

1. **Print the grid:** a grid of cells, each with a 3 mm channel and a pencil-shaded back gate behind it.
2. **Paint:** paint PEDOT:PSS along a whole row of channels in one stroke. This is the batch step. Dry at 60 °C for 5 minutes, as Sozen did.
3. **Contacts:** shade pencil source and drain pads over each end of the channel. Join copper tape to them with pencil-rubbed glue, the T1 question.
4. **Dice and test:** cut the cells apart and measure source to drain. Then put +1.5 V on the back gate and measure again. De-doping should raise the resistance.
5. **Bin:** sort the cells by resistance or by on/off ratio.

**Hazards**

- **Acidity:** PH 1000 has a pH of 1.5–2.5 ([Ossila](https://www.ossila.com/products/pedot-pss-ph-1000)). Related PEDOT:PSS dispersions are classed as causing serious eye damage, H318 ([Ossila SDS](https://downloads.ossila.com/msds/p-jet-x-n-pedot-pss.pdf)). Wear goggles and gloves, and wipe up spills.
- **Drying:** stop at 60 °C.
- **Solvents to avoid:** papers often use ethylene glycol, which is poisonous and tastes sweet, DMSO, which carries other chemicals through the skin, or acids. All are left out here.

**Expected behaviour**

- **It switches; it doesn't rectify.** A gate voltage turns the current down, reversibly.
- **It's slow.** Sozen swept the gate at 1.6 mV/s and waited 400 s between measurements.

**Verdict:** second choice. It's the best "chemical doping on paper" story and the most paper-like route. But it needs a specialty material, and it makes transistors rather than diodes, so it doesn't fit T3's forward/reverse test. It's a candidate for a later sheet.

### 3. Aluminium electrolytic rectifier: not now

**What it is**

- **How it works:** aluminium and a second electrode, such as lead or steel, sit in an electrolyte. A thin film on the aluminium passes current more easily one way ([Wikipedia: Electrolytic rectifier](https://en.wikipedia.org/wiki/Electrolytic_rectifier)).
- **History:** in 1928, homemade B-battery eliminators used lead and aluminium plates in jars of borax, sodium bicarbonate or ammonium phosphate ([onetuberadio](https://onetuberadio.com/2018/03/12/1928-power-supply-with-homemade-rectifiers/)).
- **On paper:** it could be layered as aluminium foil, then paper soaked in baking-soda solution, then pencil-shaded paper. That's close to an electrolytic capacitor, which grew out of this rectifier.

**Why not**

- **It isn't a semiconductor junction.** It's an electrochemical valve.
- **It's wet.** It dries out, and aluminium and graphite in salt water make a small battery that confuses the meter.
- **It needs forming.** The film has to be built up with current first.
- **Borax is a reproductive toxin.** Borax, the classic electrolyte, is classified in the EU as toxic to reproduction, Repr. 1B, H360FD ([Council of the EU, ST 8424/09](https://data.consilium.europa.eu/doc/document/ST-8424-2009-ADD-2/de/pdf)).

**Hazards**

- **Borax:** use baking soda instead.
- **Gas:** it gives off hydrogen bubbles, a tiny amount at 4.5 V.
- **Mains:** the 1928 versions ran from mains transformers. Never do that.

**Verdict:** a possible one-off demonstration, with baking soda at P1's 4.5 V. It's not a wafer.

### 4. Point contacts: pencil on a blued blade, pyrite or galena; demonstration only

**What it is**

- **The crystal detector,** described as "the first semiconductor diode": a fine wire, the cat's whisker, touches a mineral crystal such as galena or pyrite ([Wikipedia: Crystal detector](https://en.wikipedia.org/wiki/Crystal_detector)).
- **The foxhole radio** made one from a pencil lead on a rusty or flamed razor blade, held by a safety pin ([Wikipedia: Foxhole radio](https://en.wikipedia.org/wiki/Foxhole_radio)).

**Why not**

- **Every contact is found by hand.** "Only certain sites on the crystal surface function as rectifying junctions" ([Wikipedia: Crystal detector](https://en.wikipedia.org/wiki/Crystal_detector)). Each contact has to be searched for by hand, and a knock loses it. Nothing about it can be done in a batch.
- **But it's the perfect counterexample.** Early detectors were unreliable because nobody controlled their impurities, their doping, until the 1930s ([Wikipedia: Crystal detector](https://en.wikipedia.org/wiki/Crystal_detector)).

**Hazards**

- **Razor blades:** use an adult and a single-edge blade in a holder.
- **Flaming a blade** is a flame hazard.
- **Galena** is lead sulfide: use iron pyrite instead.

**Verdict:** a 10-minute demonstration. Use a sharpened 6B pencil as a cat's whisker on a spare T3 die, and compare it with the pencil dot.

### 5. Oxide junctions such as ZnO on CuO: no

**What it is:** a true p–n junction: p-type CuO (the black layer T3 flakes off) against n-type ZnO. The lab routes are long:

- **Vacuum and hot water:** one 2025 study evaporated zinc onto silicon in a high vacuum and turned it into ZnO in hot water at 75 °C. It then soaked the ZnO in copper chloride solution and annealed it at 450 °C for an hour to make the CuO ([Irhayem and Al-Mayalee 2025](https://jns.kashanu.ac.ir/article_114866_60307aa5dbb489271476b8aa117aca3b.pdf)).
- **Grown ZnO:** another route grows ZnO from zinc nitrate and hexamine solutions at 60–90 °C for 2–8 hours, on a seed layer ([US patent 12201753](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12201753)).

**Why not**

- **The ZnO step is lab chemistry.** It needs a vacuum evaporator, copper chloride and a 450 °C anneal. The other route needs hours of controlled heating with zinc nitrate, an oxidiser, and hexamine, a fuel-tablet chemical.
- **Heating zinc in air gives zinc oxide fume.**

**Verdict:** no. But the black CuO that T3 throws away is a p-type semiconductor too, with a band gap of 1.2–1.7 eV ([Irhayem and Al-Mayalee 2025](https://jns.kashanu.ac.ir/article_114866_60307aa5dbb489271476b8aa117aca3b.pdf)). T3 asks whether dies with black left on them behave differently.

### Comparison

| Route | Semiconductor? | Rectifies? | One sheet, many parts? | Main hazards | Verdict |
|---|---|---|---|---|---|
| Cu₂O on copper foil | Yes, p-type | Yes, leaky | Yes | Hot plate, flying flakes | **T3** |
| PEDOT:PSS on paper | Yes, a doped polymer | No; it switches | Yes | Acidic ink | Later sheet |
| Aluminium electrolytic | No, electrochemical | Yes | Awkward, wet | Borax, mains | Demonstration |
| Point contact | Yes | Yes, erratically | No | Blades, lead in galena | Demonstration |
| ZnO on CuO | Yes, p–n | Yes | Lab only | Oxidisers, zinc fume | No |

## Testing a part with a multimeter

### The diode range

The diode range is marked with a diode symbol.

- **What it does:** the meter "produces a small voltage between test leads", red positive ([Fluke](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes)). The display shows the voltage across the part while a small test current flows.
- **Reading a silicon diode:** about 0.5–0.8 V forward, or 0.2–0.3 V for germanium, and OL (over range) in reverse.
- **Reading a fault:** OL both ways means open. A low, equal reading both ways means a short.
- **Why the ratio works:** the test current is roughly the same both ways, so Rev ÷ Fwd compares how hard the die is to push current through backward and forward. That's a fair single number for how well it rectifies.

### Fwd and Rev on T3

- **Fwd:** red on T (the pencil dot), black on S (the bare copper). This is Grondahl's easy direction, from the top contact into the copper, assuming pencil graphite behaves like his lead.
- **Rev:** swap the probes.
- **If it comes out backwards:** if most dies read lower Rev than Fwd, the easy direction is the other way. Note it, and bin each die on the larger reading divided by the smaller one.

### Good practice

- **Check the meter first.** A 1N4148 (L06's D1) reads about 0.6 V one way and OL the other. A resistor reads the same both ways.
- **Measure your meter.** Diode ranges differ between meters:
  - Read your meter's diode-range voltage, with nothing else connected, on a second meter's DC volts range.
  - Read its test current on the second meter's mA range.
  - Write both on sheet 2.
- **Keep conditions the same.** Use the same light and the same probe pressure for every die, because Cu₂O reacts to light.
- **Don't mix meters on one wafer.** An analogue meter's ohms range often makes the black probe positive.
- **Stick to the diode range for binning.** The resistance range works too: Fluke gives 1 kΩ to 10 MΩ forward for a good diode. But it tests at a different voltage on each range.

### Bins

These are the T3 sheet's starting limits, tagged `[T3]` until a first wafer shows what a real spread looks like:

| Bin | Name | Rule |
|---|---|---|
| 1 | Good | Fwd gives a reading and Rev reads OL |
| 2 | Fair | Rev is 3× Fwd or more |
| 3 | Weak | Rev is 1.5× to 3× Fwd |
| R | Resistor | Rev is under 1.5× Fwd: the same both ways, so not a diode |
| S | Short | Both readings under 0.05 V |
| O | Open | Both read OL |

## The batch lesson: wafer, dicing, yield and binning

### A fab on a table

| In a chip fab | On T3 |
|---|---|
| Wafer | A 90 mm square of copper foil, with clipped corners like a solar-cell wafer |
| Furnace step | The hot plate, about 30 minutes |
| Process recipe | Plate power, time and cooling |
| Mask and lithography | Streets ruled from the frame's ticks; T and S placed from the die layout |
| Contact opening through the oxide | Scraping S back to bare copper |
| Metallisation | The pencil dot, T |
| Wafer sort: probing every die | Fwd and Rev of every die before cutting |
| Wafer map | The bin map on sheet 2 |
| Dicing saw | Scissors along the streets |
| Final test | Fwd and Rev again after cutting |
| Binning | Bins 1–3 by rectification ratio |
| Packaging | The D1–D4 copper-tape packages on sheet 1 |

Things to tell the class, from the real industry:

- **Wafer sort.** Every die is probed straight after fabrication. The results go into a file called a wafer map, which tells the packaging line which dies to use. Failed dies were once marked with a dot of ink. Packaged chips are tested again ([Wikipedia: Wafer testing](https://en.wikipedia.org/wiki/Wafer_testing)).
- **Why test before cutting.** It's cheaper to throw a bad die away before paying to package it ([Wikipedia: Wafer testing](https://en.wikipedia.org/wiki/Wafer_testing)).
- **Yield can be low.** Manufacturing is variable "sometimes achieving yields as low as 30 percent" ([Wikipedia: Product binning](https://en.wikipedia.org/wiki/Product_binning)).
- **One die, several products.** Apple's A12X and A12Z share one die, with one GPU disabled on the A12X ([Wikipedia: Product binning](https://en.wikipedia.org/wiki/Product_binning)).

### Lesson plan

Allow three sessions of about 50 minutes, plus preparation. Work in groups of four, one wafer per group.

1. **Before:** an adult cleans and oxidises the wafers. With an older class, they can do it as a demonstration behind a clear barrier.
2. **Session 1, the fab:**
   - Teach the ideas above, briefly: semiconductors, doping, junctions.
   - Show an oxidised wafer beside a clean one.
   - Groups rule the streets, number the dies, scrape S and draw T.
   - Ask: what is our recipe, and what would we change to test it?
3. **Session 2, wafer sort:**
   - Check every meter on a 1N4148.
   - Each person tests 8 of the 32 dies, Fwd and Rev.
   - Bin each die and fill the wafer map.
   - Compare the centre 16 dies with the edge 16.
4. **Session 3, dicing, final test and binning:**
   - Cut the dies apart, test them again and sort them into the bin trays.
   - Work out each stage's yield and the overall yield.
   - Package the best die, if there's time.

### Yield arithmetic

- **Stage yield** = dies that pass ÷ dies tested at that stage.
- **Overall yield** = the stage yields multiplied together.

For example, with made-up numbers: 24 of 32 dies pass wafer sort (75 %). 20 of those 24 still pass after dicing (83 %). 3 of 4 packages work (75 %). Overall: 0.75 × 0.83 × 0.75 ≈ 47 %.

### Questions for the class

- **Why do dies from one wafer differ?** The hot plate is uneven, and so are the oxide's thickness, the pencil pressure and the light.
- **Where are the good dies?** Look at the wafer map: is there a pattern?
- **Who sets the bin limits, and why?** What would you sell a Bin 3 diode as?
- **Would smaller dies yield better or worse?** Bigger dies are more likely to include a defect. Try it: cut one wafer into 7.5 mm dies.

### Process splits

Real fabs change one thing per batch to tune a recipe. Each group can change one thing, too:

- **Heat time:** 15, 30 or 45 minutes.
- **Cooling:** slowly on the plate, or lifted off with tongs onto a heatproof board.
- **Top contact:** the pencil dot, a pencil point pressed on like a cat's whisker, or bare copper tape pressed on.
- **Foil thickness:** 0.1 mm or 0.2 mm.

## Hazards and supervision

- **Adults only:**
  - running the hot plate
  - handling hot copper
  - craft knives
  - soldering
- **Everyone:**
  - wear goggles near the hot plate and while the copper cools
  - keep the room ventilated
  - no food or drink
  - wash hands after handling oxide
- **Never in T3:**
  - acids (including hydrochloric) and lye
  - lead and galena
  - borax
  - zinc, brass or galvanised metal
  - copper tape or coated foil on the hot plate
  - mains electricity
- **Age:** the standard hasn't settled the audience's age yet (§11). For younger learners, the heating step is a demonstration.

## Open questions

1. **The top contact.** Does a pencil-graphite top contact on Cu₂O rectify the way Grondahl's lead did, and which way is forward?
2. **The hot plate.** Does a 1000 W coil plate get hot enough, and evenly enough? Is 30 minutes right for 0.1–0.2 mm foil, or does thin foil oxidise right through and go brittle?
3. **The black layer.** Does the black CuO come off cleanly without acid, from foil this thin? If some stays, does the die still rectify?
4. **Bin limits.** What spread do real dies show? That sets the `[T3]` limits.
5. **Drift.** Do readings change with light, humidity or time? Retest on day 7.
6. **Dicing.** Do the dies survive scissors, or does cutting crack the oxide at the edges and short them?
7. **Use in a lesson.** Can a packaged die stand in for D1 on L06, at about 9 mA? Does it leak enough to light LED2?
8. **Die size.** Do smaller dies yield better?
9. **PEDOT:PSS.** Do pencil source, drain and back-gate contacts work, and does copy paper gate it without added salt? Is one small bottle enough for a class? This would be a T4 sheet.
10. **Age.** Which steps do learners do, and which are demonstrations? This waits on the standard's audience age (§11).

## Sources

- [Biccari, Malerba, Mittiga (2013), "Impurity effects in Cu₂O"](https://ar5iv.arxiv.org/html/1310.5341): Cu₂O is p-type with a 2.09 eV gap; copper vacancies.
- [Brattain (1951), "The Copper Oxide Rectifier", Rev. Mod. Phys. 23, 203](https://link.aps.org/doi/10.1103/RevModPhys.23.203)
- [Experimental Wireless, January 1928](https://www.worldradiohistory.com/UK/Experimental-Wireless/20s/Experimental%20Wireless-1928-01.pdf): Grondahl's rectifier and its easy direction.
- [sci-toys: a solar cell in your kitchen](https://sci-toys.com/scitoys/scitoys/echem/echem2.html): hot plate oxidation, slow cooling, output.
- [H. P. Friedrichs: cuprous oxide diode](https://hpfriedrichs.com/radioroom/cu-diode/rr-cu-diode.htm): a hobbyist's diodes, ratios and failures.
- [Rimstar: homemade solar cell](https://www.rimstar.org/renewnrg/sp_diy_homemade_solar_cell.htm)
- [Wikipedia: Metal rectifier](https://en.wikipedia.org/wiki/Metal_rectifier), [Copper(I) oxide](https://en.wikipedia.org/wiki/Copper(I)_oxide), [Doping](https://en.wikipedia.org/wiki/Doping_(semiconductor)), [Crystal detector](https://en.wikipedia.org/wiki/Crystal_detector), [Foxhole radio](https://en.wikipedia.org/wiki/Foxhole_radio), [Electrolytic rectifier](https://en.wikipedia.org/wiki/Electrolytic_rectifier), [Organic electrochemical transistor](https://en.wikipedia.org/wiki/Organic_electrochemical_transistor), [Wafer testing](https://en.wikipedia.org/wiki/Wafer_testing), [Product binning](https://en.wikipedia.org/wiki/Product_binning), [Draper point](https://en.wikipedia.org/wiki/Draper_point), [Metal fume fever](https://en.wikipedia.org/wiki/Metal_fume_fever)
- [Techneglas: dopant sources](https://www.techneglas.com/dopant-sources/dopant-advantages/), and [Baidu wiki: diffusion furnace](https://b2bwiki.baidu.com/en/encyclopedic/semiconductor-diffusion-furnace) for furnace temperatures.
- [Sozen et al. (2024), "Flexible Phototransistors on Paper: Scalable Fabrication of PEDOT:PSS Devices Using a Pen Plotter", Small Science 4, 2400063](https://doi.org/10.1002/smsc.202400063)
- [Nilsson et al., "All-organic electrochemical device with bistable and dynamic functionality", Proc. SPIE 5051](https://journals.spiedigitallibrary.org/conference-proceedings-of-spie/5051/0000/All-organic-electrochemical-device-with-bistable-and-dynamic-functionality/10.1117/12.484380.full)
- [Ossila: PEDOT:PSS PH 1000](https://www.ossila.com/products/pedot-pss-ph-1000) and [an Ossila PEDOT:PSS safety data sheet](https://downloads.ossila.com/msds/p-jet-x-n-pedot-pss.pdf)
- PEDOT:PSS secondary doping: [sorbitol (2017)](https://eurekamag.com/research/083/369/083369012.php), [sorbitol as a processing additive (2008)](https://heibib.ub.uni-heidelberg.de/search/Record/1684196213), [glycerol: Tsai et al. (2008), Proc. SPIE 7052](https://scholars.lib.ntu.edu.tw/handle/123456789/155690?&locale=en)
- [onetuberadio: 1928 power supply with homemade rectifiers](https://onetuberadio.com/2018/03/12/1928-power-supply-with-homemade-rectifiers/)
- [Council of the EU, ST 8424/09 ADD 2](https://data.consilium.europa.eu/doc/document/ST-8424-2009-ADD-2/de/pdf): borate classification, Repr. 1B H360FD.
- [Irhayem and Al-Mayalee (2025), "Structural, Optical, and Photo Detecting Properties of Radial CuO/ZnO/Si Nanostructured Heterojunction", J. Nanostructures 15(3)](https://jns.kashanu.ac.ir/article_114866_60307aa5dbb489271476b8aa117aca3b.pdf) and [US patent 12201753](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12201753): ZnO and CuO growth; CuO is p-type.
- [Fluke: how to test diodes with a digital multimeter](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes)
