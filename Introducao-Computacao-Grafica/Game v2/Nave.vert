#version 330 compatibility

uniform vec4 global_ambient;
uniform vec4 light_ambient;
uniform vec4 light_diffuse;
uniform vec4 light_specular;
uniform vec3 light_location;

out vec3 vN;    // Vetor normal
out vec3 vL;    // Vetor do ponto para a luz
out vec3 vE;    // Vetor do ponto para o olho da câmera

void main() {
    vec4 ECPosition = ModelViewMatrix * inVertex;
    gl_FrontColor = gl_Color;

    vN = normalize(gl_NormalMatrix * gl_Normal); 
    vL = light_location - ECPosition.xyz;

    vE = vec3(0.0, 0.0, 0.0) - ECPosition.xyz;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
