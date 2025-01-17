## v1.8.0 (2023-04-27)

### Feat

- **templates**: New template type: Token. Now ships with one included token template (credit to Chilli Axe). Emblems are also rolled into this template type. Also implemented better Expansion Symbol positioning and scaling, reworked the rendering chain, implemented better error handling and thread procedures, and merged most transform and MDFC template classes into single classes that can handle both faces
- **threading**: Implemented sophisticated thread tracking, locking, and release. Threads will now shut down properly when the Cancel button is pressed. The Console class was completely rewritten to faciliate management of the current render thread. "Render Target" can now select more than one card art to render
- **settings**: Added new settings. Scryfall Sorting: Change order of Scryfall results. Watermark Default Opacity: Change the defeault opacity of generated Watermarks. Renamed Dev mode to Test mode. Implemented get_default_symbol utility function

### Fix

- **text_layers**: Implemented new properties governing scaling behavior such as scale_height, scale_width, fix_overflow_width, fix_overflow_height. Added a step that ensures text does not overflow the bounding box of the text area when needed
- **fonts**: Updated the NDPMTG font to fix Phyrexian hybrid and implement acorn symbol

### Refactor

- **templates**: Move duplicate filename logic to file utils
- **frame_logic**: Completely rewrote the frame logic step for efficiency, introduced efficient mapping and utility function to find the correctly ordered color identity sequence. Creators can now use this sequence to implement 3+ color frame elements with accuracy
- **expansion_symbols.json**: Updated symbol library, removed reference keys as they are now deprecated
- **constants**: Updated constants object to use new env variables, added new utility methods, added new lock objects, added global PhotoshopHandler object
- **plugins**: Updated included plugins to use new LAYERS library and updated console handler
- **tests,-build,-deps**: Added pathvalidate dependency, updated tests, implemented env module for tracking environment variables and flags
- **img**: Renamed some preview images and SVG symbol directories
- **update**: Refactored download functions for better readability
- **enums_layers**: Moved our layer names library to a StrEnum class, con.layers refrences this
- **modules**: Implemented module utilities for retrieving and refreshing plugin modules
- **objects**: Implemented a PhotoshopHandler class to maintain one global Photoshop Application instance and refresh across new threads
- **scryfall**: Updated scryfall set utilities to support token cards
- **utils.strings**: Moved headless console to string utilities, updated console output utility functions
- **utils**: Added import comments, implemented new types and updated existing types

### Perf

- **format_text**: Improved execution time on multiple format_text functions, refactored SymbolMapper, implemented new function scale_text_to_fit_textbox
- **helpers**: Improved efficiency of some helper functions. Introduced new helpers: check_textbox_overflow, get_textbox_bounds, get_textbox_dimensions, enable/disable_vector_mask, undo/redo_action, convert_points_to_pixels, check_active_document, get_document
- **regex**: Implemented a regex pattern dataclass to pre-compile all regex patterns used by the app

## v1.7.0 (2023-04-06)

### Feat

- **settings**: Importing scryfall art for reference is now a toggle setting, has been removed from individual templates in favor of a base template function that can be modified by child classes
- **gui**: Settings for each template can now be cleared to defaults with a helpful button, templates will now be disabled unless the PSD file is installed, the updater will enable the template after a download is complete
- **scryfall**: Rewrote Scryfall data collection completely to use efficient rate limiting and error handling as well as improved caching and overall execution time of this step
- **settings**: Seperate core system settings from the base template settings which can be overwritten for each template

### Fix

- **classic**: Fixed promo star setting on classic templates
- **creature**: Fix mistake in creature vertically nudge text function
- **dev_mode**: Skip uninstalled templates during dev mode testing
- **planeswalker**: Update Planeswalker logic to enforce uniform spacing for 2 ability Planeswalkers
- **layouts**: Fixed a bug affecting Saga and Class cards that have multiline abilities
- **frame_logic**: Fixed frame logic for ca1rds like Maelstrome Muse and Ajani, Sleeper Agent and added both to our test cases
- **creator**: Custom Creator now works for Planeswalker and Saga cards again
- **updater**: Fix templates downloading to incorrect folder

### Refactor

- **planeswalker**: Adjust vertically nudge text function
- **helpers**: Updated getLayer(), getLayerSet(), spread_layers_over_reference(), and art importing functionality
- **format_text**: Added new text function check_for_text_overlap() and refactored the vertical nudge functions for Creature and Planeswalker cards
- **data**: Update project toml, fonts,  and expansion symbol data

## v1.6.0 (2023-03-16)

