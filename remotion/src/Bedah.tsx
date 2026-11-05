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
      <color attach="background" args={[C.cream]} />
      <ambientLight intensity={0.75} />
      <hemisphereLight args={['#fff7e8', '#9fb3b0', 0.55]} />
      <directionalLight castShadow position={[8, 18, 6]} intensity={1.35} shadow-mapSize-width={1024} shadow-mapSize-height={1024}
        shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} />
      <group rotation={[0, 0, slope]} position={[0, shake, 0]}>
        <mesh receiveShadow position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[400, 400]} /><meshStandardMaterial color="#e6dcc6" roughness={1} /></mesh>
        <mesh receiveShadow position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[400, 4.2]} /><meshStandardMaterial color="#2c3c42" roughness={0.95} /></mesh>
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
      <color attach="background" args={[C.cream]} />
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
      <color attach="background" args={[C.cream]} />
      <ambientLight intensity={0.75} />
      <hemisphereLight args={['#fff7e8', '#8fa6a3', 0.5]} />
      <directionalLight castShadow position={[4, 10, 6]} intensity={1.25} />
      <group position={[-0.2, 0.6, 0]} rotation={[0, -0.25, 0]} scale={0.72}>
        {/* tabung */}
        <group rotation={[0, 0, Math.PI / 2]}>
          <mesh castShadow><cylinderGeometry args={[0.9, 0.9, 3.2, 40]} /><meshStandardMaterial color={C.tealSoft} roughness={0.5} metalness={0.2} transparent opacity={0.55} /></mesh>
          <mesh position={[0, 1.6, 0]} castShadow><sphereGeometry args={[0.9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color={C.tealSoft} roughness={0.5} transparent opacity={0.55} /></mesh>
          <mesh position={[0, -1.6, 0]} rotation={[Math.PI, 0, 0]} castShadow><sphereGeometry args={[0.9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color={C.tealSoft} roughness={0.5} transparent opacity={0.55} /></mesh>
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
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -3, 0]}><planeGeometry args={[40, 40]} /><meshStandardMaterial color="#e6dcc6" /></mesh>
      {pulses > 0 && null}
    </ThreeCanvas>
  );
};

/* ============================ lapisan 2D ============================ */
const Rich: React.FC<{t: string; style?: React.CSSProperties; hl?: string}> = ({t, style, hl = C.tealSoft}) => (
  <span style={style}>{t.split(/(\*[^*]+\*)/g).filter(Boolean).map((p, i) => p.startsWith('*')
    ? <i key={i} style={{fontStyle: 'italic', color: hl}}>{p.slice(1, -1)}</i> : <span key={i}>{p}</span>)}</span>
);

const Header: React.FC<{kicker?: string; judul?: string}> = ({kicker, judul}) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [0, 8], [0, 1], {...cl, easing: eo});
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 470, background: `linear-gradient(180deg, ${C.cream} 0%, ${C.cream} 62%, rgba(242,234,217,0) 100%)`}}>
      <div style={{position: 'absolute', left: 64, top: 205, right: 64, opacity: a, transform: `translateY(${(1 - a) * 10}px)`}}>
        {kicker && <div style={{fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: '#6d7a7e', textTransform: 'uppercase'}}>{kicker}</div>}
        {judul && <div style={{fontFamily: F, fontWeight: 800, fontSize: 62, lineHeight: 1.08, color: C.ink, marginTop: 10, letterSpacing: -1}}><Rich t={judul} /></div>}
      </div>
    </div>
  );
};

const LogoChip: React.FC = () => (
  <div style={{position: 'absolute', right: 52, top: 392, display: 'flex', alignItems: 'center', gap: 10, background: C.night1, borderRadius: 999, padding: '7px 18px 7px 8px', boxShadow: '0 6px 18px rgba(0,0,0,.18)'}}>
    <Img src={staticFile('icon.png')} style={{width: 40, height: 40, borderRadius: 12}} />
    <span style={{fontFamily: F, fontWeight: 700, fontSize: 26, color: '#fff'}}>Ghostrip<span style={{color: C.mint}}>.id</span></span>
  </div>
);

const Tag: React.FC<{t: string}> = ({t}) => (
  <div style={{position: 'absolute', left: '50%', top: 486, transform: 'translateX(-50%)', fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: '#f2ead9', background: 'rgba(13,27,36,.78)', padding: '6px 14px', borderRadius: 6}}>{t}</div>
);

