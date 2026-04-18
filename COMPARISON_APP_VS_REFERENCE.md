# Perbandingan App vs Sheet Referensi Kode

Sumber pembanding:
- App: `app.py` + `constants.py`
- Referensi: `Rusted Warfare_ Unit Modding Reference.xlsx` (sheet **1.16**)

## Ringkasan

- Struktur inti sudah cocok untuk section utama unit Rusted Warfare: `[core]`, `[graphics]`, `[attack]`, `[movement]`, `[ai]`, serta multi-section seperti `turret_`, `projectile_`, `action_`, `animation_`, `canBuild_`, `leg_`, `attachment_`, `effect_`, `placementRule_`, `resource_`, dan `decal_`.
- App belum mencakup beberapa entri yang ada di sheet referensi 1.16, terutama `arm_`, `hiddenAction_`, `global_resource_`, `comment_`, `template_`, dan item non-section seperti `logicBoolean_` / `spawnUnits:LIST` / `spawnProjectiles:LIST`.
- `mod-info.txt` sudah didukung untuk import field manifest utama (`title`, `description`, `id`, `tags`, `minVersion`, `requiredMods`, `requiredModsMessage`).

## Detail Kecocokan Section

### 1) Single sections (cocok)
- `[core]`
- `[graphics]`
- `[attack]`
- `[movement]`
- `[ai]`

### 2) Multi sections (cocok)
- `turret_NAME`
- `projectile_NAME`
- `action_NAME`
- `animation_NAME`
- `canBuild_NAME`
- `leg_`
- `attachment_`
- `effect_NAME`
- `placementRule_NAME`
- `resource_NAME`
- `decal_NAME`

### 3) Ada di sheet 1.16, belum terwakili penuh di app
- `arm_` (sheet menuliskan `leg_ OR arm_`; app hanya punya mapping `leg_`)
- `hiddenAction_NAME` (sheet menuliskan `action_NAME OR hiddenAction_NAME`; app hanya mapping `action_`)
- `global_resource_NAME` (app hanya mapping `resource_`)
- `comment_NAME`
- `template_NAME`
- `logicBoolean_` (bukan section mandiri, tapi referensi logika lintas field)
- `spawnUnits:LIST`
- `spawnProjectiles:LIST`

## Detail Dukungan Import

- Import file `.ini`, `.copyfrom`, dan `.template` sudah didukung.
- Parser mengenali section sederhana (`core`, `graphics`, `attack`, `movement`, `ai`) dan section multi berbasis prefix.
- Batas import:
  - maksimal 300 unit
  - maksimal 80 asset

## Kesimpulan

Secara umum app **sudah aligned** untuk workflow modding yang paling sering dipakai pada unit editor (single + multi section utama). Gap paling penting dibanding sheet referensi 1.16 ada pada dukungan `arm_`, `hiddenAction_`, dan `global_resource_`, ditambah beberapa fitur lanjutan (`comment_`, `template_`, serta list/logic helper).
