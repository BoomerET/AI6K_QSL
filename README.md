# Wavelog QSL Studio

**Wavelog QSL Studio** is a companion application for [Wavelog](https://github.com/wavelog/wavelog) that helps amateur radio operators design, preview, and print professional physical QSL cards using contact information from their Wavelog logbook.

The application is designed around a practical hybrid workflow:

1. A commercial printer produces high-quality, full-color QSL cards with a common front design.
2. Wavelog QSL Studio retrieves an individual QSO from Wavelog.
3. The operator feeds one preprinted card into a local printer.
4. Wavelog QSL Studio prints the contact-specific information onto the back.

This approach combines professional front-side printing with inexpensive, on-demand personalization at home.

## Project Status

Wavelog QSL Studio is under active development and is not yet ready for general production use.

The current codebase includes early support for:

* Connecting to a Wavelog instance
* Retrieving QSOs
* Selecting contacts through a web interface
* Rendering QSL card layouts from YAML templates
* Generating PDF output
* Configurable print layouts and printer calibration

The project is currently being refocused around **individual 5.5 × 3.5-inch QSL card printing** rather than printing multiple cards on perforated Letter-size sheets.

## Primary Workflow

The intended everyday workflow is:

```text
Select a QSO from Wavelog
            │
            ▼
Preview the QSL card back
            │
            ▼
Insert one preprinted card
            │
            ▼
Print the contact information
            │
            ▼
Record the card as printed
```

The front of the card is expected to be professionally printed in advance. Wavelog QSL Studio prints only the variable information associated with an individual radio contact.

## Goals

Wavelog QSL Studio aims to provide:

* A simple connection to self-hosted Wavelog instances
* Accurate retrieval of QSO and station-location information
* A visual preview of the finished QSL card
* Direct printing to individual 5.5 × 3.5-inch cards
* Configurable layouts without modifying application code
* Printer-specific alignment and calibration
* Support for multiple station locations and callsigns
* A guided queue for printing several cards one at a time
* A record of which QSOs have already received a physical card
* Reusable and shareable QSL card designs

## Non-Goals

Wavelog QSL Studio is not intended to:

* Replace Wavelog as an amateur-radio logbook
* Provide a full desktop-publishing environment
* Control printers directly at the operating-system level
* Compensate for every consumer printer or driver limitation
* Produce full-bleed color artwork on home printers
* Act as a commercial variable-data printing service
* Require QSL cards to be formatted as mailable postcards

Cards may be mailed inside envelopes, so layouts do not need postage boxes, postal address areas, barcode clearances, or postcard dividers.

## Card Format

The initial target card format is:

* **Finished size:** 5.5 × 3.5 inches
* **Orientation:** Landscape
* **Front:** Professionally preprinted
* **Back:** Printed individually by the operator
* **Delivery:** Normally enclosed in an envelope

The back layout can therefore use the available space for amateur-radio information rather than postal formatting.

Typical content may include:

* Contact callsign
* QSO date and UTC time
* Frequency or band
* Operating mode
* Signal report sent
* Signal report received
* Station callsign
* Maidenhead grid square
* Operator name and location
* Equipment or antenna information
* QSL confirmation message
* Free-form comments
* Signature or station logo

## Design Model

The application separates card design from printer behavior.

### Layout

A layout defines the position and size of elements on the card, including:

* Text
* Lines
* Borders
* Tables
* Images
* Logos
* Static labels
* Dynamic Wavelog fields

Layouts are expected to be configurable through YAML files.

### Theme

A theme defines the visual presentation of a layout, including:

* Fonts
* Font sizes
* Colors
* Border styles
* Background treatments
* Logos and decorative assets

Separating themes from layouts may allow operators to reuse the same field placement with different visual designs.

### Printer Profile

A printer profile describes how a specific printer handles an individual QSL card, including:

* Card width and height
* Feed orientation
* Leading edge
* Printable side
* Horizontal offset
* Vertical offset
* Horizontal scale
* Vertical scale

Printer profiles should be reusable once calibrated.

## Calibration

Consumer printers do not always place small media exactly where software expects. Wavelog QSL Studio will include a calibration workflow that generates a test card with:

* An inset border
* Center lines
* Measurement marks
* Orientation labels
* A clearly identified leading edge
* Safe-area indicators

Users can print the calibration design on inexpensive blank stock before using professionally printed cards.

Calibration settings will then be saved in the selected printer profile.

## Planned Features

### Initial Release

* Wavelog API configuration
* QSO search and selection
* Single-card back preview
* Exact 5.5 × 3.5-inch PDF generation
* Individual-card printing
* YAML-based layouts
* Printer profiles
* Calibration test card

### Later Releases

* Multiple back layouts
* Theme support
* Print history
* Reprint support
* Marking QSOs as printed
* Guided one-card-at-a-time print queue
* Multiple Wavelog station locations
* Callsign and station-profile selection
* Signature images
* Club and award logos
* Envelope-address printing
* Importable and shareable community templates
* Improved accessibility and mobile-friendly controls

## Proposed Version Roadmap

### Version 0.2 — Individual Card Printing

* Remove perforated-sheet printing from the primary workflow
* Generate one 5.5 × 3.5-inch PDF page per QSO
* Add a single-card preview
* Add printer feed instructions
* Support basic printer offsets

### Version 0.3 — Calibration and Templates

* Add a guided calibration page
* Save reusable printer profiles
* Support multiple back layouts
* Improve template validation
* Add safe-area warnings

### Version 0.4 — Print Management

* Add a print queue
* Track printed and reprinted QSOs
* Add one-at-a-time batch guidance
* Improve Wavelog synchronization

### Version 1.0 — Community Release

* Polished installation process
* Complete documentation
* Template examples
* Stable configuration format
* Error handling and diagnostics
* Release packaging
* Community-ready branding and screenshots

## Architecture

Wavelog QSL Studio is currently built with:

* Python
* FastAPI
* Uvicorn
* Apache or another reverse proxy
* YAML configuration
* Server-side PDF generation
* HTML, CSS, and JavaScript for the web interface

A typical deployment may run alongside Wavelog in a home lab or on a small Linux server.

```text
Web Browser
     │
     ▼
Wavelog QSL Studio
     │
     ├── Wavelog API
     ├── Layout and theme files
     ├── Printer profiles
     └── PDF renderer
              │
              ▼
       Individual QSL card
```

## Configuration

The final configuration structure is still evolving. It is expected to include files similar to:

```text
config/
├── application.yaml
├── wavelog.yaml
├── printer_profiles.yaml
└── station.yaml

templates/
├── back/
│   └── default.yaml
└── themes/
    └── default.yaml

assets/
├── logos/
├── signatures/
└── images/
```

Sensitive values such as Wavelog API keys should not be committed to source control.

## Development Principles

The project follows several guiding principles:

1. **Wavelog remains the source of truth.**
   QSO and station data should come from Wavelog whenever possible.

2. **Printing should be predictable.**
   A user should be able to calibrate a printer once and reuse that configuration.

3. **Layouts should be data-driven.**
   Users should be able to customize card designs without editing Python code.

4. **The normal workflow should be simple.**
   Selecting and printing a QSL card should require only a few actions.

5. **Physical media should not be wasted.**
   Preview and calibration tools should reduce failed prints.

6. **The application should remain useful beyond one station.**
   Callsigns, station locations, printers, and designs must be configurable.

## Relationship to Wavelog

Wavelog QSL Studio is an independent companion project. It is not an official component of Wavelog unless adopted or endorsed by the Wavelog project in the future.

Wavelog is used as the authoritative source for QSO and station information.

## Contributing

The project is currently in an early design and refactoring phase. Contribution guidelines will be added once the core architecture and configuration formats stabilize.

Future contributions may include:

* Layout templates
* Themes
* Printer profiles
* Documentation
* Wavelog API improvements
* Testing
* User-interface enhancements

## License

A license has not yet been selected.

Before accepting outside contributions or publishing stable releases, the project should adopt an explicit open-source license.

## Acknowledgments

Wavelog QSL Studio is built to complement the excellent work of the Wavelog project and its community.

It is inspired by the long-standing amateur-radio tradition of exchanging physical QSL cards while using modern logging and self-hosted software to make that process easier.
