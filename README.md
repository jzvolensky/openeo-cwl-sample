# openeo-cwl-sample

Sample OGC Application Package used to test Zoo-Project-DRU OpenEO Integration

## Description

This CWL workflow is a sample application package to test the integration of the `Zoo-Project-DRU` with our OpenEO backend. All it does it reads a bunch of STAC collections to simulate an OpenEO process data transfer. Then it reads the collections, appends some nonsense metadata and writes the collections into a catalog.

Note: I have specifically maintained the CWL1.0 spec which has full conformance in `Zoo-Project-DRU` as far as I can tell to prevent any `cwltool` and `Zoo-Project-DRU` feature mismatch.

## Usage

Using `params.json`:

```zsh
cd cwl
```

```zsh
cwltool openeo-sample.cwl#openeo-workflow params.json 
```

where the `params.json` file contains the following:

```json
{
  "stac_urls": [
    "https://stac.eurac.edu/collections/MOD10A1v61",
    "https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2",
    "https://stac.eurac.edu/collections/CLC2018"
  ]
}
```

## Usage on the Zoo-Project-DRU

WIP

## Local testing and development

Install using poetry:

```zsh
poetry install
```

Run poetry shell:

```zsh
poetry shell
```
