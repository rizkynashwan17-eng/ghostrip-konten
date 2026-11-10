// Reels gaya "BEDAH TEKNIKAL" (PATEN 5 Nov 2026, selang-seling dengan gaya WhatIf).
// Acuan cara main: video penjelas teknikal ala "kita bedah" — ilustrasi 3D clay/isometrik yang membedah komponen,
// judul kecil (kicker) + judul tebal dengan kata miring di atas, subtitle per frasa dengan kata yang sedang diucapkan
// menyala, label penunjuk, kartu kutipan sumber, kata besar ("BLONG!"), tag "ILUSTRASI".
// Warna WAJIB brand Ghostrip (theme.ts): navy/teal, krem, aksen mint & oranye, font Outfit.
import React, {useMemo, useState} from 'react';
import {
  AbsoluteFill, Audio, Img, Sequence, continueRender, delayRender, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {C, FPS, H, W} from './theme';

const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const eo = Easing.bezier(0.16, 1, 0.3, 1);
const F = 'Outfit';
const MONO = 'ui-monospace, "DejaVu Sans Mono", monospace';

export type BedahChunk = {text: string; from: number; to: number};
export type BedahScene = {
  type: string; from: number; dur: number; narasi: string; chunks: BedahChunk[];
  kicker?: string; judul?: string; label?: {t: string; x: number; y: number; warna?: string; dari?: number}[];
  kutipan?: {teks: string; sumber: string; tgl?: string; dari?: number; kutip?: boolean}; boom?: string; boomDari?: number;
  ilustrasi?: string; [k: string]: any;
};
export type BedahProps = {scenes: BedahScene[]; durationInFrames: number; narasi?: string | null; musik?: string | null; whoosh?: string | null};

const useOutfit = () => {
  const [h] = useState(() => delayRender('font'));
  React.useEffect(() => {
    const f = new FontFace('Outfit', `url(${staticFile('Outfit.ttf')})`, {weight: '100 900'});
    f.load().then((ff) => { (document.fonts as any).add(ff); continueRender(h); });
  }, [h]);
};

/* ============================ 3D: bahan & model ============================ */
const mat = (color: string, extra: Partial<THREE.MeshStandardMaterialParameters> = {}) =>
  new THREE.MeshStandardMaterial({color, roughness: 0.78, metalness: 0.05, ...extra});

const Truk: React.FC<{f: number; roda?: number}> = ({f, roda = 1}) => {
  const rot = -f * 0.25 * roda;
  const wheel = (x: number, z: number, k: string) => (
    <group key={k} position={[x, 0.42, z]} rotation={[Math.PI / 2, 0, 0]}>
      <mesh castShadow rotation={[0, rot, 0]}><cylinderGeometry args={[0.42, 0.42, 0.32, 28]} /><meshStandardMaterial color="#1b2328" roughness={0.9} /></mesh>
      <mesh position={[0, z > 0 ? 0.17 : -0.17, 0]}><cylinderGeometry args={[0.2, 0.2, 0.02, 20]} /><meshStandardMaterial color="#9aa7ab" roughness={0.5} metalness={0.4} /></mesh>
    </group>
  );
  return (
    <group>
      {/* sasis */}
      <mesh castShadow receiveShadow position={[0.2, 0.62, 0]}><boxGeometry args={[6.4, 0.22, 1.5]} /><meshStandardMaterial color="#26343a" roughness={0.8} /></mesh>
      {/* kabin teal */}
      <mesh castShadow position={[2.75, 1.55, 0]}><boxGeometry args={[1.5, 1.7, 1.9]} /><meshStandardMaterial color={C.tealSoft} roughness={0.6} /></mesh>
      <mesh castShadow position={[3.52, 1.82, 0]}><boxGeometry args={[0.06, 0.8, 1.7]} /><meshStandardMaterial color="#0b1f27" roughness={0.2} metalness={0.3} /></mesh>
      <mesh position={[3.53, 1.0, 0]}><boxGeometry args={[0.05, 0.16, 1.92]} /><meshStandardMaterial color={C.mint} emissive={C.mint} emissiveIntensity={0.25} /></mesh>
      {/* bak muatan krem */}
      <mesh castShadow receiveShadow position={[-0.55, 1.75, 0]}><boxGeometry args={[4.6, 2.1, 2.0]} /><meshStandardMaterial color={C.cream} roughness={0.85} /></mesh>
      <mesh position={[-0.55, 1.75, 1.005]}><boxGeometry args={[4.4, 0.12, 0.01]} /><meshStandardMaterial color={C.orange} /></mesh>
      {wheel(2.7, 0.8, 'a')}{wheel(2.7, -0.8, 'b')}{wheel(-1.2, 0.8, 'c')}{wheel(-1.2, -0.8, 'd')}{wheel(-2.2, 0.8, 'e')}{wheel(-2.2, -0.8, 'f')}
    </group>
  );
};

/* Jalan menurun: dunia dimiringkan, marka & tiang bergerak → kesan meluncur */
const AdeganJalan: React.FC<{f: number; s: BedahScene}> = ({f, s}) => {
  const speed = s.laju ?? 0.22; // satuan dunia / frame
  const off = ((f * speed) % 4 + 4) % 4;
  const slope = s.miring ?? 0.16;
  const zoom = interpolate(f, [0, s.dur], [s.zoom0 ?? 64, s.zoom1 ?? 74], cl);
  const shake = (s.goyang ?? 0) * Math.sin(f * 1.7) * 0.03;
  return (
    <ThreeCanvas width={W} height={H} shadows orthographic camera={{position: [128, 104, 128], zoom, near: 0.1, far: 4000}}
      style={{position: 'absolute', inset: 0}} gl={{antialias: true, preserveDrawingBuffer: true}}>
      <color attach="background" args={[C.night1]} />
      <ambientLight intensity={0.75} />
      <hemisphereLight args={['#fff7e8', '#9fb3b0', 0.55]} />
      <directionalLight castShadow position={[8, 18, 6]} intensity={1.35} shadow-mapSize-width={1024} shadow-mapSize-height={1024}
        shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} />
      <group rotation={[0, 0, slope]} position={[0, shake, 0]}>
        <mesh receiveShadow position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[400, 400]} /><meshStandardMaterial color="#0f3540" roughness={1} /></mesh>\n        <gridHelper args={[400, 200, "#2fb8a0", "#1d5a63"]} position={[0, 0.003, 0]} />
        <mesh receiveShadow position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[400, 4.2]} /><meshStandardMaterial color="#16262d" roughness={0.95} /></mesh>
        {Array.from({length: 22}).map((_, i) => (
          <mesh key={i} position={[-40 + i * 4 - off, 0.012, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[2, 0.14]} /><meshStandardMaterial color="#f2ead9" /></mesh>
        ))}
        {Array.from({length: 12}).map((_, i) => (
          <group key={'p' + i} position={[-40 + i * 8 - ((f * speed) % 8), 0, -2.7]}>
            <mesh castShadow position={[0, 0.45, 0]}><boxGeometry args={[0.16, 0.9, 0.16]} /><meshStandardMaterial color={C.steel} /></mesh>
            <mesh castShadow position={[0, 0.8, 0]}><boxGeometry args={[0.2, 0.14, 0.2]} /><meshStandardMaterial color={C.orange} /></mesh>
          </group>
        ))}
        <mesh castShadow position={[0, 0.75, -2.7]}><boxGeometry args={[400, 0.12, 0.08]} /><meshStandardMaterial color="#9aa7ab" metalness={0.3} roughness={0.5} /></mesh>
        <group position={[s.trukX ?? 0, 0, 0.3]}><Truk f={f} roda={speed / 0.22} /></group>
        {/* panah mint "mesin menahan" */}
        {s.panahMesin && (
          <group position={[(s.trukX ?? 0) + 2.6, 3.4, 0.3]}>
            {[0, 1, 2].map((k) => {
              const a = ((f / 18 + k / 3) % 1);
              return <mesh key={k} position={[-a * 3.2, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
                <coneGeometry args={[0.45, 0.9, 4]} /><meshStandardMaterial color={C.mintDeep} emissive={C.mint} emissiveIntensity={0.3} transparent opacity={Math.min(1, (1 - a) * 1.6)} /></mesh>;
            })}
          </group>
        )}
      </group>
    </ThreeCanvas>
  );
};

/* Potongan tromol rem: kampas menekan tromol, panas menumpuk (emissive oranye→merah) */
const AdeganRem: React.FC<{f: number; s: BedahScene}> = ({f, s}) => {
  const p0 = s.panas0 ?? 0, p1 = s.panas1 ?? 0;
  const heat = interpolate(f, [0, s.dur * 0.85], [p0, p1], {...cl, easing: Easing.inOut(Easing.quad)});
  const press = s.tekan ? 0.5 + 0.5 * Math.sin(f / 7) : 0.15;
  const spin = -f * (s.putar ?? 0.08);
  const drumCol = new THREE.Color('#7f8b90').lerp(new THREE.Color('#ff6a2a'), Math.min(1, heat));
  const lining = new THREE.Color('#5a3b2a').lerp(new THREE.Color('#ffb27a'), Math.min(1, heat * 0.9));
  const camA = interpolate(f, [0, s.dur], [0.0, 0.35], cl);
  const shoe = (side: number) => (
    <group rotation={[0, 0, side > 0 ? 0 : Math.PI]}>
      <group position={[press * 0.06, 0, 0]}>
        <mesh castShadow rotation={[0, 0, -Math.PI * 0.42]}><torusGeometry args={[1.72, 0.12, 12, 40, Math.PI * 0.84]} /><meshStandardMaterial color="#c9d2d4" metalness={0.35} roughness={0.45} /></mesh>
        <mesh rotation={[0, 0, -Math.PI * 0.4]}><torusGeometry args={[1.86, 0.07, 10, 40, Math.PI * 0.8]} /><meshStandardMaterial color={lining} emissive={lining} emissiveIntensity={heat * 0.8} roughness={0.9} /></mesh>
      </group>
    </group>
  );
  return (
    <ThreeCanvas width={W} height={H} shadows camera={{position: [Math.sin(camA) * 12.5, 2.2, Math.cos(camA) * 12.5], fov: 34}}
      style={{position: 'absolute', inset: 0}} gl={{antialias: true, preserveDrawingBuffer: true}}>
      <color attach="background" args={[C.night1]} />
      <ambientLight intensity={0.7} />
      <hemisphereLight args={['#fff7e8', '#8fa6a3', 0.5]} />
      <directionalLight castShadow position={[5, 9, 7]} intensity={1.3} />
      <pointLight position={[0, 0, 1.2]} intensity={heat * 6} color="#ff8a3a" distance={6} />
      <group position={[0, 0.35, 0]} rotation={[0.22, -0.55, 0]}>
        {/* tromol (dipotong 3/4 supaya isi terlihat) */}
        <group rotation={[Math.PI / 2, spin, 0]}>
          <mesh castShadow><cylinderGeometry args={[2.1, 2.1, 1.1, 64, 1, true, 0.4, Math.PI * 1.55]} /><meshStandardMaterial color={drumCol} emissive={drumCol} emissiveIntensity={heat * 0.55} side={THREE.DoubleSide} metalness={0.45} roughness={0.5} /></mesh>
          <mesh position={[0, -0.55, 0]}><cylinderGeometry args={[2.1, 2.1, 0.12, 64]} /><meshStandardMaterial color="#9aa6aa" metalness={0.35} roughness={0.5} /></mesh>
          {Array.from({length: 8}).map((_, i) => (
            <mesh key={i} position={[Math.cos(i * Math.PI / 4) * 1.1, -0.64, Math.sin(i * Math.PI / 4) * 1.1]}><cylinderGeometry args={[0.09, 0.09, 0.2, 10]} /><meshStandardMaterial color="#d8dde0" metalness={0.6} roughness={0.3} /></mesh>
          ))}
        </group>
        {/* sepatu rem + kampas */}
        <group position={[0, 0, 0.05]}>{shoe(1)}{shoe(-1)}</group>
        {/* S-cam & as */}
        <mesh position={[0, -1.25, 0.1]} rotation={[0, 0, f * 0.0 + (s.tekan ? press * 0.6 : 0)]}><boxGeometry args={[0.5, 0.22, 0.3]} /><meshStandardMaterial color={C.orange} /></mesh>
        <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0, -0.9]}><cylinderGeometry args={[0.2, 0.2, 1.0, 20]} /><meshStandardMaterial color="#3c4a50" metalness={0.4} roughness={0.5} /></mesh>
      </group>
      {/* uap panas */}
      {heat > 0.55 && Array.from({length: 7}).map((_, i) => {
        const a = ((f / 40 + i / 7) % 1);
        return <mesh key={'u' + i} position={[-1.2 + i * 0.4, 1.8 + a * 2.2, 0.6]}><sphereGeometry args={[0.12 + a * 0.25, 12, 12]} /><meshStandardMaterial color="#ffffff" transparent opacity={(1 - a) * 0.45 * (heat - 0.5) * 2} /></mesh>;
      })}
    </ThreeCanvas>
  );
};

