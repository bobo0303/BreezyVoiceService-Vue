<template>
  <div class="fixed inset-0 pointer-events-none z-50">
    <!-- Render five pets -->
    <div
      v-for="(pet, index) in pets"
      :key="pet.id"
      class="absolute bottom-0"
      :class="{ 'cursor-pointer pointer-events-auto': pet.isClickable }"
      :style="getPetStyle(pet)"
      @click="handlePetClick(index)"
    ></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Import all GIF images
import slimeMove from '@/assets/pet/Slime/move.gif'
import slimeMoveR from '@/assets/pet/Slime/move-r.gif'
import slimeStand from '@/assets/pet/Slime/stand.gif'
import slimeStandR from '@/assets/pet/Slime/stand-r.gif'
import slimeDie from '@/assets/pet/Slime/die.gif'
import slimeDieR from '@/assets/pet/Slime/die-r.gif'
import slimeHit from '@/assets/pet/Slime/hit.gif'
import slimeHitR from '@/assets/pet/Slime/hit-r.gif'
import slimeJump from '@/assets/pet/Slime/jump.gif'
import slimeJumpR from '@/assets/pet/Slime/jump-r.gif'

import pigMove from '@/assets/pet/Pig/move.gif'
import pigMoveR from '@/assets/pet/Pig/move-r.gif'
import pigStand from '@/assets/pet/Pig/stand.gif'
import pigStandR from '@/assets/pet/Pig/stand-r.gif'
import pigDie from '@/assets/pet/Pig/die.gif'
import pigDieR from '@/assets/pet/Pig/die-r.gif'
import pigHit from '@/assets/pet/Pig/hit.gif'
import pigHitR from '@/assets/pet/Pig/hit-r.gif'
import pigJump from '@/assets/pet/Pig/jump.gif'
import pigJumpR from '@/assets/pet/Pig/jump-r.gif'

import greenMove from '@/assets/pet/Green Mushroom/move.gif'
import greenMoveR from '@/assets/pet/Green Mushroom/move-r.gif'
import greenStand from '@/assets/pet/Green Mushroom/stand.gif'
import greenStandR from '@/assets/pet/Green Mushroom/stand-r.gif'
import greenDie from '@/assets/pet/Green Mushroom/die.gif'
import greenDieR from '@/assets/pet/Green Mushroom/die-r.gif'
import greenHit from '@/assets/pet/Green Mushroom/hit.gif'
import greenHitR from '@/assets/pet/Green Mushroom/hit-r.gif'

import blueMove from '@/assets/pet/Blue Mushroom/move.gif'
import blueMoveR from '@/assets/pet/Blue Mushroom/move-r.gif'
import blueStand from '@/assets/pet/Blue Mushroom/stand.gif'
import blueStandR from '@/assets/pet/Blue Mushroom/stand-r.gif'
import blueDie from '@/assets/pet/Blue Mushroom/die.gif'
import blueDieR from '@/assets/pet/Blue Mushroom/die-r.gif'
import blueHit from '@/assets/pet/Blue Mushroom/hit.gif'
import blueHitR from '@/assets/pet/Blue Mushroom/hit-r.gif'
import blueJump from '@/assets/pet/Blue Mushroom/jump.gif'
import blueJumpR from '@/assets/pet/Blue Mushroom/jump-r.gif'

import prickMove from '@/assets/pet/prick/move.gif'
import prickMoveR from '@/assets/pet/prick/move-r.gif'
import prickStand from '@/assets/pet/prick/stand.gif'
import prickStandR from '@/assets/pet/prick/stand-r.gif'
import prickDie from '@/assets/pet/prick/die.gif'
import prickDieR from '@/assets/pet/prick/die-r.gif'

// Pet type definition
interface PetType {
  name: string
  folder: string
  animations: {
    move: string
    moveR: string
    stand: string
    standR: string
    die: string
    dieR: string
    hit?: string
    hitR?: string
    jump?: string
    jumpR?: string
  }
}

