<script>
  // ... (SVELTE JS kód zůstává stejný, není třeba ho měnit, jen ho vynechávám pro přehlednost) ...

  import { onMount } from 'svelte';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

  let container;
  let scene, camera, renderer, model;
  
  let rotationSpeed = 0.05; 
  let targetSpeed = 0.0005; 
  let deceleration = 0.995;

  onMount(() => {
    const width = container.clientWidth;
    const height = width; 

    scene = new THREE.Scene();
    scene.background = null; 

    camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(1, 1, 4);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(5, 10, 7);
    dirLight.castShadow = true;
    scene.add(dirLight);

    const loader = new GLTFLoader();
    loader.load('/model.glb?v=2', (gltf) => {
      model = gltf.scene;

      model.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });

      model.scale.set(1, 1, 1); 
      model.position.y = 0; 
      scene.add(model);
      
      animate();
    });

    const animate = () => {
      requestAnimationFrame(animate);
      if (model) {
        model.rotation.y += rotationSpeed;
        if (rotationSpeed > targetSpeed) {
          rotationSpeed *= deceleration;
          if (rotationSpeed < targetSpeed) rotationSpeed = targetSpeed;
        }
      }
      renderer.render(scene, camera);
    };

    const resize = () => {
      if (!container) return;
      
      // Důležité: Velikost bereme podle šířky rodičovského elementu
      const newWidth = container.clientWidth;
      const newHeight = newWidth; 

      renderer.setSize(newWidth, newHeight);
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
    };

    window.addEventListener('resize', resize);
    resize();

    return () => {
      window.removeEventListener('resize', resize);
      renderer.dispose();
    };
  });
</script>

<div class="container-fluid p-0">
  <div class="row min-vh-100 align-items-center py-5">
    
    <div class="col-md-8 mb-4 mb-md-0 d-flex justify-content-center">
      <div class="card shadow-lg border-0 rounded-4 overflow-hidden w-75">
        <div class="card-body p-0 d-flex justify-content-center align-items-center bg-white">
          <div bind:this={container} class="canvas-container"></div>
        </div>
        <div class="card-footer bg-white border-0 text-center text-muted pb-3">
          <small>Interaktivní 3D Model</small>
        </div>
      </div>
    </div>

    <div class="col-md-4 px-5">
      <h1>Model na celou obrazovku</h1>
      <p class="lead">
        Tato sekce je vysoká přesně jako tvůj prohlížeč (<code>100vh</code>).
      </p>
      <p>
        Model vlevo zabírá $2/3$ šířky na desktopu, a celý blok je vertikálně zarovnaný na střed.
      </p>
      
      <hr class="my-4">

      <p>Pokud přidáš více obsahu, bude se od tohoto bodu rolovat dál.</p>
    </div>

  </div>
  
  <div class="container py-5">
    <div class="row">
      <div class="col">
        <h3>Obsah pod hlavní sekcí</h3>
        {#each Array(10) as _, i}
          <p>Toto je výplňový text pod sekcí $100vh$ {i + 1}. Nyní můžeš scrollovat dolů a model zmizí nahoru.</p>
        {/each}
      </div>
    </div>
  </div>
</div>

<style>
  /* Globální styly pro pozadí stránky */
  :global(body) {
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
    background: #f8f9fa;
  }

  /* Zajistíme, aby div pro canvas neměl nulovou výšku před načtením 
     a aby se canvas roztáhl.
  */
  .canvas-container {
    width: 100%;
    /* Můžeš přidat max-height, pokud se model v menším sloupci
       vytáhne příliš vysoko na úkor textu, ale obvykle to není třeba */
    display: block;
  }
</style>  