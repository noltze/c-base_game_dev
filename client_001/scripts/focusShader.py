// # One pass DoF shader with noise

uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;
uniform float timer;
uniform float focus;
 
const float bluriness = 8.0; //blur amount: bigger values for shallower depth of field
 
vec2 rand(vec2 co)
{
	float noise1 =  (fract(sin(dot(co ,vec2(12.9898,78.233)+timer)) * 43758.5453));
	float noise2 =  (fract(sin(dot(co ,vec2(12.9898,78.233)*2.0)+timer) * 43758.5453));
	return clamp(vec2(noise1,noise2),0.0,1.0);
}

void main() 
{
	float depth = texture2D( bgl_DepthTexture, gl_TexCoord[0].xy).r;

	float factor = ( depth - focus );
	 
	float dofblur = clamp( factor * bluriness * 0.01, -0.01, 0.01 );

	vec2 noise = rand(gl_TexCoord[0].xy);

	vec4 col = vec4(0.0);

	float X1 = gl_TexCoord[0].x  + noise.x * dofblur;
	float Y1 = gl_TexCoord[0].y  + noise.y * dofblur;
	float X2 = gl_TexCoord[0].x  - noise.x * dofblur;
	float Y2 = gl_TexCoord[0].y  - noise.y * dofblur;
	
	float invX1 = gl_TexCoord[0].x  + (1.0-noise.x) * dofblur * 0.5;
	float invY1 = gl_TexCoord[0].y  + (1.0-noise.y) * dofblur * 0.5;
	float invX2 = gl_TexCoord[0].x  - (1.0-noise.x) * dofblur * 0.5;
	float invY2 = gl_TexCoord[0].y  - (1.0-noise.y) * dofblur * 0.5;
	
	float invX3 = gl_TexCoord[0].x  + (1.0-noise.x) * dofblur * 2.0;
	float invY3 = gl_TexCoord[0].y  + (1.0-noise.y) * dofblur * 2.0;
	float invX4 = gl_TexCoord[0].x  - (1.0-noise.x) * dofblur * 2.0;
	float invY4 = gl_TexCoord[0].y  - (1.0-noise.y) * dofblur * 2.0;
	
	col += texture2D(bgl_RenderedTexture, vec2(X1, Y1))*0.075;
	col += texture2D(bgl_RenderedTexture, vec2(X2, Y2))*0.075;
	col += texture2D(bgl_RenderedTexture, vec2(X1, Y2))*0.075;
	col += texture2D(bgl_RenderedTexture, vec2(X2, Y1))*0.075;
	
	col += texture2D(bgl_RenderedTexture, vec2(invX1, invY1))*0.125;
	col += texture2D(bgl_RenderedTexture, vec2(invX2, invY2))*0.125;
	col += texture2D(bgl_RenderedTexture, vec2(invX1, invY2))*0.125;
	col += texture2D(bgl_RenderedTexture, vec2(invX2, invY1))*0.125;
	
	col += texture2D(bgl_RenderedTexture, vec2(invX3, invY3))*0.05;
	col += texture2D(bgl_RenderedTexture, vec2(invX4, invY4))*0.05;
	col += texture2D(bgl_RenderedTexture, vec2(invX3, invY4))*0.05;
	col += texture2D(bgl_RenderedTexture, vec2(invX4, invY3))*0.05;
	
	gl_FragColor = col;
	gl_FragColor.a = 1.0;
}