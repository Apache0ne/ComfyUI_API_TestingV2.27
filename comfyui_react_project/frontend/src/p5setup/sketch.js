export default function sketch(p) {
  let theShader;
  let img;

  p.preload = () => {
    theShader = p.loadShader(
      '/vertex.glsl',
      '/fragment.glsl'
    );
  };

  p.setup = () => {
    p.createCanvas(600, 600, p.WEBGL);
    p.noStroke();
  };

  p.draw = () => {
    if (img) {
      p.shader(theShader);
      theShader.setUniform('u_resolution', [p.width, p.height]);
      theShader.setUniform('u_time', p.millis() / 1000.0);
      theShader.setUniform('u_texture', img);
      p.rect(0, 0, p.width, p.height);
    }
  };

  p.updateImage = (newImage) => {
    img = newImage;
    p.resizeCanvas(img.width, img.height);
  };
}