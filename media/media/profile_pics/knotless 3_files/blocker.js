{let e=()=>"10000000-1000-4000-8000-100000000000".replace(/[018]/g,e=>(e^crypto.getRandomValues(new Uint8Array(1))[0]&15>>e/4).toString(16)),t=e=>{let t=document.cookie.match("(^|;)\\s*"+e+"\\s*=\\s*([^;]+)");return t?t.pop():""},i=(e,t,i)=>{var n="";if(i){var a=new Date;a.setTime(a.getTime()+864e5*i),n="; expires="+a.toUTCString()}document.cookie=e+"="+(t||"")+n+"; path=/"},n=()=>{let n=t("_idy_cid");if(n){let a=localStorage.getItem("_idy_cid");a||localStorage.setItem("_idy_cid",n)}return!n&&(n=localStorage.getItem("_idy_cid"))&&i("_idy_cid",n,1825),n||(n=e(),i("_idy_cid",n,1825),localStorage.setItem("_idy_cid",n)),n},a=async()=>{if(!0==window.bmExtension)return;window.bmExtension=!0;let e=new URLSearchParams(window.location.search).get("idya");if(e){let a=new URLSearchParams(window.location.search).get("shopId"),o=new URLSearchParams(window.location.search).get("silence");if(!o){let r=window.location.protocol+"//"+window.location.host+window.location.pathname;window.history.replaceState({},document.title,r)}let c=await fetch("https://rbdata.boostymark.com/api/visit/verifyAdminAccess",{method:"POST",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({shopId:a,mode:e})}),s=await c.json();if(!0===s.status){if(i("_idy_admin",e,1825),o||alert(`Admin Access mode ${s.mode?"enabled":"disabled"}.`),"true"===e)return}else o||alert("Enable Admin Access mode failed, please try again.")}let l=t("_idy_admin");if("true"===l)return;let p=new URLSearchParams(window.location.search).get("bgio"),d=new URLSearchParams(document.currentScript.src.split("?")[1]),m=d.get("shop");m.includes("myshopify.com")||(m=Shopify&&Shopify.shop);let y=Shopify&&Shopify.checkout,h=window.location.href;if(h.startsWith(`https://${m}/admin`)||-1!==h.indexOf("shopifypreview.com")||(h=window.top&&window.top.location&&window.top.location.href)&&h.startsWith(`https://${m}/admin`)||h&&-1!==h.indexOf("shopifypreview.com"))return;let $={shop:m,cid:n(),url:h,title:document.title,r:document.referrer};y&&!p&&($.pageData=JSON.stringify(y));let u=await fetch("https://rbdata.boostymark.com/api/visit/note",{method:"POST",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify($)}),f=await u.json();if(f.fa){let b=document.getElementById("create_customer");b&&b.addEventListener("submit",function(e){if(this.action.endsWith("/account")){e.stopImmediatePropagation(),e.preventDefault();var t=document.querySelector('[name="customer[first_name]"]').value,i=document.querySelector('[name="customer[last_name]"]').value,n=document.querySelector('[name="customer[email]"]').value;fetch("https://rbdata.boostymark.com/api/visit/createRegisterRecord",{method:"POST",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({firstName:t,lastName:i,email:n,shop:m})}),this.submit()}}),document.querySelectorAll("form").forEach(function(e){if(e.action.endsWith("/contact")||e.action.includes("/contact#")){let t=e.querySelector('input[name="contact[tags]"]');t?t.value=t.value?t.value+",bm-verified":"bm-verified":((t=document.createElement("input")).type="hidden",t.name="contact[tags]",t.value="bm-verified",e.appendChild(t))}})}let g=document.createElement("div");if(g.style="top: 0px;left: 0px;position: fixed;width: 100%;height: 100%;display: flex;flex-direction: column;align-items: center;justify-content:flex-start;z-index: 2147483647 !important;background-color: white !important;letter-spacing: 0 !important;",g.innerHTML=`<div style="font-weight:500;font-size:2.2rem;margin:100px 20px 0 20px;text-align: center;">${f.bmh??""}</div><div style="margin: 5px 0 0 0;">${f.bmh?'<hr style="border: none; height: 0.1px; background: #747474; width: 400px;margin:0 10px;">':""}</div><div style="font-weight:300;font-size:1rem;margin:10px 20px 0 20px;max-width: 500px;text-align: center;">${f.bmd??""}</div>`,"redirect"==f.status)f.ret||document.body.appendChild(g),window.location.replace(f.url);else if("stay"==f.status){let v=`<meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>${f.bmh}</title>`;document.head.innerHTML=v,document.body.innerHTML="",document.body.appendChild(g),setInterval(()=>{console.clear(),document.head.innerHTML=v,document.body.innerHTML="",document.body.appendChild(g)},1e3)}else if("part"==f.status)f.se.forEach(e=>{document.querySelectorAll(e).forEach(e=>e.style.display="block")}),f.he.forEach(e=>{document.querySelectorAll(e).forEach(e=>e.style.display="none")});else if("success"==f.status&&window._bm_blocked){var x=document.createElement("script");x.className="analytics",x.textContent=window._bm_blocked_script,document.head.appendChild(x)}if(f.cp){if(f.cp.m_rc&&(document.body.oncontextmenu=function(){return!1}),f.cp.m_ts){let k=document.createElement("style");k.textContent=`body {
        -webkit-touch-callout: none; 
        -webkit-user-select: none;
        -khtml-user-select: none; 
        -moz-user-select: none; 
        -ms-user-select: none; 
        user-select: none; 
      }`,document.head.appendChild(k)}if(f.cp.m_dd&&(document.body.ondragstart=function(){return!1},document.body.ondrop=function(){return!1}),f.cp.pr_t){let w=document.createElement("style");w.media="print",w.textContent="* { display: none; }",document.head.appendChild(w)}(f.cp.k_all||f.cp.k_copy||f.cp.k_paste||f.cp.k_print||f.cp.k_save)&&(document.body.onkeydown=function(e){if(f.cp.k_all&&"a"==e.key.toLowerCase()&&(e.ctrlKey||e.metaKey)||f.cp.k_copy&&"c"==e.key.toLowerCase()&&(e.ctrlKey||e.metaKey)||f.cp.k_paste&&"v"==e.key.toLowerCase()&&(e.ctrlKey||e.metaKey)||f.cp.k_print&&"p"==e.key.toLowerCase()&&(e.ctrlKey||e.metaKey)||f.cp.k_save&&"s"==e.key.toLowerCase()&&(e.ctrlKey||e.metaKey))return!1})}};a()}