// Define all available pet types
const petTypes: PetType[] = [
  {
    name: 'Slime',
    folder: 'Slime',
    animations: {
      move: slimeMove,
      moveR: slimeMoveR,
      stand: slimeStand,
      standR: slimeStandR,
      die: slimeDie,
      dieR: slimeDieR,
      hit: slimeHit,
      hitR: slimeHitR,
      jump: slimeJump,
      jumpR: slimeJumpR,
    },
  },
  {
    name: 'Pig',
    folder: 'Pig',
    animations: {
      move: pigMove,
      moveR: pigMoveR,
      stand: pigStand,
      standR: pigStandR,
      die: pigDie,
      dieR: pigDieR,
      hit: pigHit,
      hitR: pigHitR,
      jump: pigJump,
      jumpR: pigJumpR,
    },
  },
  {
    name: 'Green Mushroom',
    folder: 'Green Mushroom',
    animations: {
      move: greenMove,
      moveR: greenMoveR,
      stand: greenStand,
      standR: greenStandR,
      die: greenDie,
      dieR: greenDieR,
      hit: greenHit,
      hitR: greenHitR,
    },
  },
  {
    name: 'Blue Mushroom',
    folder: 'Blue Mushroom',
    animations: {
      move: blueMove,
      moveR: blueMoveR,
      stand: blueStand,
      standR: blueStandR,
      die: blueDie,
      dieR: blueDieR,
      hit: blueHit,
      hitR: blueHitR,
      jump: blueJump,
      jumpR: blueJumpR,
    },
  },
  {
    name: 'Prick',
    folder: 'prick',
    animations: {
      move: prickMove,
      moveR: prickMoveR,
      stand: prickStand,
      standR: prickStandR,
      die: prickDie,
      dieR: prickDieR,
    },
  },
]

// Pet interface definition
interface Pet {
  id: number
  type: PetType // Pet type
  position: number // Position percentage (0-100)
  direction: 'left' | 'right' | 'idle' | 'dying' | 'dead' | 'hit' | 'jump'
  isMoving: boolean
  lastDirection: 'left' | 'right'
  opacity: number // Opacity (0-1)
  isClickable: boolean // Whether clickable
  maxHp: number // Maximum health
  currentHp: number // Current health
  jumpHeight: number // Jump height (0 for ground)
}

// Randomly select pet type
const getRandomPetType = (): PetType => {
  const randomIndex = Math.floor(Math.random() * petTypes.length)
  return petTypes[randomIndex]
}

// Create five pets
const pets = ref<Pet[]>([])

// Initialize pets
const initializePets = () => {
  console.log('Initializing pets...')
  for (let i = 0; i < 5; i++) {
    const petType = getRandomPetType()
    const initialDirection = Math.random() > 0.5 ? 'right' : 'left'
    const maxHp = Math.floor(Math.random() * 3) + 1 // Random 1-3 health
    const newPet: Pet = {
      id: i,
      type: petType, // Randomly select pet type
      position: Math.random() * 80 + 10, // 10-90% random position
      direction: initialDirection,
      isMoving: true,
      lastDirection: initialDirection,
      opacity: 1, // Fully opaque
      isClickable: true, // Can be clicked
      maxHp: maxHp,
      currentHp: maxHp,
      jumpHeight: 0, // Initially on ground
    }
    console.log(
      `Creating pet ${i}:`,
      newPet.type.name,
      'at position',
      newPet.position,
      'HP:',
      newPet.maxHp,
    )
    pets.value.push(newPet)
  }
  console.log('Total pets created:', pets.value.length)
}

// Calculate individual pet style
const getPetStyle = (pet: Pet) => {
  let backgroundImage = ''
  const animations = pet.type.animations

  switch (pet.direction) {
    case 'left':
      backgroundImage = `url(${animations.move})`
      break
    case 'right':
      backgroundImage = `url(${animations.moveR})`
      break
    case 'idle':
      if (pet.lastDirection === 'left') {
        backgroundImage = `url(${animations.stand})`
      } else {
        backgroundImage = `url(${animations.standR})`
      }
      break
    case 'hit':
      // When hit, show corresponding hit animation based on last movement direction
      if (pet.lastDirection === 'left') {
        backgroundImage = `url(${animations.hit || animations.stand})`
      } else {
        backgroundImage = `url(${animations.hitR || animations.standR})`
      }
      break
    case 'jump':
      // When jumping, show corresponding jump animation based on last movement direction
      if (pet.lastDirection === 'left') {
        backgroundImage = `url(${animations.jump || animations.stand})`
      } else {
        backgroundImage = `url(${animations.jumpR || animations.standR})`
      }
      break
    case 'dying':
      // Show corresponding death animation based on last movement direction
      if (pet.lastDirection === 'left') {
        backgroundImage = `url(${animations.die})`
      } else {
        backgroundImage = `url(${animations.dieR})`
      }
      break
    case 'dead':
      // Dead state shows no image
      backgroundImage = ''
      break
  }

  // Debug information
  if (pet.direction !== 'dead' && !backgroundImage) {
    console.error(
      `Pet ${pet.id} (${pet.type.name}) has no background image for direction: ${pet.direction}`,
    )
  }

  // Make all pets use half of original GIF size, proportionally scaled down
  let bottomOffset = '1px' // Default bottom offset

  // Special position adjustment for pig
  if (pet.type.name === 'Pig') {
    bottomOffset = '-3px' // Pig slightly lower
  }

  // Add jump height offset
  const jumpOffset = pet.jumpHeight
  const finalBottomOffset = `calc(${bottomOffset} + ${jumpOffset}px)`

  return {
    left: `${pet.position}%`,
    bottom: finalBottomOffset,
    width: 'auto', // Let width automatically adapt to background image
    height: 'auto', // Let height automatically adapt to background image
    minWidth: '50px', // Minimum width also halved accordingly
    minHeight: '50px', // Minimum height also halved accordingly
    backgroundImage,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    backgroundSize: '70%', // Scale down to 70% of original size
    opacity: pet.opacity,
    display: pet.direction === 'dead' && pet.opacity === 0 ? 'none' : 'block',
    transition:
      pet.direction === 'hit'
        ? 'left 0.2s ease-out'
        : pet.direction === 'jump'
          ? 'bottom 0.5s ease-in-out'
          : 'none', // Add vertical movement animation when jumping
  }
}

