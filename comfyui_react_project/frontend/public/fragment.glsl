#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
uniform sampler2D u_texture;

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    vec4 texColor = texture2D(u_texture, st);
    
    float r = abs(sin(u_time * 0.5 + st.x * 3.14));
    float g = abs(cos(u_time * 0.7 + st.y * 3.14));
    float b = abs(sin(u_time * 0.9 + (st.x + st.y) * 3.14));
    
    vec3 color = vec3(r, g, b);
    
    gl_FragColor = vec4(texColor.rgb * color, texColor.a);
}