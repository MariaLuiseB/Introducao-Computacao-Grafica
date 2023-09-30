#version 330 compatibility

out vec4 vColor;

void main() {
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	vColor = gl_Position.zyxw;
}