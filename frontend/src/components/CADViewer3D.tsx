import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Environment, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

interface CADViewerProps {
  modelData?: any;
  onModelClick?: (object: THREE.Object3D) => void;
}

// Sample Wing Mesh Component
const WingMesh: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  // Create simple wing geometry (can be replaced with loaded CAD model)
  const createWingGeometry = () => {
    const shape = new THREE.Shape();

    // Root chord
    shape.moveTo(0, 0);
    shape.lineTo(2, 0);
    shape.lineTo(1.5, 10); // Tip chord (tapered)
    shape.lineTo(0, 10);
    shape.lineTo(0, 0);

    const extrudeSettings = {
      depth: 0.15,
      bevelEnabled: true,
      bevelThickness: 0.02,
      bevelSize: 0.02,
      bevelSegments: 3,
    };

    return new THREE.ExtrudeGeometry(shape, extrudeSettings);
  };

  return (
    <mesh ref={meshRef} position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
      <primitive object={createWingGeometry()} />
      <meshStandardMaterial
        color="#2196f3"
        metalness={0.3}
        roughness={0.4}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

// Sample Fuselage Component
const FuselageMesh: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <mesh ref={meshRef} position={[1, 1, 0]} rotation={[0, 0, Math.PI / 2]}>
      <cylinderGeometry args={[0.5, 0.5, 8, 32]} />
      <meshStandardMaterial color="#90a4ae" metalness={0.5} roughness={0.3} />
    </mesh>
  );
};

// Main 3D Scene
const Scene: React.FC = () => {
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
      <pointLight position={[-10, -10, -5]} intensity={0.5} />

      {/* Sample Aircraft Components */}
      <WingMesh />
      <FuselageMesh />

      {/* Grid */}
      <Grid args={[20, 20]} cellSize={1} cellColor="#6e6e6e" sectionColor="#3f3f3f" />
    </>
  );
};

const CADViewer3D: React.FC<CADViewerProps> = ({ modelData, onModelClick }) => {
  return (
    <div style={{ width: '100%', height: '100%', background: '#1a1a1a' }}>
      <Canvas shadows camera={{ position: [15, 15, 15], fov: 50 }}>
        <PerspectiveCamera makeDefault position={[15, 15, 15]} />

        {/* Controls */}
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          rotateSpeed={0.5}
          zoomSpeed={0.8}
          minDistance={5}
          maxDistance={100}
        />

        {/* Environment */}
        <Environment preset="sunset" />

        {/* Scene */}
        <Scene />
      </Canvas>
    </div>
  );
};

export default CADViewer3D;
