// Mount every widget on the page once all of them are registered (this file is concatenated last).
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", QB.mount); else QB.mount();
