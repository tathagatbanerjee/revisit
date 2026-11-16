# Capture for the first static recipe

Start with a stationary, textured subject or room. Move the camera steadily around
it, keeping substantial overlap between neighboring views. Use landscape16:9,
normal perspective video, clear focus and consistent exposure. Choose one
continuous1–30s interval. Do not combine cuts/dissolves, wildly different shots,
strong fisheye distortion or generated frames into one scene.

Camera translation supplies spatial baseline. Rotating in place, reflective
surfaces, repeated plain walls, motion blur and fast exposure changes can defeat
camera recovery. Moving people may blur or become ghosts in a static fit; this
recipe does not replay their event. Broad orbiting only works within the coverage
actually recorded. Unsupported surfaces are not facts recovered from the video.

A suitable first input is your own steady shot of a textured tabletop object or
room, with a clear translating camera and minimal movement in the subject. The
Houseplant example demonstrates real captured geometry, but its source video is
not included as a Revisit training fixture. A cleared reference input video and
its fresh Revisit fitting result remain part of end-to-end qualification.

The app prepares640×360 observations at12Hz, preserving original source PTS. It
rejects non16:9 footage rather than silently changing camera geometry. Crop a copy
externally if necessary and retain your original. Successful decoding and camera
mapping are preliminary checks; GPU geometry and appearance still need review.

If camera recovery fails, inspect the source previews for blur, cuts and lack of
parallax. Select a better interval or capture more overlapping stationary detail.
Keep the failed attempt as evidence and create a new project for the correction.
