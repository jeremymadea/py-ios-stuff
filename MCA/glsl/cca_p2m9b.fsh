
precision highp float;


// Standard uniforms
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;


// User Supplied Parameters
uniform float p1; 
uniform float p2; 
uniform float o_weight; // orig cell
uniform float a_weight; // adjacent cells
uniform float c_weight; // corner cells

// offset vector
vec2 to;

void main() {
  //to = u_scale * (vec2(1.0,1.0) / u_sprite_size);
  to = (vec2(1.0,1.0) / u_sprite_size); 
  
  
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
  vec4 col0 = texture2D(u_texture, tc0); // UL
  vec4 col1 = texture2D(u_texture, tc1); // UC
  vec4 col2 = texture2D(u_texture, tc2); // UR
  vec4 col3 = texture2D(u_texture, tc3); // ML
  vec4 col4 = texture2D(u_texture, tc4); // MC
  vec4 col5 = texture2D(u_texture, tc5); // MR
  vec4 col6 = texture2D(u_texture, tc6); // BL
  vec4 col7 = texture2D(u_texture, tc7); // BC
  vec4 col8 = texture2D(u_texture, tc8); // BR

  vec4 sum = (
      c_weight * (col0 + col3 + col6 + col8) +
      a_weight * (col1 + col3 + col5 + col7) + 
      o_weight * col4
  );
  float n = o_weight + 4.0 * (a_weight + c_weight);
  vec4 avg = sum / n; 

	gl_FragColor = vec4(
		fract(avg.rrr * p1 + p2), 1.0
	);
  
}
