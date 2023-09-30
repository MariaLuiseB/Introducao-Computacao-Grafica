#version 330 compatibility

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 lightPosition;  // Posição da luz

in vec4 inVertex;
in vec3 inNormal;  // Normal do vértice

out vec3 fragNormal;
out vec3 fragLightDir;

void main() {
    gl_Position = projectionMatrix * modelViewMatrix * inVertex;
    
    fragNormal = mat3(modelViewMatrix) * inNormal;  // Transformar a normal para espaço de visão
    fragLightDir = lightPosition - inVertex.xyz;
}
