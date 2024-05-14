
precision highp float;

uniform float p1; 
uniform float p2; 

varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

vec2 to;
 

void main() {
  to = u_scale * (vec2(1.0,1.0) / u_sprite_size) ;
  
  // texture coords
  vec2 tc0 = v_tex_coord.st + vec2(-to.s, -to.t);
  vec2 tc1 = v_tex_coord.st + vec2(  0.0, -to.t);
  vec2 tc2 = v_tex_coord.st + vec2( to.s, -to.t);
  vec2 tc3 = v_tex_coord.st + vec2(-to.s,  0.0);
  vec2 tc4 = v_tex_coord.st + vec2(  0.0,  0.0);
  vec2 tc5 = v_tex_coord.st + vec2( to.s,  0.0);
  vec2 tc6 = v_tex_coord.st + vec2(-to.s,  to.t);
  vec2 tc7 = v_tex_coord.st + vec2(  0.0,  to.t);
  vec2 tc8 = v_tex_coord.st + vec2( to.s,  to.t);

  // colors 
  vec4 col0 = texture2D(u_texture, tc0);
  vec4 col1 = texture2D(u_texture, tc1);
  vec4 col2 = texture2D(u_texture, tc2);
  vec4 col3 = texture2D(u_texture, tc3);
  vec4 col4 = texture2D(u_texture, tc4);
  vec4 col5 = texture2D(u_texture, tc5);
  vec4 col6 = texture2D(u_texture, tc6);
  vec4 col7 = texture2D(u_texture, tc7);
  vec4 col8 = texture2D(u_texture, tc8);

  vec4 sum = (
      col0 + col1 + col2 + col3 + col4 +
      col5 + col6 + col7 + col8);
  vec4 avg = sum / 9.0; 

	gl_FragColor = vec4(
		fract(avg.rrr * p1 + p2), 1.0
	);
  
}
