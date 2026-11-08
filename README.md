# Reel Factory

Everything for The Automated Minute (Dinny) and Skin Eats (Ipo): art, farm photos, finished episodes, the build engine, and the rules.

Read RULES.md first.

## Folders

- `shows/automated-minute/` Episodes 1 and 2: page, MP4, voice file, script
- `shows/skin-eats/` Part 1 page
- `art/dinny/` 16 Dinny expressions, cut out (plus the original sheet)
- `art/ipo/` 16 Ipo expressions, cut out (plus the original sheet)
- `art/scenes/` 64 cutaway scenes: Dinny, happy owners, stressed owners, bots at work
- `art/brand/` Fruity Puppy label, Moon Tea bottle, Dinny badge, Kudoken logo and coin, set backdrop
- `photos/farm/` Real farm photos cropped for the lab window
- `photos/farm-originals/` Real farm photos, full size
- `engine/` Scripts that time captions to a voice file, mix sound effects, and render the MP4
- `prompts/` Prompts for Grok and Muse

## Making a new episode

1. Write the script. Record it in ElevenLabs. Save the mp3.
2. `engine/align.py` lines each word up with the voice.
3. Write a spec (see `shows/automated-minute/ep2-spec.json`): which face and which scene on each line.
4. `engine/build.py` builds the page and the sound mix.
5. `engine/record.js` plus `engine/assemble.py` render the 1080x1920 MP4.
