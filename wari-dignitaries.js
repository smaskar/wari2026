// Leadership strip — names/designations as provided 2026-07-03 (hoarding order = protocol order).
// Photos cropped from campaign hoarding (low-res); swap files in assets/img/leaders/ when originals arrive.
window.WARI_DIGNITARIES=[
 {n:"श्री. देवेंद्र फडणवीस",d:"मा. मुख्यमंत्री",img:"./assets/img/leaders/l1.jpg"},
 {n:"श्री. एकनाथ शिंदे",d:"मा. उपमुख्यमंत्री",img:"./assets/img/leaders/l2.jpg"},
 {n:"सौ. सुनेत्रा अजित पवार",d:"मा. उपमुख्यमंत्री",img:"./assets/img/leaders/l3.jpg"},
 {n:"श्री. प्रकाश आबिटकर",d:"मा. मंत्री, सार्वजनिक आरोग्य व कुटुंब कल्याण",img:"./assets/img/leaders/l4.jpg"},
 {n:"श्रीमती मेघना साकोरे-बोर्डीकर",d:"मा. राज्यमंत्री, सार्वजनिक आरोग्य व कुटुंब कल्याण",img:"./assets/img/leaders/l5.jpg"}
];
(function(){
  function render(){
    var el=document.getElementById('leaders-strip'); if(!el) return;
    el.innerHTML=window.WARI_DIGNITARIES.map(function(o){
      return '<div class="ldr"><img src="'+o.img+'" alt="'+o.n+'" loading="lazy"/><b>'+o.n+'</b><small>'+o.d+'</small></div>';
    }).join('');
  }
  if(document.readyState!=='loading') render(); else document.addEventListener('DOMContentLoaded', render);
})();