/* subtitle per frasa, kata yang sedang diucapkan menyala mint */
const Sub: React.FC<{c: BedahChunk}> = ({c}) => {
  const f = useCurrentFrame();
  const words = c.text.replace(/\*/g, '').split(/\s+/).filter(Boolean);
  const span = Math.max(1, c.to - c.from);
  const wts = words.map((w) => Math.max(2, w.length)); const tot = wts.reduce((a, b) => a + b, 0);
  let acc = 0; let cur = words.length - 1;
  for (let i = 0; i < words.length; i++) { acc += wts[i]; if (f < (acc / tot) * span * 0.92) { cur = i; break; } }
  const pop = spring({frame: f, fps: FPS, config: {damping: 15, stiffness: 240}});
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1240, display: 'flex', justifyContent: 'center', transform: `scale(${0.94 + 0.06 * pop})`}}>
      <div style={{background: 'rgba(7,26,34,.92)', borderRadius: 18, padding: '14px 22px', maxWidth: 900, textAlign: 'center', lineHeight: 1.32, boxShadow: '0 10px 30px rgba(0,0,0,.25)'}}>
        {words.map((w, i) => (
          <span key={i} style={{fontFamily: F, fontWeight: 700, fontSize: 54, color: i === cur ? C.ink : '#fff', background: i === cur ? C.mint : 'transparent', borderRadius: 10, padding: '0 8px', margin: '0 1px'}}>{w}</span>
        ))}
      </div>
    </div>
  );
};

const Label: React.FC<{l: {t: string; x: number; y: number; warna?: string; dari?: number}}> = ({l}) => {
  const f = useCurrentFrame() - (l.dari ?? 6);
  const a = spring({frame: f, fps: FPS, config: {damping: 13, stiffness: 200}});
  const bg = l.warna === 'merah' ? C.red : l.warna === 'mint' ? C.mint : C.orange;
  return (
    <div style={{position: 'absolute', left: l.x, top: l.y, transform: `translate(-50%,-50%) scale(${a})`, background: bg, color: l.warna === 'merah' ? '#fff' : C.ink,
      fontFamily: F, fontWeight: 800, fontSize: 28, letterSpacing: 1.5, padding: '8px 18px', borderRadius: 999, boxShadow: '0 8px 20px rgba(0,0,0,.25)', whiteSpace: 'nowrap', textTransform: 'uppercase'}}>{l.t}</div>
  );
};

const Kutipan: React.FC<{k: NonNullable<BedahScene['kutipan']>}> = ({k}) => {
  const f = useCurrentFrame() - (k.dari ?? 4);
  const a = interpolate(f, [0, 10], [0, 1], {...cl, easing: eo});
  return (
    <div style={{position: 'absolute', left: 64, right: 200, top: 560, opacity: a, transform: `translateY(${(1 - a) * 24}px)`, background: '#fffdf8', borderRadius: 18,
      borderLeft: `8px solid ${C.mintDeep}`, padding: '22px 26px', boxShadow: '0 14px 34px rgba(13,27,36,.22)'}}>
      <div style={{fontFamily: F, fontWeight: 700, fontSize: 36, lineHeight: 1.25, color: C.ink}}>{k.kutip === false ? k.teks : `“${k.teks}”`}</div>
      <div style={{fontFamily: MONO, fontSize: 20, color: '#6d7a7e', marginTop: 14, letterSpacing: 1}}>{k.sumber}{k.tgl ? <><br />{k.tgl}</> : null}</div>
    </div>
  );
};

const Boom: React.FC<{t: string}> = ({t}) => {
  const f = useCurrentFrame();
  const a = spring({frame: f, fps: FPS, config: {damping: 9, stiffness: 260}});
  const shadow = Array.from({length: 9}).map((_, i) => `${i + 1}px ${i + 1}px 0 ${C.orangeDeep}`).join(',') + ', 0 18px 30px rgba(0,0,0,.35)';
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', transform: `rotate(-7deg) scale(${0.4 + 0.6 * a})`, opacity: Math.min(1, a * 1.4)}}>
      <span style={{fontFamily: F, fontWeight: 900, fontSize: 170, color: C.orange, WebkitTextStroke: `4px ${C.ink}`, textShadow: shadow, letterSpacing: -2}}>{t}</span>
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
        <rect x={-92} y={176} width={184} height={50} rx={25} fill={low ? C.red : C.ink} /><text y={213} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={36} fill="#fff">{v.toFixed(1)} bar</text>
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
  return <AdeganJalan f={f} s={s} />;
};

export const Bedah: React.FC<BedahProps> = (p) => {
  useOutfit();
  return (
    <AbsoluteFill style={{background: C.cream}}>
      {p.scenes.map((s, i) => (
        <Sequence key={i} from={s.from} durationInFrames={s.dur}>
          {s.type === 'logo' ? <LogoEnd /> : (
            <>
              <Scene3D s={s} />
              <Header kicker={s.kicker} judul={s.judul} />
              <LogoChip />
              {s.ilustrasi !== '' && <Tag t={s.ilustrasi ?? 'ILUSTRASI'} />}
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
