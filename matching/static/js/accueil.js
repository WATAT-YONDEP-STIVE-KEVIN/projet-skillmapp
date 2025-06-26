// Animation légère sur les boutons CTA
document.addEventListener('DOMContentLoaded', function () {
  const ctaBtn = document.querySelector('.cta-button');
  if (ctaBtn) {
    ctaBtn.addEventListener('mouseover', () => {
      ctaBtn.style.transform = 'scale(1.05)';
    });
    ctaBtn.addEventListener('mouseout', () => {
      ctaBtn.style.transform = 'scale(1)';
    });
  }

  const contactBtn = document.querySelector('.contact-button');
  if (contactBtn) {
    contactBtn.addEventListener('click', () => {
      alert("Merci de nous contacter ! Nous reviendrons vers vous sous peu.");
    });
  }
});
