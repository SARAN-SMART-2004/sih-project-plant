let text = document.getElementById('text');
let leaf = document.getElementById('leaf');
let hill1 = document.getElementById('hill1');
let hill4 = document.getElementById('hill4');
let hill5 = document.getElementById('hill5');
let camera = document.getElementById('camera');

window.addEventListener('scroll', () => {
    let value = window.scrollY;
    text.style.marginTop = value * 2.5 + 'px';
    camera.style.marginTop = value * 2.5 + 'px';
    leaf.style.top = value * -1.5 + 'px';
    leaf.style.left = value * 1.5 + 'px';
    hill5.style.left = value * 1.5 + 'px';
    hill4.style.left = value * -1.5 + 'px';
    hill1.style.top = value * 1 + 'px';
});


let zone = document.getElementById('butt');
let cameraa = document.getElementById("enhancerUIContainer");
let frame = document.getElementById('framepic');

function opens() {
    zone.style.display = "block";
    cameraa.style.display = "none";
}

function closes() {
    zone.style.display = "none";
    cameraa.style.display = "block";

}





function cameras() {
    cameraa.style.display = "block";
    cameraa.style.border = "3px solid yellow"
    framepic.style.display = "none";
    let enhancer = null;
    (async () => {
        enhancer = await Dynamsoft.DCE.CameraEnhancer.createInstance();
        document.getElementById("enhancerUIContainer").appendChild(enhancer.getUIElement());
        await enhancer.open(true);
        document.querySelector(".dce-btn-close").onclick = ()=>{
          framepic.style.display = "block";
        }
    })();
    document.getElementById('capture').onclick = () => {
        if (enhancer) {
            let frame = enhancer.getFrame();
    
            let width = screen.availWidth;
            let height = screen.availHeight;
            let popW = 800, popH = 500;
            let left = (width - popW) / 2;
            let top = (height - popH) / 2;
    
            popWindow = window.open('', 'popup', 'width=' + popW + ',height=' + popH +
                ',top=' + top + ',left=' + left + ', scrollbars=yes');
    
            popWindow.document.body.appendChild(frame.canvas);
        }
    };
    
}


