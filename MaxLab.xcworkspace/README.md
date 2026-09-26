# App Lab workspace

Keep these independent repositories as siblings:

```
parent/
  app-lab/MaxLab.xcworkspace
  gamify15/Gamefy.xcodeproj
  reset/Reset.xcodeproj
  maxlab/MaxLab.xcodeproj
```

Close existing Xcode windows for these projects, then open `app-lab/MaxLab.xcworkspace`. Select the shared `Gamefy`, `Reset` or `MaxLab` scheme and an iPhone Simulator or your signed iPhone. Each `.xcodeproj` also works on its own. Signing settings are not managed by this workspace.

Gamefy exports its existing `AppFoundation` module. Reset's existing standalone foundation source is exported as `ResetFoundation`, so the modules and products are unambiguous when both packages are loaded. MaxLab does not use Foundation and has no package dependency. No additional Foundation copies are needed. The separate private `apple-app-foundation` template repository is not a workspace dependency; open it separately when editing the template. Requiring that private repository would break self-contained clones and CI without additional credentials.

All project object IDs are unique across projects. Shared schemes point to the corresponding app and UI-test targets. File references resolve from each repository root, not from inside its `.xcodeproj` bundle.

From `app-lab`, run `./verify` to validate file references, object IDs, package bindings and schemes, then compile all three apps and UI-test bundles in one workspace build directory. Run `swift test` in each app repository for its unit tests. To execute UI tests, use Xcode's Product > Test on a disposable Simulator; Gamefy's tests reset app data.

If an already-open Xcode window still shows stale missing-product or recovered-reference errors after pulling the fixes, quit Xcode and reopen this workspace. Only if errors persist, use Product > Clean Build Folder and File > Packages > Reset Package Caches, then reopen. No signing changes are needed.