// Handle pet click
const handlePetClick = (petId: number) => {
  const pet = pets.value.find((p) => p.id === petId)
  if (!pet || !pet.isClickable) return

  // Reduce health
  pet.currentHp -= 1
  console.log(`Pet ${pet.id} (${pet.type.name}) HP: ${pet.currentHp}/${pet.maxHp}`)

  if (pet.currentHp <= 0) {
    // Health reaches zero, die immediately
    startDying(pet)
  } else {
    // Still has health, show hit effect
    showHitEffect(pet)
  }
}

// Show hit effect
const showHitEffect = (pet: Pet) => {
  const animations = pet.type.animations

  // Check if hit animation exists
  if (!animations.hit && !animations.hitR) {
    // No hit animation, die immediately
    console.log(`Pet ${pet.id} has no hit animation, dying immediately`)
    startDying(pet)
    return
  }

  // Pause movement and show hit animation
  pet.direction = 'hit'
  pet.isClickable = false
  pet.isMoving = false

  // Calculate knockback effect: determine knockback direction based on last movement direction
  const knockbackDistance = 10 // Increase to 50px for more obvious effect
  const viewportWidth = window.innerWidth || 1920 // Get viewport width, default 1920px
  const knockbackPercent = (knockbackDistance / viewportWidth) * 100 // Convert to percentage

  console.log(`Pet ${pet.id} knockback: ${knockbackPercent}% (${knockbackDistance}px)`)

  // Delay knockback execution slightly for more natural animation effect
  setTimeout(() => {
    if (pet.lastDirection === 'left') {
      // If pet was moving left, knockback to the right when hit
      const newPosition = Math.min(94, pet.position + knockbackPercent)
      console.log(`Pet moving left, knocked back from ${pet.position}% to ${newPosition}%`)
      pet.position = newPosition
    } else {
      // If pet was moving right, knockback to the left when hit
      const newPosition = Math.max(0, pet.position - knockbackPercent)
      console.log(`Pet moving right, knocked back from ${pet.position}% to ${newPosition}%`)
      pet.position = newPosition
    }
  }, 50) // Delay 50ms for knockback execution

  // Return to normal state after 0.7 seconds (give sliding animation more time)
  setTimeout(() => {
    if (pet.currentHp > 0) {
      pet.isClickable = true
      pet.isMoving = true
      // Restore movement state
      pet.direction = pet.lastDirection
    }
  }, 700)
}

// Show jump effect
const showJumpEffect = (pet: Pet) => {
  const animations = pet.type.animations

  // Check if jump animation exists
  if (!animations.jump && !animations.jumpR) {
    console.log(`Pet ${pet.id} has no jump animation`)
    return
  }

  // Set jump state while maintaining movement and click ability
  pet.direction = 'jump'
  // Don't stop movement and click functionality

  console.log(`Pet ${pet.id} (${pet.type.name}) is jumping!`)

  // Jump animation: jump up first, then fall down
  const maxJumpHeight = 40 // Jump height for more obvious effect
  const jumpDuration = 500 // Jump duration 0.5 seconds

  // Jump up
  setTimeout(() => {
    pet.jumpHeight = maxJumpHeight
  }, 50) // Slight delay for more natural animation

  // Fall down
  setTimeout(() => {
    pet.jumpHeight = 0
  }, jumpDuration)

  // Return to normal state after 1 second
  setTimeout(() => {
    pet.jumpHeight = 0 // Ensure back to ground
    // Restore movement state
    pet.direction = pet.lastDirection
  }, 1000)
}