/* Tabung angin + pipa ke rem: titik udara mengalir tiap pedal diinjak */
const AdeganAngin: React.FC<{f: number; s: BedahScene}> = ({f, s}) => {
  const curve = useMemo(() => new THREE.CatmullRomCurve3([
    new THREE.Vector3(1.9, 0, 0), new THREE.Vector3(2.8, 0.2, 0.4), new THREE.Vector3(3.2, -1.2, 0.6), new THREE.Vector3(3.6, -2.4, 0.2)]), []);
  const tube = useMemo(() => new THREE.TubeGeometry(curve, 60, 0.09, 10, false), [curve]);
  const pulses = s.injak ?? 4;
  const dots = Array.from({length: 14}).map((_, i) => {
    const t = ((f / 45) + i / 14) % 1;
    return curve.getPoint(t);
  });
  const level = interpolate(f, [0, s.dur * 0.9], [s.bar0 ?? 8, s.bar1 ?? 6.4], cl);
  const fill = Math.max(0.05, (level - 4) / 5);
  return (
    <ThreeCanvas width={W} height={H} shadows camera={{position: [4.5, 3.6, 13.5], fov: 36}} style={{position: 'absolute', inset: 0}} gl={{antialias: true, preserveDrawingBuffer: true}}>
      <color attach="background" args={[C.night1]} />
      <ambientLight intensity={0.75} />
      <hemisphereLight args={['#fff7e8', '#8fa6a3', 0.5]} />
      <directionalLight castShadow position={[4, 10, 6]} intensity={1.25} />
      <group position={[-0.2, 0.6, 0]} rotation={[0, -0.25, 0]} scale={0.72}>
        {/* tabung */}
        <group rotation={[0, 0, Math.PI / 2]}>
          <mesh castShadow><cylinderGeometry args={[0.9, 0.9, 3.2, 40]} /><meshStandardMaterial color="#6fa3aa" roughness={0.45} metalness={0.25} transparent opacity={0.6} /></mesh>
          <mesh position={[0, 1.6, 0]} castShadow><sphereGeometry args={[0.9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color="#6fa3aa" roughness={0.45} transparent opacity={0.6} /></mesh>
          <mesh position={[0, -1.6, 0]} rotation={[Math.PI, 0, 0]} castShadow><sphereGeometry args={[0.9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color="#6fa3aa" roughness={0.45} transparent opacity={0.6} /></mesh>
          {/* isi udara */}
          <mesh position={[0, 0, 0]}><cylinderGeometry args={[0.8 * Math.sqrt(fill) + 0.05, 0.8 * Math.sqrt(fill) + 0.05, 3.0, 32]} /><meshStandardMaterial color={C.mint} emissive={C.mint} emissiveIntensity={0.35} transparent opacity={0.6} /></mesh>
        </group>
        <mesh castShadow position={[-0.6, -1.0, 0]}><boxGeometry args={[0.2, 0.3, 1.6]} /><meshStandardMaterial color="#3c4a50" /></mesh>
        <mesh castShadow position={[0.8, -1.0, 0]}><boxGeometry args={[0.2, 0.3, 1.6]} /><meshStandardMaterial color="#3c4a50" /></mesh>
        <mesh geometry={tube}><meshStandardMaterial color="#9aa7ab" metalness={0.3} roughness={0.5} /></mesh>
        {dots.map((p, i) => <mesh key={i} position={p}><sphereGeometry args={[0.1, 12, 12]} /><meshStandardMaterial color="#ffffff" emissive={C.mint} emissiveIntensity={0.5} /></mesh>)}
        {/* bilik rem */}
        <mesh castShadow position={[3.6, -2.6, 0.2]}><cylinderGeometry args={[0.45, 0.45, 0.5, 28]} /><meshStandardMaterial color="#c9d2d4" metalness={0.35} roughness={0.45} /></mesh>
      </group>
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -3, 0]}><planeGeometry args={[60, 60]} /><meshStandardMaterial color="#0f3540" /></mesh><gridHelper args={[60, 40, "#2fb8a0", "#1d5a63"]} position={[0, -2.99, 0]} />
      {pulses > 0 && null}
    </ThreeCanvas>
  );
};

/* Ban truk dibelah: tekanan angin, lentur dinding samping, panas, beban, pecah */
const BanSatu: React.FC<{f: number; s: BedahScene; p: number; heat: number; x: number; sc: number; beban: number; pecah: number}> = ({f, s, p, heat, x, sc, beban, pecah}) => {
  const R = 1.65, T = 0.62, ROUT = R + T;
  const sq = 0.02 + (1 - p) * 0.3 + Math.max(0, beban - 1) * 0.22;
  const spin = -f * (s.putar ?? 0.07);
  const rubber = new THREE.Color('#2a343a').lerp(new THREE.Color('#ff5a1f'), Math.min(1, heat));
  const arc = Math.PI * 1.72;
  const k = pecah < 0 ? 1 : Math.max(0, 1 - pecah / 5);
  const wobble = (1 - p) * 0.035 * Math.sin(f / 3.2);
  const nArrow = 14;
  return (
    <group position={[x, -ROUT * sq * sc, 0]} scale={[sc * (1 + sq * 0.7 + wobble) * k, sc * (1 - sq) * k, sc * k]}>
      <group rotation={[0, 0, spin]}>
        <mesh castShadow rotation={[0, 0, 0]}>
          <torusGeometry args={[R, T, 22, 72, arc]} />
          <meshStandardMaterial color={rubber} emissive={rubber} emissiveIntensity={heat * 0.75} roughness={0.8} side={THREE.DoubleSide} transparent opacity={0.88} />
        </mesh>
        {Array.from({length: 38}).map((_, i) => {
          const a = (i / 38) * arc;
          return <mesh key={i} position={[Math.cos(a) * (R + T + 0.05), Math.sin(a) * (R + T + 0.05), 0]} rotation={[0, 0, a]}>
            <boxGeometry args={[0.16, 0.2, 1.05]} /><meshStandardMaterial color={rubber} emissive={rubber} emissiveIntensity={heat * 0.7} roughness={0.9} /></mesh>;
        })}
      </group>
      {/* velg */}
      <group rotation={[Math.PI / 2, spin, 0]}>
        <mesh castShadow><cylinderGeometry args={[1.02, 1.02, 0.7, 40]} /><meshStandardMaterial color="#aeb9bd" metalness={0.55} roughness={0.35} /></mesh>
        <mesh position={[0, 0.37, 0]}><cylinderGeometry args={[0.42, 0.42, 0.12, 24]} /><meshStandardMaterial color="#e3e9eb" metalness={0.5} roughness={0.3} /></mesh>
        {Array.from({length: 8}).map((_, i) => <mesh key={i} position={[Math.cos(i * Math.PI / 4) * 0.7, 0.4, Math.sin(i * Math.PI / 4) * 0.7]}><cylinderGeometry args={[0.07, 0.07, 0.1, 10]} /><meshStandardMaterial color="#6d7a80" metalness={0.6} /></mesh>)}
      </group>
      {/* panah tekanan di dalam: makin penuh makin panjang */}
      {s.panah !== false && Array.from({length: nArrow}).map((_, i) => {
        const a = (i / nArrow) * Math.PI * 2 + spin;
        const pulse = 0.85 + 0.15 * Math.sin(f / 6 + i);
        const len = (0.25 + 0.55 * p) * pulse;
        return <mesh key={i} position={[Math.cos(a) * (1.22 + len / 2), Math.sin(a) * (1.22 + len / 2), 0.0]} rotation={[0, 0, a - Math.PI / 2]}>
          <coneGeometry args={[0.13, len, 6]} /><meshStandardMaterial color={C.mint} emissive={C.mint} emissiveIntensity={0.55} /></mesh>;
      })}
    </group>
  );
};

const AdeganBan: React.FC<{f: number; s: BedahScene}> = ({f, s}) => {
  const dur = s.dur;
  const p = interpolate(f, [0, dur * 0.85], [s.p0 ?? 1, s.p1 ?? s.p0 ?? 1], {...cl, easing: Easing.inOut(Easing.quad)});
  const heat = interpolate(f, [0, dur * 0.85], [s.panas0 ?? 0, s.panas1 ?? s.panas0 ?? 0], {...cl, easing: Easing.inOut(Easing.quad)});
  const beban = s.beban ? interpolate(f, [0, dur * 0.85], [s.beban0 ?? s.beban, s.beban], cl) : 0;
  const pd = s.pecahDi ?? -1;
  const pecah = pd >= 0 && f >= pd ? f - pd : -1;
  const camA = interpolate(f, [0, dur], [-0.12, 0.2], cl);
  const ganda = !!s.ganda;
  const sc = ganda ? 0.72 : 1;
  const ROUT = 2.27;
  const sq = (pp: number) => 0.02 + (1 - pp) * 0.3 + Math.max(0, beban - 1) * 0.22;
  const topY = ROUT * sc * (1 - sq(p)) - ROUT * sc * sq(p) * 1;
  const frag = Array.from({length: 22}).map((_, i) => {
    const a = (i / 22) * Math.PI * 2, v = 0.18 + ((i * 37) % 10) / 40;
    const t = Math.max(0, pecah);
    return {x: Math.cos(a) * v * t * 1.2, y: Math.sin(a) * v * t * 1.2 - 0.004 * t * t, z: ((i * 13) % 7 - 3) * 0.12 * t * 0.2, r: a + t * 0.2, w: 0.3 + (i % 4) * 0.12};
  });
  return (
    <ThreeCanvas width={W} height={H} shadows camera={{position: [Math.sin(camA) * 12.5, 1.5, Math.cos(camA) * 12.5], fov: 34}} style={{position: 'absolute', inset: 0}} gl={{antialias: true, preserveDrawingBuffer: true}}>
      <color attach="background" args={[C.night1]} />
      <ambientLight intensity={0.75} />
      <hemisphereLight args={['#fff7e8', '#8fa6a3', 0.55]} />
      <directionalLight castShadow position={[5, 9, 7]} intensity={1.3} />
      <pointLight position={[0, 0, 2.2]} intensity={heat * 5} color="#ff8a3a" distance={7} />
      <group position={[0, 0.3, 0]}>
        <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -ROUT * sc, 0]}><planeGeometry args={[60, 40]} /><meshStandardMaterial color="#0f3540" roughness={1} /></mesh>
        <gridHelper args={[60, 40, '#2fb8a0', '#1d5a63']} position={[0, -ROUT * sc + 0.01, 0]} />
        {ganda ? (
          <>
            <BanSatu f={f} s={s} p={p} heat={heat} x={-1.35} sc={sc} beban={0} pecah={pecah} />
            <BanSatu f={f} s={s} p={s.p2 ?? 1} heat={Math.min(heat, 0.2)} x={1.35} sc={sc} beban={0} pecah={-1} />
          </>
        ) : (
          <BanSatu f={f} s={s} p={p} heat={heat} x={0} sc={sc} beban={beban} pecah={pecah} />
        )}
        {/* beban di atas ban */}
        {beban > 0 && !ganda && pecah < 0 && (
          <group position={[0, topY + 0.65, 0]}>
            <mesh castShadow><boxGeometry args={[3.2, 1.1, 2.0]} /><meshStandardMaterial color={C.cream} roughness={0.85} /></mesh>
            <mesh position={[0, 0, 1.005]}><boxGeometry args={[3.0, 0.1, 0.01]} /><meshStandardMaterial color={C.orange} /></mesh>
            {[-1, 0, 1].map((i) => <mesh key={i} position={[i * 0.9, 1.0 + 0.15 * Math.sin(f / 5 + i), 0]} rotation={[Math.PI, 0, 0]}>
              <coneGeometry args={[0.28, 0.7 * Math.min(1.6, beban), 4]} /><meshStandardMaterial color={C.orange} emissive={C.orange} emissiveIntensity={0.3} /></mesh>)}
          </group>
        )}
        {/* serpihan & kilat saat pecah */}
        {pecah >= 0 && pecah < 45 && frag.map((q, i) => (
          <mesh key={i} position={[q.x, q.y, q.z]} rotation={[q.r, q.r, q.r]}><boxGeometry args={[q.w, 0.14, 0.3]} /><meshStandardMaterial color="#2a343a" /></mesh>
        ))}
        {pecah >= 0 && pecah < 10 && (
          <mesh><sphereGeometry args={[1 + pecah * 0.5, 24, 24]} /><meshStandardMaterial color="#ffffff" emissive="#ffd9a0" emissiveIntensity={1} transparent opacity={(1 - pecah / 10) * 0.55} /></mesh>
        )}
        {/* uap panas */}
        {heat > 0.5 && pecah < 0 && Array.from({length: 7}).map((_, i) => {
          const a = ((f / 40 + i / 7) % 1);
          return <mesh key={'u' + i} position={[-1.2 + i * 0.4, 2.0 + a * 2.2, 0.8]}><sphereGeometry args={[0.12 + a * 0.25, 12, 12]} /><meshStandardMaterial color="#ffffff" transparent opacity={(1 - a) * 0.4 * (heat - 0.45) * 2} /></mesh>;
        })}
      </group>
    </ThreeCanvas>
  );
};

