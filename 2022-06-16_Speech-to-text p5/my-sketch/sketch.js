function preload() {
  fontGlyph = loadFont('assets/gl.otf');
  fontC = loadFont('assets/consolaz.ttf');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(60);
  let lang = navigator.language || 'en-US';
  let speechRec = new p5.SpeechRec(lang, gotSpeech);
  let continuous = false;
  let interimResults = true;

  speechRec.onError = restart;
  speechRec.onEnd = restart;

  speechRec.start(continuous, interimResults);

  function restart(){
    speechRec.start(continuous, interimResults);
  }

  



  function gotSpeech() {

    console.log(speechRec);
    background('white');
    textAlign(CENTER);
    textSize(100);
    textFont(fontC);
    fill(255, 255, 51)
    let conf = str(round(speechRec.resultConfidence, 10));
    let uppcase = speechRec.resultString.toUpperCase();
    background(0, 0, 244);
    text(conf, windowWidth/2,windowHeight/2 + windowHeight/4);
    fill(255, 255, 51)
    textFont(fontC);
    if(uppcase.length > 6){
      newText = uppcase.split(" ").slice(-6).join(" ");
      text(newText, windowWidth/2, windowHeight/2);
    }else{
      text(uppcase, windowWidth/2, windowHeight/2);
    }
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}




