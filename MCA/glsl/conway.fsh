#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform float param1; 
uniform float param2; 
uniform float weight; 

uniform sampler2D texture;
uniform vec2 texOffset;

varying vec4 vertColor;
varying vec4 vertTexCoord;

const vec4 lumcoeff = vec4(0.299, 0.587, 0.114, 0);

float conway(float c, float hoodavg) { 
    if (c > .5) {
      if (hoodavg >= .25 && hoodavg <= .375) return 1.0; 
      return 0; 
    } else {  
      if (hoodavg == .375) return 1.0;
      return 0; 
    } 
}

void main() {
  vec2 tc0 = vertTexCoord.st + vec2(-texOffset.s, -texOffset.t); //TL
  vec2 tc1 = vertTexCoord.st + vec2(         0.0, -texOffset.t); //TC
  vec2 tc2 = vertTexCoord.st + vec2(+texOffset.s, -texOffset.t); //TR
  vec2 tc3 = vertTexCoord.st + vec2(-texOffset.s,          0.0); //ML 
  vec2 tc4 = vertTexCoord.st + vec2(         0.0,          0.0); //MC
  vec2 tc5 = vertTexCoord.st + vec2(+texOffset.s,          0.0); //MR
  vec2 tc6 = vertTexCoord.st + vec2(-texOffset.s, +texOffset.t); //BL
  vec2 tc7 = vertTexCoord.st + vec2(         0.0, +texOffset.t); //BC
  vec2 tc8 = vertTexCoord.st + vec2(+texOffset.s, +texOffset.t); //BR

  vec4 col0 = texture2D(texture, tc0);
  vec4 col1 = texture2D(texture, tc1);
  vec4 col2 = texture2D(texture, tc2);
  vec4 col3 = texture2D(texture, tc3);
  vec4 col4 = texture2D(texture, tc4);
  vec4 col5 = texture2D(texture, tc5);
  vec4 col6 = texture2D(texture, tc6);
  vec4 col7 = texture2D(texture, tc7);
  vec4 col8 = texture2D(texture, tc8);

  vec4 sum = (col0 + col1 + col2 + col3 + col5 + col6 + col7 + col8);
       sum += weight * col4;

  vec4 avg = sum / (8 + weight);

  //gl_FragColor = vec4(fract(avg.rgb * param1 + param2), 1.0); //
  gl_FragColor = vec4(conway(col4.r, avg.r), 
                      conway(col4.g, avg.g), 
                      conway(col4.b, avg.b), 1.0); //
}
