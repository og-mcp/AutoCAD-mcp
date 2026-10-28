---
name: scroll-object-explainer
description: Build interactive object explanations where scrolling opens an assembled object into an exploded view, labels its components, explores each part in detail, and reassembles it. Use whenever users ask to open a lens, engine, product, machine, device, biological structure, or conceptual system to explain its parts; create a scroll-driven teardown, cutaway, exploded-view explainer, or disassembly story; or reproduce a reference site's object-opening animation. Also use when feedback says the object should open on scroll or reveal detailed subsections. Not for ordinary entrance animations, static diagrams, a looping hero alone, physical disassembly instructions, or source-code architecture analysis.
---

# Scroll Object Explainer

Create a working local explainer that teaches how the object's parts contribute to the whole. Preserve the object's identity through the entire sequence. A spinning hero followed by unrelated cards does not meet this goal.

## Determine the scope from context

Extract the object, audience, reference URL or assets, desired detail, existing app, and output format from the conversation. Continue in the existing project and stack when present. For a new local web app without another preference, use React, TypeScript, Vite, Tailwind, Anime.js, and Three.js only when real depth is useful.

Ask only for information that blocks a useful result. If the object is known but exact internal geometry is unavailable, offer or build a clearly identified schematic rather than inventing manufacturer-specific internals. Do not turn a local implementation request into a deployment or a request to change unrelated agent settings.

## 1. Gather evidence before reproducing a reference

When a reference site is supplied, inspect its scroll behavior, not just its first viewport. Use the REA skill for requested reverse-engineering evidence when available. Use its supported CLI fallback if MCP tools are absent; do not repeatedly reinstall a healthy registration. Distinguish REA Evidence from ordinary browser observations.

Capture at least these states:

1. Assembled object and introductory copy.
2. Side rotation or opening transition.
3. Fully separated components and annotation layout.
4. First, middle, and last detailed subsection.
5. Reverse scroll and the reassembled state.
6. A narrow viewport at opening and part detail.

Record normalized scroll positions in viewport units, section boundaries, headings, label names, connection-line anchors, geometry sources, camera changes, background transitions, and the active-part behavior. Inspect public network records for existing GLB/GLTF assets before approximating a precise object with primitives. Keep source attribution and licenses; access to an asset does not establish redistribution rights.

For an original explainer, derive the same information from supplied models, drawings, authoritative references, and the learning goal. Separate verified anatomy or engineering facts from a schematic representation. Do not present a render as evidence of real construction, assembly order, or safe physical disassembly.

## 2. Create a teaching storyboard and part registry

Write a compact storyboard and a machine-readable registry before building the scene. Use [assets/storyboard.example.json](assets/storyboard.example.json) as a structural example, replacing its parts and timing for the actual object.

Every part should have:

- Stable ID, human name, parent assembly, and geometry/node mapping.
- Assembled transform and exploded offset or target transform.
- Label anchor in model coordinates, label side, and detail-section ID.
- Function, connection to adjacent parts, and one useful cause/effect explanation.
- Source or an explicit schematic/unknown designation.

Order the narrative by the audience's understanding: what the object does, what opens, how parts relate, what each part contributes, and how the assembly works together. Do not simply explain meshes in file order. For each selected part, provide its purpose, interaction with neighboring parts, and a concrete example; add a failure mode only when supported and useful.

Use this state progression:

`assembled → rotate → open casing → explode → annotate → focus(part 1…N) → reassemble`

Set the scroll budget from the content and reading time. Do not hard-code the lens example's dimensions, part count, eight subsections, or sixteen viewport story into every project. For a requested close reproduction, preserve the observed subsection order and disclose meaningful differences.

## 3. Prepare geometry and choose the renderer

Read [references/implementation.md](references/implementation.md) for the implementation recipe.

- Prefer a supplied or authorized GLB/GLTF model with meaningful component groups.
- Inspect node names, hierarchy, bounds, pivots, compression, units, and textures. Run `scripts/inspect_glb.py <file.glb>` for inert GLB metadata when useful; it cannot decode compressed geometry or establish semantic part names.
- Configure Draco or Meshopt only when the asset requires it. Serve matching decoder files locally when offline operation is required and retain dependency licenses.
- Preserve original vertex coordinates and transforms until the hierarchy is understood. Put each semantic part inside its own transform group instead of destructively moving geometry.
- Use Three.js for depth, casing removal, camera changes, and spatial relationships. Use SVG or CSS for genuinely planar or schematic subjects. Do not claim that a flattened SVG tilt reproduces a reference's 3D opening sequence.
- If a single fused mesh cannot be separated reliably, explain the limitation and use a cutaway, authored primitives, or a labeled schematic. Do not pretend arbitrary mesh fragments are meaningful parts.

Keep a declarative part registry separate from rendering code and teaching copy. Avoid embedding one object's imported geometry or private project paths in this skill.

## 4. Build a continuous scroll scene

