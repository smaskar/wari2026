(function(){
  const css = `
    @media (min-width: 900px){
      body{overflow-x:hidden!important;}
      .page{
        max-width:470px!important;
        width:100%!important;
        margin:0 auto!important;
        display:block!important;
        min-height:100dvh!important;
        border-radius:0!important;
      }
      .hero,.section,.toolbar,.map-card,.summary,.list{
        grid-column:auto!important;
      }
      .map-card{
        margin:14px 18px 0!important;
        width:auto!important;
      }
      #map{
        height:255px!important;
        width:100%!important;
      }
      .list{
        max-height:none!important;
        overflow:visible!important;
      }
    }
    .leaflet-container{max-width:100%!important;}
  `;
  const style = document.createElement('style');
  style.id = 'desktop-mobile-alignment-fix';
  style.appendChild(document.createTextNode(css));
  document.head.appendChild(style);
  window.addEventListener('load', function(){
    setTimeout(function(){
      if(window.map && typeof window.map.invalidateSize === 'function'){
        window.map.invalidateSize(true);
      }
    }, 300);
  });
})();
