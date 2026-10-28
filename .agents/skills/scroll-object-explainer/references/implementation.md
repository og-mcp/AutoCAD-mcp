# Implementation recipe

## Minimal scene structure

```text
StorySection (relative, height determined by narrative)
  StickyViewport (sticky, top 0, height 100svh, overflow hidden)
    Canvas (Three.js, transparent)
    DOM explanation panels
    SVG annotation lines + DOM labels
    Chapter navigation
```

Keep scene state, explanatory content, and part geometry separate. A registry entry may reference several meshes, and a mesh name is not proof of its physical function.

## Shared progress

For a section whose rectangle top is `rect.top`, set:

```ts
const travel = section.offsetHeight - viewport.clientHeight;
const progress = Math.max(0, Math.min(1, -rect.top / Math.max(1, travel)));
timeline.seek(progress * timeline.duration);
```

Coalesce scroll updates with `requestAnimationFrame`. Recalculate section travel on layout changes. For chapter navigation, convert the chapter's normalized progress back into an absolute section scroll position. Keep state changes limited to actual chapter transitions rather than rerendering React on every pixel.

Create a paused timeline over an explicit pose object or per-part groups. Use stable start values, deterministic positions, and absolute transforms so seeking to 0, 1, or any intermediate value works without a previous playback history. Check current Anime.js signatures through Context7; sample code in a skill is not a substitute for the installed version's types.

## Geometry preparation

Load models with GLTFLoader. For Draco-compressed files, set the DRACOLoader decoder path to a known local directory and ship matching decoder files. Meshopt compression needs its own supported decoder. Never treat a missing decoder as an absent part.

Preserve model units and pivots. Save every semantic group's assembled matrix before adding effects. Define exploded offsets in an assembly-local coordinate system. Move outer casing sections clear of the view before expanding inner layers. Animate radial components radially, stacked layers along their common axis, and hinged covers around their real or explicitly schematic hinges.

Use bounding boxes or spheres for framing, including all displaced parts. With a perspective camera, fit the bounds against both vertical and horizontal field of view with margin. Wide or tall screens have different limiting axes. Reframe selected parts while retaining spatial context. For a source reproduction, recover source transforms and camera behavior before fitting a replacement camera by eye.

## Label projection

1. Attach a local anchor to the correct semantic group.
2. Update model and camera world matrices.
3. Transform the local anchor to world space, then project through the camera.
4. Convert normalized device coordinates into the canvas viewport's CSS pixel coordinates.
5. Draw the leader line to the actual DOM label endpoint in the same viewport.
6. Recalculate after model movement, camera changes, resize, and label layout changes.

Do not mix device pixel ratio coordinates with CSS pixel coordinates. Resolve overlaps with column placement, measured label sizes, or staged annotation visibility. Fade labels behind the camera or outside the relevant section.

## Teaching focus

Highlight the part named by the active subsection. Show relationships through a short flow animation, adjacent connectors, transparent shell, or cutaway when it makes the explanation more concrete. Avoid surrounding every object with unrelated example cards instead of explaining its actual parts.

For an internal-part chapter, keep the assembly opened and avoid front-casing occlusion. Use an independently framed close-up with separate focus/context materials when necessary. Measure the committed copy and demo panels, then fit the selected group into the unoccupied screen region. Pair the explanation with a working, chapter-specific experiment; code alone is insufficient. See [detail-and-annotation-lessons.md](detail-and-annotation-lessons.md) for implementation and projection pitfalls.

## Performance and cleanup

Render on scroll/resize when the scene is otherwise static; use continuous frames only for purposeful local demonstrations. Reuse shared geometry and materials, cap device pixel ratio, and avoid recreating meshes during scroll. Separate heavy Three.js loading when useful; do not hide bundle-size problems by merely raising warning thresholds.

Guard asynchronous callbacks after unmount. Dispose resources once, taking shared ownership into account. Test setup-cleanup-setup under React StrictMode. Track load readiness separately from canvas visibility and give WebGL failure a readable DOM fallback.
