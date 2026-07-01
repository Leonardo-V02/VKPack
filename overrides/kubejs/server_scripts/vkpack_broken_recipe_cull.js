// VKPack stability pass: remove known-broken recipe IDs that produce JEI/runtime
// errors because their backing registry entries are missing in the current mod set.
// This removes recipe entries only; it does not disable the owning mods.

ServerEvents.recipes(event => {
  const brokenRecipeIds = [
    'cataclysm_spellbooks:burning_manuscript',
    'cataclysm_spellbooks:disc_driver_upgrade',
    'cataclysm_spellbooks:engineer_boots',
    'cataclysm_spellbooks:engineer_hood',
    'cataclysm_spellbooks:engineer_leggings',
    'cataclysm_spellbooks:engineer_suit',
    'cataclysm_spellbooks:engineers_power_glove',
    'cataclysm_spellbooks:excel_upgrade_cooldown',
    'cataclysm_spellbooks:excel_upgrade_mana',
    'cataclysm_spellbooks:excel_upgrade_resistence',
    'cataclysm_spellbooks:frozen_tablet',
    'cataclysm_spellbooks:mechanical_brace',
    'cataclysm_spellbooks:murasama',
    'cataclysm_spellbooks:smithing/excelsius_power_chestplate_upgrade',
    'cataclysm_spellbooks:smithing/excelsius_power_visors_upgrade',
    'cataclysm_spellbooks:smithing/excelsius_resist_chestplate_upgrade',
    'cataclysm_spellbooks:smithing/excelsius_resist_visors_upgrade',
    'cataclysm_spellbooks:smithing/excelsius_speed_chestplate_upgrade',
    'cataclysm_spellbooks:smithing/excelsius_speed_visors_upgrade',
    'cataclysm_spellbooks:technomancy_rune',
    'cataclysm_spellbooks:technomancy_upgrade_orb',
    'cataclysm_spellbooks:the_berserker_upgrade',
    'cataclysm_spellbooks:the_combuster_upgrade',
    'cataclysm_spellbooks:the_nightstalker_upgrade',
    'cataclysm_spellbooks:the_ordeal_upgrade',
    'cataclysm_spellbooks:the_subjugator_upgrade'
  ]

  brokenRecipeIds.forEach(id => event.remove({ id: id }))
})
