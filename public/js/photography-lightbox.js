(async function () {
  try {
    const { default: PhotoSwipe } = await import(
      "https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe.esm.js"
    );
    const { default: PhotoSwipeLightbox } = await import(
      "https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe-lightbox.esm.js"
    );
    // Load CSS by injecting a <link> tag — importing a CSS URL with dynamic import fails
    // because the browser expects a JS/WASM module. Create a helper that resolves when
    // the stylesheet is loaded (or rejects on error).
    function loadCss(href) {
      return new Promise((resolve, reject) => {
        // avoid adding duplicate
        if (document.querySelector(`link[href="${href}"]`)) return resolve();
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = href;
        link.onload = () => resolve();
        link.onerror = (e) => reject(e);
        document.head.appendChild(link);
      });
    }
    await loadCss(
      "https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe.css",
    );

    function init() {
      const gallery = document.getElementById("photography-grid");
      if (!gallery) return;

      const lightbox = new PhotoSwipeLightbox({
        gallery,
        children: "a",
        pswpModule: PhotoSwipe,
      });

      lightbox.init();
      window.__pswpLightbox = lightbox;
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", init);
    } else {
      init();
    }
  } catch (e) {
    console.warn("PhotoSwipe init failed", e);
  }
})();
