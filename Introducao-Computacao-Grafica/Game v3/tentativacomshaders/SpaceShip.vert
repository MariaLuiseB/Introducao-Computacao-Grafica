#version 330 core

layout(location = 0) in vec3 inPosition;   // Posições dos vértices
layout(location = 1) in vec3 inNormal;     // Normais dos vértices

out vec3 vN;    // Vetor normal
out vec3 vL;    // Vetor do ponto para a luz
out vec3 vE;    // Vetor do ponto para o olho da câmera

uniform mat4 model;        // Matriz de modelo
uniform mat4 view;         // Matriz de visão
uniform mat4 projection;   // Matriz de projeção

uniform vec3 Light_location; // Posição da luz

void main()
{
    vec4 ECPosition = view * model * vec4(inPosition, 1.0); // Posição do olho

    vN = normalize(mat3(transpose(inverse(model))) * inNormal); // Vetor normal normalizado
    vL = Light_location - ECPosition.xyz; // Vetor do ponto para a luz
    vE = -ECPosition.xyz; // Vetor do ponto para o olho da câmera

    gl_Position = projection * ECPosition; // Posição final do vértice
}