### Feat

- **settings**: New Setting: Template Border, default is black. Other options are white, silver and gold
- **template**: New Template: Universes Beyond, used in crossover sets like WH40K, Transformers, etc
- **expansion_symbol**: Rewrite expansion symbol settings to allow 4 distinct modes, including SVG
- **watermarks**: Add support for optional Watermark generation
- **fonts**: New font utility functions: register_font(), unregister_font(), get_all_fonts(), check_fonts()
- **helpers**: New helper functions: set_fx_visibility(), enable_layer_fx(), disable_layer_fx(), set_fill_opacity(), apply_fx_color_overlay()
- **files**: Restructure directory structure, allow self contained plugins

### Fix

- **settings**: Back face to MDFC/Transform now uses the same ini as front face
- **console**: Add missing newline
- **symbols**: Updated some expansion symbols
- **kivy**: Replace unused MPlantin font with PlantinMTPRo
- **scryfall**: Improved MTG Set data caching to fix inconsistencies with collector information
- **sketch**: Fix bug causing some pencil sketch filters to fail
- **constants**: Fix cwd not working properly in executable version

### Refactor

- **tests**: Update tests for directory restructure and expansion symbol rewrite
- **layouts**: Improve handling of card_count, pre-cache set data, reorganize properties pertaining to all double faced cards
- **SilvanMTG**: Remove default configurations for cfg.remove_reminder
- **types_photoshop**: Specify NotRequired for some values

## v1.5.0 (2023-03-02)

### Feat

- **expansion-symbol**: New layer effects helpers implemented, Expansion Symbol now rendered using these effects
- **helpers**: Import art directly into the document, add new helper utilities
- **templates**: New template type: Class

### Fix

- **ixalan**: Ixalan now renders without an error at create_expansion_symbol()
- **layouts**: Transform front sides now work when name is lowercase
- **layouts**: Added support for meld transform icon, added support for non-Ixalan back face lands
- **symbols**: Add support for ONE, ONC, DMR, and SCD
- **console**: Improve error logging dramatically
- **fonts**: Updated keyrune font to latest
- **layouts**: Patch a bug that causes alternate language to not identify creatures

### Refactor

- **helpers**: Deprecated solidcolor(), Added new helpers
- **layouts**: BaseLayout > NormalLayout, made BasicLandLayout extend to NormalLayout
- **cwd**: Use con.cwd to find the current directory across Proxyshop, always use root directory of project
- **DoubleFeature**: Explicit definitions for layer groups
- **creator**: Added scryfall formatting step to custom creator which in the future will help keep data in-line with what is expected for the layout object
- **symbols**: Allow use of old Expansion Symbol rendering, pending potential future deprecation
- **frame_logic**: Improved formatting and refactored
- **format_text**: Code readability improvements

## v1.4.0 (2023-01-30)

### Feat

- **saga**: Implemented full automation for sagas
- **symbols**: Update symbol library and template manifest on launch
- **gui**: Add preview image to showcase each template
- **settings**: New automatic settings panels

### Fix

- **CrimsonFangTemplate**: Fixed dual color frame generation
- **settings**: Additional fixes for new panel config system
- **frame_logic**: Fix frame logic for some transform cards
- **settings**: Small patches to settings logic
- **creator**: Fix template logic for creator tab
- **scryfall**: Add special exception for championship cards
- **expansion_symbol**: Default stroke now uses config value
- **meld**: Fix meld card layout data

### Refactor

- **planeswalker**: Refactored planeswalker text generation
- **templates**: Add scaling to Planeswalker spacing
- **configs**: Rename configs to match new nomenclature
- **settings**: Rewrite settings to use class name for ini/json naming convention
- **layouts**: Trimmed down layout classes and properties
- **frame_logic**: Add FrameDetails type
- **sketch**: Switch sketch config to new settings system
- **plugin-templates**: Make adjustments to included plugin templates
- **templates**: Remove useless print statements
- **symbols**: Add missing symbols to library
- **config**: Reformat config for Kivy settings panel
- **text_layers.py**: Refactored classic quote alignment
- **gui**: Seperate GUI elements into modules

## v1.3.0 (2023-01-06)

### Fix

- **updater**: Fixed Google Drive downloads, moved S3 downloading to Cloudfront

### Refactor

- **__env__**: Moved environment variables to py file
- **gui.py**: Removed unnecessary newline
- **templates.py**: Added app reference to BaseTemplate as property
- **main.py**: Added proper version tracking, refactored console output
- **constants**: Update HTTP header used for requests
