# Product redesign v2 research note

References studied before implementation:

- Finch: the companion is the emotional feedback loop; small daily actions are framed as care for both user and pet, and progress is celebrated through growth and short adventures.
- Plant Nanny: the habit is represented by a living world object whose condition changes with consistency.
- Waterful: quick completion, visible streaks, and short challenges create motivation without requiring a complex economy.
- Airbnb HorizonCalendar: horizontally paged date ranges, custom day cells, selection callbacks, animated updates, and accessibility are stronger foundations than a large static calendar.
- ScreenPets and PetPlayground: animation should be state driven, with deliberate transitions and interaction responses rather than a permanent repeating timer.

Adopted: one continuous scene, compact horizontally navigable history, direct manipulation tied to the physical task, visible world transformation, irregular companion behaviors, and lightweight milestone unlocks.

Rejected: copied characters or art, analytics dashboards, generic card stacks, constant blinking/looping motion, noisy reward economies, and a third-party calendar dependency while the required interaction remains small enough for native SwiftUI.
