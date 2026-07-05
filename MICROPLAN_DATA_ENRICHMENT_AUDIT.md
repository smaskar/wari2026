# Microplan Data Enrichment Audit

Source workbook analyzed:
`/Users/santosh/projects/Wari2026/Documents/Pune/Microplan -Ashadhi Wari 2026_01.07.2026.xlsx`

Analysis date: 2026-07-05

## Current App Data Snapshot

The app currently builds 608 public map/list points from the local JS datasets.

| Dataset area | Current count |
| --- | ---: |
| Ambulance pins | 132 |
| Distinct ambulance vehicles | 101 |
| Health/doctor-capable points | 217 |
| Water points | 193 |
| Toilet points | 23 |
| Hirkani booths | 67 |
| Halt/rest/mukkam points | 108 |
| Ambulance pins without primary call number | 19 |
| Health points without doctor/MO field | 41 |
| Points marked `ready: verify` | 370 |

## Workbook Inventory

The workbook has 33 sheets. It is useful, but not directly map-ready: the inspected sheets do not contain latitude/longitude or Google Maps links. Most usable data must be matched to existing mapped places or separately geocoded and manually verified before becoming public directions.

### High-Value Public Enrichment Candidates

| Sheet | Usable rows | Useful fields | Fit for app |
| --- | ---: | --- | --- |
| `Health Facility-Tukaram Maharaj` | 186 | date, district, taluka, mukkam/place, facility name, facility type, OPD/ICU, private hospital count | Good for place-level service richness after matching to mukkam/facility points |
| `Health Facility-Dnyaneshwar Mah` | 220 | date, district, taluka, mukkam/place, facility name, facility type, OPD/ICU, private hospital count | Good for place-level service richness after matching to mukkam/facility points |
| `पाणी स्त्रोतांचीमाहिती- Tukaram` | 53 | place, source-type counts, tanker filling counts, total/tested/potable source counts | Good for water context at mukkam/place level, not exact directions |
| `पाणी स्त्रोतांचीमाहिती-Dnyanesh` | 37 | place, source-type counts, tanker filling counts, total/tested/potable/unsafe source counts | Good for water context at mukkam/place level, not exact directions |

Health facility detail:

| Sheet | हिंदुहृदयसम्राट बाळासाहेब ठाकरे आपला दवाखाना | PHC | Ambulance Pathak variants | ICU rows | OPD rows | Private hospital count total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tukaram | 96 | 17 | 12 | 17 | 158 | 161 |
| Dnyaneshwar | 107 | 14 | 29 | 28 | 139 | 295 |

Water summary:

| Sheet | Total water sources | Tested sources | Potable sources | Unsafe sources | Tanker filling points |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tukaram | 2,594 | 1,006 | 20 | not consistently filled | 98 |
| Dnyaneshwar | 4,530 | 2,988 | 2,006 | 994 | 300 |

## Admin-Only Or Verification-Only Data

These sheets contain rich operational details but should not be shown publicly without a privacy and verification decision.

| Sheet | Rows | Why useful | Why not direct public import |
| --- | ---: | --- | --- |
| `AD-DM Palkhi` | 480 | Dindi pramukh, Arogya Doot, vehicles, supervisors, nodal officers | Heavy personal phone-number content; no coordinates |
| `AD-TM Palkhi` | 620 | Dindi pramukh, Arogya Doot, vehicles, supervisors, nodal officers | Heavy personal phone-number content; no coordinates |
| `AD-Sopan Kaka Palkhi` | 116 | Same structure for Sopan Kaka palkhi | Outside the current two-palkhi public app scope unless scope expands |
| `1.SDH`, `2.Trauma ICU(20)`, `3.Rural-HBT`, `4.Urban-HBT`, `5.Tin Rasta`, `Teen Rasta`, `Reserve` | hundreds each | Staff rosters, departments, shifts, phone numbers | Many dates appear to be 2025; privacy-sensitive |
| `Route ICU & HBT`, `No. -ICU & HBT (3)` | about 100 each | ICU/HBT route structure | Appears to be 2024 planning data |
| `Route Plan-2025`, `Route Plan-2025 (2)` | 147 / 371 | Route structure and HBT lists | Marked 2025; use as reference only until updated |

## Data Quality Notes

- No inspected sheet provides coordinates, so automated map-pin creation would create unverified locations.
- Facility names are not consistently formatted against current app labels. A rough match found only a small direct overlap, especially for हिंदुहृदयसम्राट बाळासाहेब ठाकरे आपला दवाखाना and temporary service points.
- The workbook mixes 2026 health/water planning sheets with 2024/2025 reference/manpower sheets. Do not treat every tab as current 2026 operational truth.
- Several sheets include personal mobile numbers. These are useful for internal operations, but public display should be deliberate and minimal.
- Some data-entry fields are inconsistent or misspelled, e.g. `Vehical`, mixed date text, inconsistent PHC/RH/हिंदुहृदयसम्राट बाळासाहेब ठाकरे आपला दवाखाना spellings, and partial potability data in the Tukaram water sheet.

## Recommended Enrichment Path

1. Extract four public-safe sheets first: the two health facility sheets and the two water-source sheets.
2. Normalize them into a review CSV with source sheet, row number, palkhi, date, mukkam/place, facility/source name, service type, OPD/ICU, and aggregate counts.
3. Match rows to existing app entities in this order: exact mukkam name, known mapped facility, existing water/filling point, then manual review.
4. Add only matched records to a new `wari-microplan-summary.js` module as place-level metadata. Avoid creating new map pins until coordinates are verified.
5. Surface the metadata as context on existing cards and mukkam views, for example:
   - `OPD/ICU services available near this mukkam`
   - `Private hospitals nearby: N`
   - `Water sources tested: X / Y`
   - `Tanker filling points in area: N`
6. Keep AD/staff/roster sheets in an internal admin dataset unless there is explicit approval to publish specific phone numbers.
7. For temporary हिंदुहृदयसम्राट बाळासाहेब ठाकरे आपला दवाखाना/ICU/ambulance pathak points that do not match existing map data, create a manual verification queue with geocoding candidates and source row references.

## Safe Immediate Decision

Use this workbook to enrich the app, but do not bulk-import it directly into public map pins. The best immediate value is place-level service and water-source context tied to existing mapped mukkams/facilities. The next implementation step should be a normalization script and a manual-review CSV, followed by a small UI pass to show verified microplan context on existing cards.
