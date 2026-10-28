# Verification checklist

Use the existing project's runner and installed browser where possible. A scroll test should exercise the feature rather than assert that the implementation contains expected words.

## State checks

- Assembled: all part transforms equal their saved assembled transforms within a stated numerical tolerance.
- Opening: camera changes and casing clears the internal parts; the scene remains pinned.
- Exploded: semantically distinct components separate without losing their correspondence to the original object.
- Annotated: each expected label appears once and leader lines track its component.
- Detail: every chapter selects the matching component, keeps it unobstructed by the casing, and exposes its role through clear copy and a relevant working demonstration. Check all chapters, not only the first. A front-facing colored shell is not evidence that an internal component is visible.
- Reversed: scroll from late detail back through opening to assembled; transforms and visible content restore correctly.
- Direct jumps: chapter buttons and deep links produce the intended state without having played earlier frames.

## Layout and access

Check desktop, narrow phone, short viewport, and resize while the engine is open. Confirm no horizontal overflow, unintended clipping, text/geometry overlap, offscreen focused part, unreadable tiny labels, or navigation obscuring copy. The full exploded bounds should fit except where deliberate cropping is documented and useful.

Check keyboard activation, focus visibility, active chapter semantics, semantic headings, and reduced motion. Verify part explanations remain reachable when autonomous animation is disabled. Check that the fallback explains model-load or WebGL failure.

Assert that each selected-part label appears once, overview labels are inactive in detail mode, and inactive hero copy/controls are excluded from assistive technology. Compare projected close-up bounds with the committed explanation and demonstration rectangles, using explicit clearance margins on both desktop and mobile. Check the actual target of the focus arrow; an endpoint inside an empty bounding-box corner is not sufficient.

Verify demonstration motion or scroll response, correct chapter mapping, replay, and reduced-motion behavior. Inspect the final closing state and direct end-to-overview reversal. Keep functional, visual, and learning-quality conclusions separate.

## Runtime

Wait for a model readiness marker with an attached-state selector if the scene starts hidden. Separate script errors, failed geometry/decoder requests, expected cancelled loads during unmount, and favicon noise. Capture before/after frames with animations settled or paused when comparing rendering.

Run build and lint. Save screenshots at semantic checkpoints, a short results file, viewport sizes, and any remaining limitations. Numeric transform checks and assertions do not establish pixel equivalence or factual accuracy of the explanatory text.

## Reference reproduction

Pair original and local screenshots by semantic chapter. Compare orientation, component ordering, spacing, annotation anchoring, background transition, selected part, and explanation order. List meaningful differences. Do not call source geometry plus different timing/shaders an exact reproduction.