/* ============================ lapisan 2D (gaya khas Ghostrip) ============================ */
// Kata kunci *bintang* = mint + garis bawah oranye (tanpa huruf miring)
const Rich: React.FC<{t: string; style?: React.CSSProperties}> = ({t, style}) => (
  <span style={style}>{t.split(/(\*[^*]+\*)/g).filter(Boolean).map((p, i) => p.startsWith('*')
    ? <span key={i} style={{color: C.mint, boxShadow: `inset 0 -10px 0 ${C.orange}55`}}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}</span>
);

/* Logo melayang di tengah atas (hantu tanpa kotak + Ghostrip.id) */
const LogoFloat: React.FC = () => {
  const f = useCurrentFrame();
  const bob = Math.sin(f / 18) * 6;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 150, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 14, transform: `translateY(${bob}px)`}}>
      <Img src={staticFile('logo_float.png')} style={{width: 92, height: 92, filter: 'drop-shadow(0 8px 14px rgba(0,0,0,.45))'}} />
      <span style={{fontFamily: F, fontWeight: 700, fontSize: 40, color: '#fff', textShadow: '0 3px 12px rgba(0,0,0,.5)'}}>Ghostrip.id</span>
    </div>
  );
};

/* Judul bab: nomor bulat oranye + topik kecil mint, judul putih di tengah */
const Bab: React.FC<{no: number; kicker?: string; judul?: string}> = ({no, kicker, judul}) => {
  const f = useCurrentFrame();
  const a = spring({frame: f, fps: FPS, config: {damping: 16, stiffness: 180}});
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 272, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', opacity: a, transform: `scale(${0.96 + 0.04 * a})`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
        <span style={{width: 44, height: 44, borderRadius: '50%', background: C.orange, color: C.ink, fontFamily: F, fontWeight: 900, fontSize: 24, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{String(no).padStart(2, '0')}</span>
        {kicker && <span style={{fontFamily: F, fontWeight: 700, fontSize: 26, letterSpacing: 5, color: C.mint, textTransform: 'uppercase'}}>{kicker}</span>}
      </div>
      {judul && <div style={{fontFamily: F, fontWeight: 800, fontSize: 64, lineHeight: 1.1, color: '#fff', marginTop: 14, letterSpacing: -0.5, textShadow: '0 4px 18px rgba(0,0,0,.45)'}}><Rich t={judul} /></div>}
    </div>
  );
};

const Tag: React.FC<{t: string}> = ({t}) => (
  <div style={{position: 'absolute', right: 56, top: 1560, fontFamily: F, fontWeight: 600, fontSize: 22, letterSpacing: 3, color: 'rgba(233,245,243,.55)', textTransform: 'uppercase'}}>{t}</div>
);

/* Subtitle tanpa kotak: kata muncul satu per satu, kata yang diucapkan mint */
const Sub: React.FC<{c: BedahChunk}> = ({c}) => {
  const f = useCurrentFrame();
  const words = c.text.replace(/\*/g, '').split(/\s+/).filter(Boolean);
  const span = Math.max(1, c.to - c.from);
  const wts = words.map((w) => Math.max(2, w.length)); const tot = wts.reduce((x, y) => x + y, 0);
  const starts: number[] = []; let acc = 0;
  for (let i = 0; i < words.length; i++) { starts.push((acc / tot) * span * 0.9); acc += wts[i]; }
  let cur = 0; for (let i = 0; i < words.length; i++) if (f >= starts[i]) cur = i;
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 1270, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 16px'}}>
      {words.map((w, i) => {
        const k = spring({frame: f - starts[i], fps: FPS, config: {damping: 12, stiffness: 260}});
        const shown = f >= starts[i];
        return (
          <span key={i} style={{fontFamily: F, fontWeight: 900, fontSize: 66, lineHeight: 1.18, color: i === cur ? C.mint : shown ? '#fff' : 'rgba(255,255,255,.32)',
            transform: `translateY(${shown ? (1 - k) * 10 : 0}px) scale(${i === cur ? 1.06 : 1})`, display: 'inline-block',
            textShadow: `0 4px 0 ${C.night0}, 0 0 18px rgba(0,0,0,.8), 2px 2px 0 ${C.night0}, -2px -2px 0 ${C.night0}`}}>{w}</span>
        );
      })}
    </div>
  );
};

