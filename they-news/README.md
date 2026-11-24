# THEY NEWS

Because everything is a psy-op.

Vertical 1080x1920 clips. Jessie sits in the circle on the left, the scene plays on the right, and the words land at the bottom as ransom-note cutouts. Every episode flips between glasses off (the front message, in color) and glasses on (black and white, aliens revealed, the real message). Every clip ends on OBEY, a red spray-painted counter-message, and the BROBOTS.SPACE plate with the voiced tag line.

## Run it

```
cd they-news/engine && python3 cut.py          # slices art/they-live sheets into cuts/ (once)
cd ../episodes/ep7-pyramid-receipts
python3 spec.py                                 # renders the mp4 next to the spec
python3 spec.py still 12 30                     # stills at 12s and 30s, for checking layout
```

Needs Python 3 with numpy, scipy and Pillow, plus ffmpeg. The music bed goes at `music/bed.wav` (not in the repo, drop in any loopable track).

## Make a new episode

1. Copy any `episodes/epN-*` folder.
2. Generate the voice lines as wav files into that folder. The episodes so far used Speko: glasses-off voices vary per story (Deepgram zeus and athena, Soniox Daniel and Adrian, Inworld Edward, OpenAI coral, ash, nova, shimmer, Rime walnut). The glasses-on translator is always OpenAI `onyx` on `gpt-4o-mini-tts` with "cold, flat, slow monotone, hypnotic, like a subliminal command."
3. Edit `SEGS` in `spec.py`. Each segment is one side of a flip:
   - `mode`: `off` or `on`
   - `screen`: which drawn screen to show (write a function, add it to `SCREENS`)
   - `audio`: list of `(wav name, start offset)`
   - `caps`: ransom-note captions `(start, end, TEXT)`
   - `figs`: cutout figures on the right, `(cut name, x offset, optional scale)`
   - `jessie`: `(time, pose)` changes for the circle
4. Finish with an `on` segment using `screen='end'` then `'end_g'` (OBEY plus spray paint), `brand=` time for the plate, and `('tag', ...)` audio for "Because everything is a psy-op."

Segment lengths size themselves to the audio, and the flip effects (click, red/cyan split, flash, boom) drop in automatically wherever the mode changes.

## Art notes

- Jessie: use the `jessie-cool-*` set (blue eyes, calm). Skip `jessie-cool-glasses-worn-03` and `-06`, they came out without glasses.
- Couple: `fullbody-regular-*` and `fullbody-alien-*` poses 01 to 16 line up for clean swaps. Woman 03, 06 and 08 on the regular 01-08 sheet are framed differently from their alien versions.
- Engine draws its figures flipped so they face the screen.

## Episodes so far

| folder | story |
|---|---|
| ep1-cloudy-day | weatherman, chemtrails (older single-file builder, `build.py`) |
| ep2-the-king-returns | Nvidia reinstates Jensen Huang, Newt's tweet, reply war |
| ep3-pause-yours | Bernie's "pause advanced AI" post |
| ep4-fish-lady | viral office story, she's the alien |
| ep5-lead-dust | Iowa Army lead azide detonation, MTG tweet |
| ep6-copy-paste | "what is the mental illness called" copypasta |
| ep7-pyramid-receipts | Donini's erosion dating of the Great Pyramid |
