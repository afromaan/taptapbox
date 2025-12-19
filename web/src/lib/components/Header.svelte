<script lang="ts">
  let rotationX = 0;
  let rotationY = 0;

  function handleMouseMove(event: MouseEvent) {
    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
    const x = event.clientX - rect.left; 
    const y = event.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    rotationY = ((x - centerX) / centerX) * 15;
    rotationX = -((y - centerY) / centerY) * 15;
  }

  function resetRotation() {
    rotationX = 0;
    rotationY = 0;
  }
</script>

<header class="bg-white shadow mb-3">
  <div class="container-fluid">
    <div class="row align-items-center">
      <div class="col-4">
        <h2
          class="nadpis"
          on:mousemove={handleMouseMove}
          on:mouseleave={resetRotation}
          style="transform: rotateX({rotationX}deg) rotateY({rotationY}deg);"
        >
          <a href="/" class="text-decoration-none text-reset">TapTapBox</a>
        </h2>
      </div>
      <div class="col-4"></div>
      <div class="col-4">
        <nav>
          <ul class="nav justify-content-end">
            <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="/about">About</a></li>
            <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</header>

<style>
.nadpis {
  font-weight: bold;
  font-family: "Chewy", system-ui;
  letter-spacing: 5px;
  margin: 20px 0;
  display: inline-block;
  transition: transform 0.1s ease;
  cursor: pointer;
  perspective: 500px;
  color: #8a2be2;
}

.nadpis a {
  text-decoration: none;
}

.nav-link {
  background-color: #8a2be2;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 10px;
  margin: 5px;
  color: white;
  transition: transform 0.3s ease, color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
}

.nav-link:hover {
  transform: scale(1.1);
  background-color: white;
  color: #7a1be2;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
}
</style>