Use a tall story section with one sticky viewport. Keep ordinary page scrolling; do not hijack the wheel or keyboard. Use a single normalized scroll progress value to drive a paused Anime.js timeline through `seek()`, or the documented `onScroll` synchronization API. Check current API guidance with Context7 when implementing library-specific code.

Animate camera or parent orientation, casing displacement, per-part separation, annotation visibility, part focus, and reassembly from that same progress. Derive the active subsection from the same source so copy and geometry cannot drift apart.

Maintain the assembled object's continuity into the opening sequence. Avoid a visible jump between an unrelated hero and a second model. Crossfade only when the silhouettes, camera, scale, and transforms agree at the handoff.

For the annotation stage, project model-space anchors through the actual scene and camera matrices to screen coordinates after transforms update. Render leader lines and label endpoints in the same coordinate system. Prevent label collisions and keep lines from crossing the teaching copy when practical. On mobile, deliberately reposition or reduce annotations instead of shrinking desktop typography until it becomes unreadable.

During a part-detail section:

- Keep the object open. A front-facing view of the complete casing with a colored surface does not explain an internal part; confirm that the selected geometry is actually visible and unobstructed.
- Bring the selected component into a readable three-quarter close-up or cutaway, exposing its depth and relevant interfaces. Keep an exploded overview faintly visible for spatial context when helpful.
- Keep enough neighboring structure visible to explain its relationship to the assembly.
- Pair the selected part with a plain-language explanation and a working demonstration of its role. A code snippet or feature title alone is not a detailed explanation. For conceptual software models, demonstrate the represented behavior without inventing physical machinery claims.
- Reserve separate measured areas for copy, the selected part, the demonstration, and code. Fit the close-up into the remaining space rather than allowing it to cover the explanation or controls.
- Render one selected-part label, with its leader ending on the visible component. Do not leave a second fixed-position label or point an arrow at an empty corner of a bounding box.
- Make chapter controls scroll to real subsection positions. Support direct navigation and scrolling backward.

Read [references/detail-and-annotation-lessons.md](references/detail-and-annotation-lessons.md) when fixing unclear explanations, front-only detail views, overlapping close-ups, incorrect leader lines, or a discontinuous final pose. It captures the failure modes that functional scroll checks alone missed.

Treat the story as a reversible function of scroll position. Derive every animated part transform from its saved assembled transform; do not accumulate offsets on repeated scrolls. Reassembly should restore the original transforms, not a roughly similar pose.

## 5. Make it robust and accessible

Compute camera framing from the entire object's bounds at its most separated state, including casing travel. Check both the full assembly and each focused part. Recompute on viewport resize and orientation changes. Do not rely on desktop camera settings scaled down by an arbitrary constant.

Keep headings and explanations as semantic DOM content. Give chapter controls accessible names and current-step state. Support keyboard navigation. Under reduced motion, remove autonomous loops, rapid rotations, and sweeping transitions; provide direct part selection or static states with all explanations still reachable.

Hide inactive introductory and overview content from assistive technology as well as visually. Opacity alone leaves old copy, controls, and concatenated labels exposed. Use appropriate hidden or aria-hidden state and inert controls, while keeping the active explanation and chapter navigation reachable.

Use React scope cleanup (`createScope` / `revert`), cancel scheduled frames, detach scroll/resize listeners, disconnect observers, and dispose geometries, materials, textures, renderers, and decoder workers owned by the component. Handle asset-load failure with usable explanatory content rather than a blank canvas. Account for component unmount during asynchronous model loading and StrictMode setup/cleanup.

Readiness is distinct from visibility: a model can finish loading while its canvas is intentionally hidden at the start. Tests should wait for a readiness state to be attached, not necessarily visible. Serve geometry and decoders from local public assets if the result is expected to run locally without third-party requests.

## 6. Verify the actual story

Read [references/verification.md](references/verification.md) and perform checks appropriate to the implementation. Run the project's production build and lint plus a meaningful browser test of the scroll interaction.

Capture screenshots at the storyboard checkpoints in both directions. Confirm camera framing, readable labels, the correct part for every subsection, matching explanation text, reverse continuity, exact restoration of assembled transforms, resize behavior, keyboard access, and reduced motion. Check browser errors and failed asset requests. A successful build or an animated first viewport alone is insufficient.

Check every detail chapter for meaningful visibility, unique labels, part-specific demonstration behavior, and clearance between projected part bounds and measured text/demo rectangles. Correct overview connectors do not establish that the detailed explanation works. Include screenshots of the chapter the user reported, not only the overview.

If browser automation is unavailable, report which checks remain unverified; do not claim they passed. Compare reference and local captures at equivalent semantic states rather than assuming equal raw scroll offsets or expecting asynchronous animation phases to match automatically.

## Deliver

Leave a runnable local app, source code, part registry/storyboard, asset attribution, concise run commands, and captured verification results. Report the local URL and what was tested. Describe the result as an exact reproduction only when the relevant geometry, camera, subsection behavior, timing, and pixels were actually compared; otherwise name the material differences plainly.

When the user requests only planning, stop at a concrete storyboard, registry design, implementation approach, and verification plan. Do not scaffold an unsolicited app.
