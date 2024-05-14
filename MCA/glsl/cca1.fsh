
precision highp float;

uniform float param1; 
uniform float param2; 

varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

vec2 texOffset;
 

void main() {
  texOffset = 6.0 * (vec2(1.0,1.0) / (u_sprite_size * u_scale));
  
  vec2 tc0 = v_tex_coord.st + vec2(-texOffset.s, -texOffset.t);
  vec2 tc1 = v_tex_coord.st + vec2(         0.0, -texOffset.t);
  vec2 tc2 = v_tex_coord.st + vec2(+texOffset.s, -texOffset.t);
  vec2 tc3 = v_tex_coord.st + vec2(-texOffset.s,          0.0);
  vec2 tc4 = v_tex_coord.st + vec2(         0.0,          0.0);
  vec2 tc5 = v_tex_coord.st + vec2(+texOffset.s,          0.0);
  vec2 tc6 = v_tex_coord.st + vec2(-texOffset.s, +texOffset.t);
  vec2 tc7 = v_tex_coord.st + vec2(         0.0, +texOffset.t);
  vec2 tc8 = v_tex_coord.st + vec2(+texOffset.s, +texOffset.t);

  vec4 col0 = texture2D(u_texture, tc0);
  vec4 col1 = texture2D(u_texture, tc1);
  vec4 col2 = texture2D(u_texture, tc2);
  vec4 col3 = texture2D(u_texture, tc3);
  vec4 col4 = texture2D(u_texture, tc4);
  vec4 col5 = texture2D(u_texture, tc5);
  vec4 col6 = texture2D(u_texture, tc6);
  vec4 col7 = texture2D(u_texture, tc7);
  vec4 col8 = texture2D(u_texture, tc8);

  vec4 sum = (col0 + col1 + col2 + col3 + col5 + col6 + col7 + col8);
  vec4 avg = sum / 8.0;
  
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.993), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.906), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.914), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.930), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.933), 1.0); // Watching TV
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.934), 1.0); // Ditto
  
  // gl_FragColor = vec4(fract(avg.rgb/2.0 + 0.936), 1.0); // Awesome watching TV style shifter
  
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.937), 1.0); // Ditto
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.938), 1.0); // Ditto. More aggressive, less regular 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.939), 1.0); // Ditto. More fluid.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.94), 1.0);  // More fluid yet.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.944), 1.0); // Wormy
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.946), 1.0); // Even more wormy.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.947), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.948), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.949), 1.0); 
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.951), 1.0); // Wormy, kaleidoscope-y start
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.958), 1.0); // Finally different. skip_iters = 3
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.96), 1.0); // skip_iters=3
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.961), 1.0); // skip_iters=3 ... kinda getting bigger?
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.962), 1.0); //
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.963), 1.0); // Static.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.967), 1.0); // Nice watching tv style shifter variation
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.969), 1.0); // Ditto
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.97), 1.0); // Ditto; slow paced.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.971), 1.0); // Interesting to watch over time.
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.986), 1.0); // can develop structure like .993
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.989), 1.0); // Start at skip_iters=5. Sometimes agar fills space. Skip_iters=4
  //gl_FragColor = vec4(fract(avg.rgb/2 + 0.988), 1.0); // Similar to above but agar is ubiquitous.
  
   // ditto and instantaneous.
  // gl_FragColor = vec4(fract(avg.rgb/2.0 + 0.993), 1.0); 
  
  
  //gl_FragColor = vec4(fract(avg.rgb/2 + 3 * 0.31830988618), 1.0); //  3/PI
  
  /* Faves 
     .993
     .515
     .51437
  */ 
  
  gl_FragColor = vec4(fract(avg.rgb * param1 + param2), 1.0); // 
}