/* Label: chip navy berbingkai mint dengan titik penanda */
const Label: React.FC<{l: {t: string; x: number; y: number; warna?: string; dari?: number}}> = ({l}) => {
  const f = useCurrentFrame() - (l.dari ?? 6);
  const a = spring({frame: f, fps: FPS, config: {damping: 13, stiffness: 200}});
  const ac = l.warna === 'merah' ? C.red : l.warna === 'oranye' ? C.orange : C.mint;
  return (
    <div style={{position: 'absolute', left: l.x, top: l.y, transform: `translate(-50%,-50%) scale(${a})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div style={{background: 'rgba(7,26,34,.9)', border: `3px solid ${ac}`, color: '#fff', fontFamily: F, fontWeight: 800, fontSize: 28, letterSpacing: 2, padding: '8px 18px', borderRadius: 12, whiteSpace: 'nowrap', textTransform: 'uppercase', boxShadow: '0 8px 20px rgba(0,0,0,.35)'}}>{l.t}</div>
      <div style={{width: 3, height: 26, background: ac}} /><div style={{width: 14, height: 14, borderRadius: '50%', background: ac, boxShadow: `0 0 12px ${ac}`}} />
    </div>
  );
};

/* Kartu sumber: navy, tanda kutip mint, sumber mint */
const Kutipan: React.FC<{k: NonNullable<BedahScene['kutipan']>}> = ({k}) => {
  const f = useCurrentFrame() - (k.dari ?? 4);
  const a = interpolate(f, [0, 10], [0, 1], {...cl, easing: eo});
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: 520, opacity: a, transform: `translateY(${(1 - a) * 24}px)`, background: 'rgba(7,26,34,.94)', borderRadius: 26,
      border: `2px solid ${C.mint}55`, padding: '26px 30px 24px', boxShadow: '0 18px 40px rgba(0,0,0,.45)', textAlign: 'center'}}>
      {k.kutip !== false && <div style={{fontFamily: F, fontWeight: 900, fontSize: 80, lineHeight: 0.6, color: C.mint, height: 34}}>“</div>}
      <div style={{fontFamily: F, fontWeight: 700, fontSize: 36, lineHeight: 1.28, color: '#fff'}}>{k.teks}</div>
      <div style={{fontFamily: F, fontWeight: 600, fontSize: 22, color: C.mint, marginTop: 14, letterSpacing: 1}}>— {k.sumber}{k.tgl ? ` · ${k.tgl}` : ''}</div>
    </div>
  );
};

/* Kata besar gaya STEMPEL (seperti cap di surat penawaran) */
const Boom: React.FC<{t: string}> = ({t}) => {
  const f = useCurrentFrame();
  const a = spring({frame: f, fps: FPS, config: {damping: 10, stiffness: 300}});
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 760, display: 'flex', justifyContent: 'center', transform: `rotate(-9deg) scale(${1.6 - 0.6 * a})`, opacity: Math.min(1, a * 1.3)}}>
      <div style={{border: `12px solid ${C.orange}`, borderRadius: 26, padding: '6px 34px', background: 'rgba(7,26,34,.55)', boxShadow: `0 0 0 4px ${C.night0}, 0 20px 40px rgba(0,0,0,.45)`}}>
        <span style={{fontFamily: F, fontWeight: 900, fontSize: 150, color: C.orange, letterSpacing: 4, textShadow: `0 4px 0 ${C.night0}`}}>{t}</span>
      </div>
    </div>
  );
};

/* Gauge tekanan angin (2D, di atas adegan angin) */
const Gauge: React.FC<{s: BedahScene}> = ({s}) => {
  const f = useCurrentFrame();
  const v = interpolate(f, [0, s.dur * 0.9], [s.bar0 ?? 8, s.bar1 ?? 6.4], cl);
  const ang = interpolate(v, [0, 10], [-130, 130]);
  const low = v < 7;
  return (
    <div style={{position: 'absolute', left: 690, top: 800, width: 300, height: 340}}>
      <svg width={300} height={340} viewBox="-170 -170 340 385">
        <circle r={160} fill="#fffdf8" stroke={C.ink} strokeWidth={10} />
        {/* zona merah < 7 bar */}
        <path d={arc(-130, interpolate(7, [0, 10], [-130, 130]), 128)} stroke={C.red} strokeWidth={22} fill="none" />
        <path d={arc(interpolate(7, [0, 10], [-130, 130]), 130, 128)} stroke={C.mintDeep} strokeWidth={22} fill="none" />
        {Array.from({length: 11}).map((_, i) => { const a = (-130 + i * 26) * Math.PI / 180; return <text key={i} x={Math.sin(a) * 96} y={-Math.cos(a) * 96 + 9} textAnchor="middle" fontFamily="Outfit" fontWeight={700} fontSize={24} fill={C.ink}>{i}</text>; })}
        <g transform={`rotate(${ang})`}><rect x={-5} y={-120} width={10} height={130} rx={5} fill={low ? C.red : C.ink} /></g>
        <circle r={16} fill={C.ink} />
        <rect x={-92} y={176} width={184} height={50} rx={25} fill={low ? C.red : C.mint} /><text y={213} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={36} fill={low ? "#fff" : C.ink}>{v.toFixed(1)} bar</text>
      </svg>
    </div>
  );
};
function arc(a0: number, a1: number, r: number) {
  const p = (a: number) => [Math.sin(a * Math.PI / 180) * r, -Math.cos(a * Math.PI / 180) * r];
  const [x0, y0] = p(a0), [x1, y1] = p(a1);
  return `M ${x0} ${y0} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}`;
}

/* Pola gigi transmisi (2D) — gigi rendah menyala */
const Gigi: React.FC<{aktif: number[]}> = ({aktif}) => {
  const f = useCurrentFrame();
  const a = spring({frame: f - 6, fps: FPS, config: {damping: 14}});
  const pos: Record<number, [number, number]> = {1: [-90, -80], 2: [-90, 80], 3: [0, -80], 4: [0, 80], 5: [90, -80], 6: [90, 80]};
  return (
    <div style={{position: 'absolute', left: 660, top: 600, transform: `scale(${a})`, transformOrigin: 'top left'}}>
      <svg width={320} height={320} viewBox="-160 -160 320 320">
        <rect x={-150} y={-150} width={300} height={300} rx={36} fill="#fffdf8" stroke={C.ink} strokeWidth={8} />
        <path d="M -90 -80 V 80 M 0 -80 V 80 M 90 -80 V 80 M -90 0 H 90" stroke="#9aa7ab" strokeWidth={10} strokeLinecap="round" />
        {Object.entries(pos).map(([g, [x, y]]) => {
          const on = aktif.includes(+g);
          return <g key={g}><circle cx={x} cy={y} r={34} fill={on ? C.mint : '#e9e3d4'} stroke={C.ink} strokeWidth={5} /><text x={x} y={y + 13} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={36} fill={C.ink}>{g}</text></g>;
        })}
      </svg>
    </div>
  );
};

/* end card logo */
const LogoEnd: React.FC = () => {
  const f = useCurrentFrame();
  const a = spring({frame: f, fps: FPS, config: {damping: 12}});
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, ${C.teal} 0%, ${C.night1} 55%, ${C.night0} 100%)`, alignItems: 'center', justifyContent: 'center'}}>
      <Img src={staticFile('icon.png')} style={{width: 300, height: 300, borderRadius: 72, transform: `scale(${a})`, boxShadow: `0 0 80px ${C.mint}55`}} />
      <div style={{fontFamily: F, fontWeight: 800, fontSize: 72, color: '#fff', marginTop: 40, opacity: a}}>Ghostrip<span style={{color: C.mint}}>.id</span></div>
    </AbsoluteFill>
  );
};

