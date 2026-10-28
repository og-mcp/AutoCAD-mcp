# Detail visibility and annotation lessons

These lessons came from a working lens reconstruction that passed basic scroll tests but still failed to explain its parts clearly. Generalize the methods; do not copy its dimensions, component count, viewport offsets, or object-specific geometry.

## An opened overview is not enough

The scene opened correctly, but its detail timeline then turned the entire lens back toward the camera. The front casing hid the selected internals. Changing its color and adding explanatory text did not solve the visibility problem.

Keep the assembly open during detail chapters. Present the actual selected geometry in a separate close-up or remove the occluding shell. A three-quarter orientation should expose useful depth and interfaces rather than merely repeat the complete object's front face. Retain a faint exploded assembly so the reader can locate the part within the whole.

When a separate close-up is useful, clone the semantic group once after loading or place an equivalent instance in a dedicated focus group. Reset its position, orientation, and scale independently from the overview. Preserve the original component in context. Reuse immutable geometry, but give context and focus separate materials: ghosting a shared material must not make the highlighted copy faint too. Dispose shared resources according to ownership rather than disposing them once for each clone. Use the appropriate cloning method for skinned or animated assets.

## Explain behavior, not just an API name

Each detailed chapter should answer:

1. Which part is selected?
2. What does it do?
3. How does it interact with the rest of the object?
4. What observable demonstration makes that role understandable?

Keep the demonstration tied to the chapter's learning goal. In the transform example, separate position, rotation, and scale channels visibly, instead of showing only a code sample. In a physical device, demonstrate the relevant flow, motion, load path, or interaction, using supported facts and clearly identified schematic elements. Do not add unrelated animation cards as a substitute for the selected component's explanation.

Provide replay when useful. Match the displayed example and selected part to the same chapter ID. Demonstrations should respect reduced motion and remain understandable in a static state.

## Fit into the remaining space

Measure the active copy and demonstration panels after React commits the chapter's DOM. Reserve an actual screen rectangle for the close-up, with readable gaps around it. Recalculate when chapter text, viewport size, fonts, or orientation changes. A chapter-layout event, layout effect, or observed panel resize can schedule a fresh scene projection after the new content mounts.

Project each relevant mesh's local geometry bounds through its current world matrix and camera, then combine the resulting screen bounds. Projecting a world-axis-aligned box can substantially overestimate a rotated part's footprint. If that estimate prevents useful framing or places an annotation above empty space, use transformed local bounds or sampled visible vertices instead.

Iteratively scale and recenter the selected group to fit the reserved rectangle. Check both axes and perspective depth; do not assume one constant mobile scale fits every component. Record projected bounds for verification. Check that the part clears both the copy and the demonstration, not merely that it fits somewhere inside the viewport. If a short screen cannot support readable copy and a useful close-up, stack or unpin the detail layout rather than shrinking everything indefinitely.

## Leaders need real endpoints

Use one selected-part label. Remove obsolete fixed labels when introducing a projected label; otherwise duplicate names and arrows remain in the page.

For overview leaders, measure the actual label rectangle after layout. Match font family, font size, line height, padding, and gap when comparing to a reference: typography changes the leader's endpoint even when the model anchor is correct.

A reference with a horizontal segment and a 45-degree diagonal can use this routing, with all points in the same CSS-pixel viewport:

```text
anchor = projected component anchor
end = measured label edge plus its intended gap
run = min(abs(end.y - anchor.y), abs(end.x - anchor.x))
bend = (anchor.x + sign(end.x - anchor.x) * run, end.y)
path = end → bend → anchor
```

Apply this only when it matches the intended design. Preserve any observed anchor offsets when reproducing a specific source and document what is being matched. Do not invent a different angle just to force a path through text.

For a close-up arrow, anchor to the visible surface or an authored surface point. The top of an enclosing bounding box can be empty space; a sampled top silhouette vertex or an appropriate model-local anchor is a better endpoint. Update matrices before projection and recalculate after part or camera movement. Do not smooth the line independently in a way that makes it detach from its part while scrubbing.

## Hidden DOM and the closing state

The reported page text exposed old hero copy, all overview labels, and a duplicate selected-part name alongside the active explanation. Visual opacity does not remove content from the accessibility tree or disable hidden controls. Set suitable hidden/aria-hidden state on inactive panels and inert state on inactive controls. Keep navigation and active content accessible.

Do not let the final scroll state end on an oversized, half-rotated, or partially separated object. Explicitly author the closing pose, optional component visibility, background, and any handoff to a front-view overlay. Test a direct jump to the end and a reverse jump back to overview. A matching source geometry file does not guarantee a matching final pose.

## Evidence and acceptance

At every detail chapter, verify selected geometry visibility, correct explanation, a relevant working demonstration, one label, a leader touching the component, and clearance from text and controls on desktop and mobile. Confirm motion rather than only counting demo elements. Test replay and reduced motion.

For close reference reproduction, compare measured connector points at equivalent semantic states. Report the viewport, checkpoint, tolerance, and observed deviation. A subpixel leader match proves only that connector geometry matched at that checkpoint; it says nothing about explanatory clarity, shading, other viewports, or the full animation's fidelity.
