
import {GLTFLoader} from 'GLTFLoader.js';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 5;


var clock = new THREE.Clock();
// model
// gltfLoader = new THREE.GLTFLoader()
// gltfLoader.load( "/home/bachir/Downloads/upbge/monkyemove.glb", function ( model ) {
//     mixer= new THREE.AnimationMixer(model.scene);
//     model.animations.forEach((clip) => {mixer.clipAction(clip).play(); });
//     scene.add(model.scene)})

function animate() {
  requestAnimationFrame( animate );
  renderer.render( scene, camera );
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
}
animate();
// Our Javascript will go here.
