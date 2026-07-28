# R34Sch Changelog

## 1.2
- Removed metadata writing (metadata.py)
- Added filtering options:
- 1. Exclude AI (Improved) (--exclude-ai)
- 2. Only Images (--only-image)
- 3. Only Videos (--only-video)
- 4. Rating (safe, questionable, explicit) (-r)
- Support for searching (-s)
- Randomize posts (-R)
- Cache/History support:
- - -c for clearing cache folder
- - -l for listing cache (history)
- - -d <archive> for deleting a specific archive
- Download from ID support (-I)
- -i (--images) renamed to -n (--number)
- Support for viewing info (metadata) of a post (if -I is passed) or posts (-i)
- Verbose (-v)

## 1.11
- Fixed progress bar overflowing
- Renamed r34sch_config.cfg to just r34sch.cfg
- Removed unnecessary Windows R34Sch folder placement
- Added cookies thru config file to the original parser
- Added option to skip writing to metadata: `--skip-metadata`
- Added `--exclude-ai` option: when searching, it excludes everything that has `ai_` at the start of a tag

## 1.1

- Added API Support (see README for configuration)
- Metadata writing to files
- Better UI
- r34sch_config.cfg Config file

**At 1.2 we're gonna add more options, caching & history, full rule 34 search on the terminal (autocomplete included), and much more! :D**