/* ============================ komposisi ============================ */
const Scene3D: React.FC<{s: BedahScene}> = ({s}) => {
  const f = useCurrentFrame();
  if (s.type === 'rem') return <AdeganRem f={f} s={s} />;
  if (s.type === 'angin') return <AdeganAngin f={f} s={s} />;
  if (s.type === 'ban') return <AdeganBan f={f} s={s} />;
  return <AdeganJalan f={f} s={s} />;
};

export const Bedah: React.FC<BedahProps> = (p) => {
  useOutfit();
  const babNo: number[] = []; let nb = 0; let prev = '';
  p.scenes.forEach((s) => { if (s.kicker && s.kicker !== prev) { nb++; prev = s.kicker; } babNo.push(Math.max(1, nb)); });
  return (
    <AbsoluteFill style={{background: C.night1}}>
      {p.scenes.map((s, i) => (
        <Sequence key={i} from={s.from} durationInFrames={s.dur}>
          {s.type === 'logo' ? <LogoEnd /> : (
            <>
              <Scene3D s={s} />
              <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 560, background: 'linear-gradient(180deg, rgba(4,13,19,.85) 0%, rgba(4,13,19,.55) 60%, rgba(4,13,19,0) 100%)'}} />
              <LogoFloat />
              <Bab no={babNo[i]} kicker={s.kicker} judul={s.judul} />
              {s.ilustrasi !== '' && <Tag t={s.ilustrasi ?? 'Ilustrasi'} />}
              {s.type === 'angin' && <Gauge s={s} />}
              {s.gigi && <Gigi aktif={s.gigi} />}
              {(s.label ?? []).map((l, j) => <Label key={j} l={l} />)}
              {s.kutipan && <Kutipan k={s.kutipan} />}
              {s.boom && <Sequence from={s.boomDari ?? 8} durationInFrames={Math.max(1, s.dur - (s.boomDari ?? 8))}><Boom t={s.boom} /></Sequence>}
              {s.chunks.map((c, j) => (
                <Sequence key={j} from={c.from} durationInFrames={Math.max(1, c.to - c.from)}><Sub c={{...c, from: 0, to: c.to - c.from}} /></Sequence>
              ))}
            </>
          )}
          {p.whoosh && i > 0 && <Audio src={staticFile(p.whoosh)} volume={0.25} />}
        </Sequence>
      ))}
      {p.narasi && <Sequence from={6}><Audio src={staticFile(p.narasi)} /></Sequence>}
      {p.musik && <Audio src={staticFile(p.musik)} volume={p.narasi ? 0.16 : 0.5} />}
    </AbsoluteFill>
  );
};
