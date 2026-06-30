// Gives new players the Gigani Silent Gear progression roadmap once.
PlayerEvents.loggedIn(event => {
  const player = event.player
  const data = player.persistentData
  if (data.giganiGearRoadmapGiven) return

  const attempts = [
    () => Item.of('patchouli:guide_book[patchouli:book="gigani:silentgear_roadmap"]'),
    () => Item.of('patchouli:guide_book', { 'patchouli:book': 'gigani:silentgear_roadmap' }),
    () => Item.of('patchouli:guide_book', '{patchouli:book:"gigani:silentgear_roadmap"}')
  ]

  for (const makeBook of attempts) {
    try {
      player.give(makeBook())
      data.giganiGearRoadmapGiven = true
      return
    } catch (err) {
      // Try the next Patchouli item-data format; 1.21 packs differ here.
    }
  }

  player.give('minecraft:book')
  data.giganiGearRoadmapGiven = true
  console.error('[Gigani] Could not create Patchouli roadmap book item; gave a plain book fallback.')
})