// Start death animation
const startDying = (pet: Pet) => {
  pet.direction = 'dying'
  pet.isClickable = false
  pet.isMoving = false

  // Start death animation and fade effect simultaneously
  const fadeInterval = setInterval(() => {
    pet.opacity -= 0.15 // Speed up fade
    if (pet.opacity <= 0) {
      clearInterval(fadeInterval)
      pet.direction = 'dead'
      // Respawn after random 3-10 seconds
      const respawnTime = Math.random() * 7000 + 3000 // 3-10 seconds
      setTimeout(() => {
        respawnPet(pet.id)
      }, respawnTime)
    }
  }, 80) // Reduce interval time, total about 0.8 seconds to completely disappear
}

// Respawn pet
const respawnPet = (petId: number) => {
  const pet = pets.value.find((p) => p.id === petId)
  if (!pet) return

  // Ensure pet is completely hidden
  pet.opacity = 0
  pet.direction = 'dead'

  // Use nextTick to ensure DOM update completion before changing position
  setTimeout(() => {
    // Change position and type when pet is completely invisible
    pet.type = getRandomPetType() // Randomly select new pet type when respawning
    pet.position = Math.random() * 90 + 5 // 5-95% random position
    pet.direction = Math.random() > 0.5 ? 'left' : 'right'
    pet.lastDirection = pet.direction
    pet.isClickable = true
    pet.isMoving = true

    // Reset health
    const newMaxHp = Math.floor(Math.random() * 3) + 1 // Random 1-3 health
    pet.maxHp = newMaxHp
    pet.currentHp = newMaxHp
    pet.jumpHeight = 0 // Ensure on ground when respawning
    console.log(`Pet ${pet.id} respawned as ${pet.type.name} with HP: ${pet.maxHp}`)

    // Wait one more frame to ensure position setting completion
    setTimeout(() => {
      // Fade in effect
      const fadeInInterval = setInterval(() => {
        pet.opacity += 0.1
        if (pet.opacity >= 1) {
          pet.opacity = 1
          clearInterval(fadeInInterval)
        }
      }, 50) // Increase opacity every 50ms, total about 0.5 seconds to fully show
    }, 16) // Wait one animation frame (about 16ms)
  }, 100) // Wait 100ms to ensure complete hiding
}

// Start moving
const startMoving = (pet: Pet, dir: 'left' | 'right') => {
  pet.direction = dir
  pet.lastDirection = dir
  pet.isMoving = true
}

// Stop moving
const stopMoving = (pet: Pet) => {
  pet.direction = 'idle'
  pet.isMoving = false
}

// Movement logic
const move = () => {
  pets.value.forEach((pet) => {
    // Don't move if pet is dying, dead, or being hit
    if (
      !pet.isMoving ||
      pet.direction === 'dying' ||
      pet.direction === 'dead' ||
      pet.direction === 'hit'
    )
      return

    const speed = 0.15

    if (pet.direction === 'left' || (pet.direction === 'jump' && pet.lastDirection === 'left')) {
      pet.position = Math.max(0, pet.position - speed)
      if (pet.position <= 0 && pet.direction !== 'jump') {
        startMoving(pet, 'right')
      }
    } else if (
      pet.direction === 'right' ||
      (pet.direction === 'jump' && pet.lastDirection === 'right')
    ) {
      pet.position = Math.min(94, pet.position + speed) // Changed to 94% to leave space for 60px width
      if (pet.position >= 94 && pet.direction !== 'jump') {
        startMoving(pet, 'left')
      }
    }
  })
}

// Random decision making
const makeDecision = (pet: Pet) => {
  // Don't make decisions if pet is dying, dead, or being hit
  if (pet.direction === 'dying' || pet.direction === 'dead' || pet.direction === 'hit') return

  // Check if has jump animation
  const hasJumpAnimation =
    pet.type.name === 'Slime' || pet.type.name === 'Pig' || pet.type.name === 'Blue Mushroom'

  const rand = Math.random()

  if (hasJumpAnimation && rand < 0.1) {
    // 10% chance to jump
    showJumpEffect(pet)
  } else if (rand < 0.4) {
    startMoving(pet, 'left')
  } else if (rand < 0.8) {
    startMoving(pet, 'right')
  } else {
    stopMoving(pet)
  }
}

// Timer
let moveInterval: number

onMounted(() => {
  // Initialize pets
  initializePets()

  // Start movement for each pet
  pets.value.forEach((pet) => {
    startMoving(pet, pet.direction as 'left' | 'right')
  })

  // Movement loop
  moveInterval = setInterval(move, 50)

  // Decision loop for each pet
  pets.value.forEach((pet, index) => {
    const scheduleDecision = () => {
      const delay = 2000 + Math.random() * 3000
      setTimeout(() => {
        makeDecision(pet)
        scheduleDecision()
      }, delay)
    }

    setTimeout(scheduleDecision, 1000 + index * 500)
  })
})

onUnmounted(() => {
  if (moveInterval) clearInterval(moveInterval)
})
</script>

<style scoped>
/* Vue Transition */
</style>
