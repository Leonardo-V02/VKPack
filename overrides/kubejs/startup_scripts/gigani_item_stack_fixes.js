ItemEvents.modification(event => {
  const stackTo64 = id => {
    try {
      event.modify(id, item => {
        if (typeof item.kjs$setMaxStackSize === 'function') {
          item.kjs$setMaxStackSize(64)
        } else if (typeof item.setMaxStackSize === 'function') {
          item.setMaxStackSize(64)
        } else {
          item.maxStackSize = 64
        }
      })
    } catch (error) {
      console.warn(`[Gigani] Skipped stack-size fix for missing item ${id}: ${error}`)
    }
  }

  if (typeof Platform !== 'undefined' && Platform.isLoaded('adorablehamsterpets')) {
    stackTo64('adorablehamsterpets:green_beans')
    stackTo64('adorablehamsterpets:steamed_green_beans')
  }
  // Coal coke fuel: coal is 1600 ticks, so coke is 2x coal for furnace-style consumers.
  const setBurnTime = (id, ticks) => {
    try {
      event.modify(id, item => {
        if (typeof item.kjs$setBurnTime === 'function') {
          item.kjs$setBurnTime(ticks)
        } else if (typeof item.setBurnTime === 'function') {
          item.setBurnTime(ticks)
        } else {
          item.burnTime = ticks
        }
      })
    } catch (error) {
      console.warn(`[Gigani] Skipped coal coke fuel fix for missing item ${id}: ${error}`)
    }
  }

  ;[
    'immersiveengineering:coal_coke',
    'immersiveengineering:coke',
    'electrodynamics:coalcoke'
  ].forEach(id => setBurnTime(id, 3200))

  setBurnTime('immersiveengineering:dust_coke', 800)
})
