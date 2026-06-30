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
})
