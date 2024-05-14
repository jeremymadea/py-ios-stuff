
precision highp float;

varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

vec2 to;

uniform float p1
uniform float p2



void main() {
   
  // texture coords
  vec2 to = (1.0/u_sprite_size) * u_scale;

 // vec2 xy = v_tex_coord.st + 
 // 	(vec2(to.s, 0.0));
  	
 // vec2 nc = v_tex_coord + (to *  10.0);

  vec4 oc = texture2D(u_texture, nc);
  //float c = fract(u_time)/2.0;
  vec4 tmp = oc;
  vec4 cc = vec4(tmp.gbr,1.0);

  gl_FragColor = cc;
      
	 
}
