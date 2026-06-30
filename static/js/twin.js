/* Alvitsenna Digital Twin — Three.js hologramma wireframe inson modeli */
function initDigitalTwin(containerId, opts) {
  const container = document.getElementById(containerId);
  if (!container || typeof THREE === "undefined") return;

  const settings = Object.assign({
    gender: "female",
    organ: "liver",
    pulse: true,
  }, opts || {});

  const width = container.clientWidth;
  const height = container.clientHeight;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
  camera.position.set(0, 1.1, 6.2);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  const hologramColor = 0x3fd6ff;
  const lineMat = new THREE.LineBasicMaterial({ color: hologramColor, transparent: true, opacity: 0.55 });
  const wireMat = new THREE.MeshBasicMaterial({ color: hologramColor, wireframe: true, transparent: true, opacity: 0.4 });

  const human = new THREE.Group();
  scene.add(human);

  const isMale = settings.gender === "male";
  const shoulderW = isMale ? 0.95 : 0.78;
  const hipW = isMale ? 0.62 : 0.74;

  function addMesh(geo, y, scaleX) {
    const mesh = new THREE.Mesh(geo, wireMat.clone());
    mesh.position.y = y;
    if (scaleX) mesh.scale.x = scaleX;
    human.add(mesh);
    return mesh;
  }

  // Head
  addMesh(new THREE.SphereGeometry(0.34, 16, 12), 3.05);
  // Neck
  addMesh(new THREE.CylinderGeometry(0.12, 0.14, 0.25, 10), 2.66);
  // Torso (chest -> waist)
  const torso = addMesh(new THREE.CylinderGeometry(shoulderW * 0.5, hipW * 0.42, 1.5, 14), 1.75);
  // Pelvis
  addMesh(new THREE.CylinderGeometry(hipW * 0.42, hipW * 0.34, 0.4, 14), 0.9);
  // Arms
  [-1, 1].forEach((side) => {
    const upperArm = addMesh(new THREE.CylinderGeometry(0.1, 0.09, 1.0, 8), 2.05);
    upperArm.position.x = side * (shoulderW * 0.62);
    upperArm.rotation.z = side * 0.12;
    const lowerArm = addMesh(new THREE.CylinderGeometry(0.085, 0.07, 0.95, 8), 1.15);
    lowerArm.position.x = side * (shoulderW * 0.72);
    lowerArm.rotation.z = side * 0.05;
  });
  // Legs
  [-1, 1].forEach((side) => {
    const upperLeg = addMesh(new THREE.CylinderGeometry(0.16, 0.13, 1.3, 10), 0.05);
    upperLeg.position.x = side * 0.22;
    const lowerLeg = addMesh(new THREE.CylinderGeometry(0.12, 0.09, 1.25, 10), -1.25);
    lowerLeg.position.x = side * 0.22;
  });

  // Vertical scanning ring
  const ringGeo = new THREE.TorusGeometry(1.05, 0.012, 8, 64);
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: hologramColor, transparent: true, opacity: 0.5 }));
  ring.rotation.x = Math.PI / 2;
  human.add(ring);

  // Particle field around figure
  const particleCount = 140;
  const positions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i++) {
    const r = 1.6 + Math.random() * 0.6;
    const theta = Math.random() * Math.PI * 2;
    const y = Math.random() * 3.6 - 0.3;
    positions[i * 3] = Math.cos(theta) * r;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = Math.sin(theta) * r;
  }
  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const particles = new THREE.Points(particleGeo, new THREE.PointsMaterial({ color: hologramColor, size: 0.018, transparent: true, opacity: 0.4 }));
  scene.add(particles);

  // Diagnosis hotspot (organ marker)
  const organY = settings.organ === "heart" ? 2.05 : 1.85;
  const organX = settings.organ === "heart" ? 0 : -0.18;
  const hotspotGroup = new THREE.Group();
  hotspotGroup.position.set(organX, organY, 0.45);
  const core = new THREE.Mesh(
    new THREE.SphereGeometry(0.13, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xff5d5d, transparent: true, opacity: 0.85 })
  );
  hotspotGroup.add(core);
  const halo = new THREE.Mesh(
    new THREE.SphereGeometry(0.24, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xff5d5d, transparent: true, opacity: 0.18 })
  );
  hotspotGroup.add(halo);
  human.add(hotspotGroup);

  human.position.y = -1.5;

  let frame = 0;
  function animate() {
    frame += 1;
    human.rotation.y += 0.0035;
    particles.rotation.y -= 0.0012;
    ring.position.y = 1.4 + Math.sin(frame * 0.01) * 1.4;
    if (settings.pulse) {
      const s = 1 + Math.sin(frame * 0.06) * 0.18;
      halo.scale.set(s, s, s);
      core.material.opacity = 0.7 + Math.sin(frame * 0.06) * 0.25;
    }
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();

  window.addEventListener("resize", () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });
}
