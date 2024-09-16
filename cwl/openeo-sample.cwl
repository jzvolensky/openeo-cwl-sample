cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.0.1
s:dateCreated: '2024-06-05'
s:keywords: OpenEO, EO, CWL, AP, InterTwin, Magic
s:codeRepository: https://github.com/jzvolensky/Itwin-tech-meeting
s:releaseNotes: https://github.com/jzvolensky/Itwin-tech-meeting/blob/main/README.md
s:license: https://github.com/jzvolensky/Itwin-tech-meeting/blob/main/LICENSE
s:author:
  - s:name: Juraj Zvolensky
    s:email: juraj.zvolensky@eurac.edu
    s:affiliation: CWL Enthusiast

$graph:
  - class: Workflow
    id: openeo-workflow
    label: Sample workflow to test OpenEO integration with CWL
    doc: whatever will add this later if neede
    
    inputs:
      stac_urls:
        label: Single STAC Url or a list of STAC Url
        type: string[]

    outputs:
      - id: stac_catalog
        outputSource:
          - node_stac/stac_catalog
        type: Directory
    
    steps:
      node_stac:
        run: "#stac"
        in:
          stac_urls: stac_urls
        out:
          - stac_catalog

  - class: CommandLineTool
    id: stac
    requirements:
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        ramMin: 1024
        ramMax: 4096
        coresMin: 1
        coresMax: 2
    hints:
      DockerRequirement:
        dockerPull: potato55/openeo-cwl-sample:0.1
    baseCommand: ["python3", "/app/read_write_stac.py"]
    arguments: []
    inputs:
      stac_urls:
        type: string[]
        inputBinding:
          position: 1
    outputs:
      stac_catalog:
        outputBinding:
          glob: .
        type: Directory
      