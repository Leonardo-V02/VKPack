# Publishing Checklist

- Upload dist/GrindingGear-1.0.0+mc1.21.1-neoforge.jar.
- Use MODRINTH_DESCRIPTION.md for the project description.
- Mark the project as NeoForge-only for Minecraft 1.21.1.
- Add hard dependencies:
  - Silent Gear
  - Silent Lib
  - Apotheosis
- Apotheosis will pull its normal dependency chain, but listing Placebo, Apothic Attributes, Apothic Spawners, and Apothic Enchanting as additional dependencies is acceptable if the host allows it.
- Mention that KubeJS is not required.
- Mention that older KubeJS prototype startup scripts must be disabled before installing this jar into migrated packs.