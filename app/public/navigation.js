import { Vector3 } from 'three';

// Translate the eye and orbit target together: orientation and orbit distance stay fixed.
export function translateCamera(camera, controls, axes, distance) {
  const delta = new Vector3(axes.right ?? 0, axes.up ?? 0, -(axes.forward ?? 0));
  if (!delta.lengthSq() || !Number.isFinite(distance)) return;
  delta.normalize().applyQuaternion(camera.quaternion).multiplyScalar(distance);
  camera.position.add(delta);
  controls.target.add(delta);
  controls.update();
}

export function createNavigation(canvas, getContext) {
  const held = new Set();
  const bindings = { KeyW: ['forward', 1], ArrowUp: ['forward', 1], KeyS: ['forward', -1], ArrowDown: ['forward', -1], KeyA: ['right', -1], ArrowLeft: ['right', -1], KeyD: ['right', 1], ArrowRight: ['right', 1], KeyQ: ['up', -1], KeyE: ['up', 1] };
  const moves = { left: { right: -1 }, right: { right: 1 }, up: { up: 1 }, down: { up: -1 }, forward: { forward: 1 }, back: { forward: -1 } };
  const speed = document.getElementById('move-speed');
  let lastTime = null;
  canvas.tabIndex = 0;
  canvas.setAttribute('aria-label', '3D scene. WASD to move, Q down, E up, Shift faster. Drag to orbit.');
  canvas.addEventListener('pointerdown', () => canvas.focus({ preventScroll: true }));
  const clear = () => { held.clear(); lastTime = null; };
  canvas.addEventListener('blur', clear);
  window.addEventListener('blur', clear);
  document.addEventListener('visibilitychange', clear);
  window.addEventListener('keyup', event => held.delete(event.code));
  canvas.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || (!bindings[event.code] && !event.code.startsWith('Shift'))) return;
    event.preventDefault(); held.add(event.code);
  });
  speed.addEventListener('input', () => { document.getElementById('move-speed-value').textContent = `${Number(speed.value)}×`; });
  function move(axes, amount) {
    const context = getContext();
    if (!context.ready) return;
    translateCamera(context.camera, context.controls, axes, Math.max(context.radius, 0.01) * amount * Number(speed.value));
  }
  for (const button of document.querySelectorAll('[data-move]')) {
    button.addEventListener('click', () => move(moves[button.dataset.move], 0.12));
  }
  return {
    clear,
    tick(now) {
      const dt = lastTime === null ? 0 : Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;
      if (document.activeElement !== canvas || !held.size) return;
      const axes = { right: 0, up: 0, forward: 0 };
      for (const key of held) if (bindings[key]) axes[bindings[key][0]] += bindings[key][1];
      move(axes, dt * 0.6 * (held.has('ShiftLeft') || held.has('ShiftRight') ? 3 : 1));
    }
  };
}
