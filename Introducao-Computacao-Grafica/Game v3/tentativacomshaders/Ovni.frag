#version 330 compatibility

in vec3 fragNormal;
in vec3 fragLightDir;

out vec4 fragColor;

uniform vec4 materialAmbient;
uniform vec4 materialDiffuse;
uniform vec4 materialSpecular;
uniform float materialShininess;

uniform vec4 lightAmbient;
uniform vec4 lightDiffuse;
uniform vec4 lightSpecular;

void main() {
    vec3 normalizedNormal = normalize(fragNormal);
    vec3 normalizedLightDir = normalize(fragLightDir);
    
    // Cálculo da iluminação difusa
    float diffuseFactor = max(dot(normalizedNormal, normalizedLightDir), 0.0);
    vec4 diffuseColor = materialDiffuse * lightDiffuse * diffuseFactor;
    
    // Cálculo da iluminação especular
    vec3 viewDir = normalize(-vec3(gl_FragCoord));
    vec3 reflectDir = reflect(-normalizedLightDir, normalizedNormal);
    float specularFactor = pow(max(dot(viewDir, reflectDir), 0.0), materialShininess);
    vec4 specularColor = materialSpecular * lightSpecular * specularFactor;
    
    // Cor final do fragmento com iluminação
    vec4 finalColor = materialAmbient + diffuseColor + specularColor;
    
    fragColor = finalColor;
}
