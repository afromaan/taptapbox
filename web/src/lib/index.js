import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.162/build/three.module.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.162/examples/jsm/loaders/GLTFLoader.js";

const canvas = document.getElementById("scene");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 1, 3);

const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
scene.add(light);

const loader = new GLTFLoader();

let model;
let rotateAlways = true;    // <— nastav si to: TRUE = furt se točí, FALSE = točí se jen při najetí myši
let hover = false;

loader.load("model.glb", gltf => {
    model = gltf.scene;
    scene.add(model);

    // Po načtení – rychlé protočení
    const start = performance.now();
    const duration = 700; // 0.7s
    const startRot = 0;
    const endRot = Math.PI * 2;

    function quickSpin(t) {
        const elapsed = t - start;

        if (elapsed < duration) {
            const progress = elapsed / duration;
            model.rotation.y = startRot + (endRot - startRot) * progress;
            requestAnimationFrame(quickSpin);
        } else {
            model.rotation.y = 0; // reset
        }
    }
    requestAnimationFrame(quickSpin);
});

window.addEventListener("mousemove", e => {
    hover = true;
    clearTimeout(window.leaveTimeout);
    window.leaveTimeout = setTimeout(() => hover = false, 150);
});

function animate() {
    requestAnimationFrame(animate);

    if (model) {
        if (rotateAlways) {
            model.rotation.y += 0.005;
        } else if (hover) {
            model.rotation.y += 0.01;
        }
    }
    renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
