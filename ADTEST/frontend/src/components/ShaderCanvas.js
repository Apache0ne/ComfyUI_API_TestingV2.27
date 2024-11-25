import React, { useRef, useEffect, useState } from 'react';
import p5 from 'p5';
import sketch from '../p5setup/sketch';

const ShaderCanvas = ({ imageUrl }) => {
  const canvasRef = useRef(null);
  const [p5Instance, setP5Instance] = useState(null);

  useEffect(() => {
    if (!p5Instance) {
      const newP5 = new p5(sketch, canvasRef.current);
      setP5Instance(newP5);
    }

    return () => {
      if (p5Instance) {
        p5Instance.remove();
      }
    };
  }, [p5Instance]);

  useEffect(() => {
    if (p5Instance && imageUrl) {
      p5Instance.loadImage(imageUrl, (loadedImg) => {
        p5Instance.updateImage(loadedImg);
      });
    }
  }, [p5Instance, imageUrl]);

  useEffect(() => {
    if (canvasRef.current) {
      canvasRef.current.oncontextmenu = (e) => e.preventDefault();
    }
  }, []);

  return (
    <div>
      <div ref={canvasRef}></div>
      {!imageUrl && <p>Please generate an image to apply 3D shader effects.</p>}
    </div>
  );
};

export default ShaderCanvas;