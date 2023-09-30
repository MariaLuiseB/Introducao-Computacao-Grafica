#version 330 core

uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;

uniform float Material_shininess;
uniform vec4 Material_specular;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;

in vec2 vST;
in vec3 vN;
in vec3 vL;
in vec3 vE;

out vec4 FragColor;

void main() {
    vec3 Normal = normalize(vN); // Normal da superfície do objeto
    vec3 Light = normalize(vL); // A luz está na origem, ou seja, é um vetor que aponta para a origem (0, 0, 0)
    vec3 Eye = normalize(vE); // O olho está na origem, ou seja, é um vetor que aponta para a origem (0, 0, 0)

    vec4 ambient = Global_ambient * Material_ambient;

    float d = max(dot(Normal, Light), 0);
    vec4 diffuse = Light_diffuse * d * Material_diffuse;

    float s = 0;
    vec3 ref = normalize(reflect(-Light, Normal));
    s = pow(max(dot(Eye, ref), 0.0), Material_shininess);

    vec4 specular = Light_specular * s * Material_specular;

    float attenuation = 1.0 / (1.0 + 0.0001 * pow(length(vL), 2));
    FragColor = ambient + attenuation * (diffuse + specular);
}
