import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame, Easing} from 'remotion';
import {C, W, H} from './theme';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const easeOut = Easing.bezier(0.16, 1, 0.3, 1);

// Kamera: dorong pelan (push-in) sepanjang adegan, seperti gaya referensi
export const Camera: React.FC<{dur: number; from?: number; to?: number; ox?: string; oy?: string; pan?: number; children: React.ReactNode}> = ({dur, from = 1, to = 1.07, ox = '50%', oy = '55%', pan = 0, children}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, dur], [from, to], clamp);
  const x = interpolate(f, [0, dur], [0, pan], clamp);
  return <AbsoluteFill style={{transform: `translateX(${x}px) scale(${s})`, transformOrigin: `${ox} ${oy}`}}>{children}</AbsoluteFill>;
};

// Langit malam dengan cahaya cakrawala oranye (warna brand)
export const NightSky: React.FC<{horizon?: number; warm?: number; stars?: boolean}> = ({horizon = 1150, warm = 1, stars = true}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${C.night0} 0%, ${C.night1} 30%, ${C.night2} ${(horizon / H) * 100 - 14}%, #1a3b44 ${(horizon / H) * 100 - 4}%, #5b4a45 ${(horizon / H) * 100}%, ${C.asphalt} ${(horizon / H) * 100 + 0.2}%)`}} />
      <div style={{position: 'absolute', left: -200, right: -200, top: horizon - 260, height: 320, background: `radial-gradient(60% 100% at 50% 100%, rgba(255,157,92,${0.55 * warm}) 0%, rgba(255,157,92,${0.18 * warm}) 45%, transparent 75%)`}} />
      {stars && Array.from({length: 40}).map((_, i) => {
        const x = random(`sx${i}`) * W, y = random(`sy${i}`) * (horizon - 420);
        const tw = 0.25 + 0.35 * (0.5 + 0.5 * Math.sin(f / 12 + i * 1.7));
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 3, height: 3, borderRadius: 2, background: '#d9f7f1', opacity: tw}} />;
      })}
    </AbsoluteFill>
  );
};

// Lampu jalan dengan cahaya bulat lembut
export const Lamp: React.FC<{x: number; y: number; h?: number; flip?: boolean; s?: number}> = ({x, y, h = 520, flip = false, s = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `scale(${s}) scaleX(${flip ? -1 : 1})`, transformOrigin: 'left bottom'}}>
    <div style={{position: 'absolute', left: -170, top: -150, width: 360, height: 360, borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,214,150,0.55) 0%, rgba(255,178,122,0.18) 35%, transparent 70%)'}} />
    <div style={{position: 'absolute', left: -4, top: 0, width: 10, height: h, background: '#0e222a'}} />
    <div style={{position: 'absolute', left: -60, top: -4, width: 70, height: 12, borderRadius: 6, background: '#0e222a'}} />
    <div style={{position: 'absolute', left: -64, top: 4, width: 30, height: 10, borderRadius: 5, background: '#ffe2b3', boxShadow: '0 0 30px 10px rgba(255,214,150,0.7)'}} />
  </div>
);

// Bokeh lampu kabur untuk latar kartu
export const Bokeh: React.FC<{tint?: string; n?: number}> = ({tint = 'rgba(255,170,100,', n = 14}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 80% at 50% 70%, #1a2a30 0%, ${C.night0} 75%)`}}>
      {Array.from({length: n}).map((_, i) => {
        const x = random(`bx${i}`) * W, y = 1200 + random(`by${i}`) * 700;
        const r = 50 + random(`br${i}`) * 120;
        const a = 0.12 + random(`ba${i}`) * 0.22;
        return <div key={i} style={{position: 'absolute', left: x - r + Math.sin(f / 40 + i) * 10, top: y - r, width: r * 2, height: r * 2, borderRadius: '50%', background: `radial-gradient(circle, ${tint}${a}) 0%, ${tint}0) 70%)`}} />;
      })}
    </AbsoluteFill>
  );
};

// Butiran film + vinyet supaya terasa sinematik
export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const seed = f % 4;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={W} height={H} style={{position: 'absolute', opacity: 0.07, mixBlendMode: 'overlay'}}>
        <filter id={`n${seed}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} /></filter>
        <rect width={W} height={H} filter={`url(#n${seed})`} />
      </svg>
      <AbsoluteFill style={{background: 'radial-gradient(120% 90% at 50% 45%, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

// Truk box Ghostrip tampak samping (kabin oranye, bak krem bergaris mint)
export const Truck: React.FC<{x: number; y: number; s?: number; speed?: number; lights?: boolean; label?: string; flip?: boolean}> = ({x, y, s = 1, speed = 0, lights = true, label = '', flip = false}) => {
  const f = useCurrentFrame();
  const rot = f * 9 * speed;
  const bob = Math.sin(f / 2.6) * 2.2 * Math.min(1, speed) + Math.sin(f / 13) * 0.8;
  const Wheel = ({cx}: {cx: number}) => (
    <g transform={`translate(${cx} 312) rotate(${rot})`}>
      <circle r={44} fill="#0a1419" />
      <circle r={26} fill="#5b6f76" />
      <circle r={9} fill="#2a3a40" />
      {[0, 60, 120].map((a) => <rect key={a} x={-3} y={-24} width={6} height={48} fill="#3d5158" transform={`rotate(${a})`} />)}
    </g>
  );
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${s}) scaleX(${flip ? -1 : 1})`, transformOrigin: 'left top'}}>
      <svg width={900} height={380} style={{overflow: 'visible'}}>
        <defs>
          <linearGradient id="beam" x1="0" x2="1">
            <stop offset="0" stopColor="#fff1cf" stopOpacity={0.55} />
            <stop offset="1" stopColor="#fff1cf" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="box" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#eef1ee" />
            <stop offset="1" stopColor="#c9d2cf" />
          </linearGradient>
          <linearGradient id="cab" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={C.orange} />
            <stop offset="1" stopColor={C.orangeDeep} />
          </linearGradient>
        </defs>
        {lights && <polygon points="760,232 1250,150 1250,360 760,262" fill="url(#beam)" />}
        <ellipse cx={400} cy={356} rx={390} ry={20} fill="rgba(0,0,0,0.45)" />
        <g transform={`translate(0 ${bob})`}>
          <rect x={20} y={30} width={520} height={250} rx={10} fill="url(#box)" />
          <rect x={20} y={30} width={520} height={18} rx={8} fill="#ffffff" opacity={0.6} />
          <rect x={20} y={210} width={520} height={16} fill={C.mintDeep} />
          <rect x={20} y={230} width={520} height={6} fill={C.mint} />
          {label && <text x={280} y={160} textAnchor="middle" fontFamily="Outfit" fontWeight={800} fontSize={64} fill={C.ink} opacity={0.85}>{label}</text>}
          <path d="M556 110 h128 q42 0 64 44 l40 82 v52 h-232 z" fill="url(#cab)" />
          <path d="M582 132 h92 q24 0 36 26 l30 60 h-158 z" fill="#9fd8e0" opacity={0.85} />
          <path d="M582 132 h40 l-30 86 h-10 z" fill="#ffffff" opacity={0.25} />
          <rect x={556} y={262} width={236} height={22} rx={6} fill="#b85a26" />
          <rect x={776} y={226} width={18} height={14} rx={3} fill={lights ? '#fff6d8' : '#c9b48a'} />
          {lights && <circle cx={786} cy={233} r={22} fill="rgba(255,240,200,0.35)" />}
          <rect x={20} y={280} width={770} height={18} rx={6} fill="#132027" />
          <Wheel cx={170} />
          <Wheel cx={270} />
          <Wheel cx={680} />
        </g>
      </svg>
    </div>
  );
};

// Tokoh SOPIR (topi oranye) dan BOS (kumis), bergerak luwes: napas, kedip, kepala ikut badan
export const Person: React.FC<{who: 'sopir' | 'bos'; x: number; y: number; s?: number; pose?: 'cemas' | 'santai' | 'telepon' | 'pikir'; face?: 1 | -1}> = ({who, x, y, s = 1, pose = 'santai', face = 1}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const breathe = Math.sin(t * 2.1) * 4;
  const tilt = Math.sin(t * 1.2) * 2.5 + (pose === 'cemas' ? -5 : 0) + (pose === 'pikir' ? 6 : 0);
  const blink = (f + (who === 'bos' ? 40 : 0)) % 96 > 92 ? 0.1 : 1;
  const shirt = who === 'sopir' ? '#2f6f86' : '#3d4b5c';
  const shirtDark = who === 'sopir' ? '#24596c' : '#2f3a48';
  // lengan kanan: cemas = mengusap dahi, telepon = pegang HP di depan dada, pikir = dagu
  const wipe = Math.sin(t * 3.4) * 8;
  // sudut dihitung untuk bahu kiri (x=150): negatif = ke kanan/atas
  const arm = {
    cemas: {a1: 180 + wipe * 0.3, a2: -14 + wipe * 0.8},
    telepon: {a1: -25, a2: -85},
    pikir: {a1: -20, a2: -142},
    santai: {a1: 6 + Math.sin(t * 2) * 3, a2: -6},
  }[pose];
  const Arm: React.FC<{x: number; y: number; a1: number; a2: number; color: string}> = ({x: ax, y: ay, a1, a2, color}) => (
    <g transform={`translate(${ax} ${ay}) rotate(${a1})`}>
      <line x1={0} y1={0} x2={0} y2={96} stroke={color} strokeWidth={36} strokeLinecap="round" />
      <g transform={`translate(0 96) rotate(${a2})`}>
        <line x1={0} y1={0} x2={0} y2={74} stroke={color} strokeWidth={32} strokeLinecap="round" />
        <ellipse cx={0} cy={96} rx={19} ry={22} fill={C.skin} />
      </g>
    </g>
  );
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${s}) scaleX(${face})`, transformOrigin: 'center bottom', width: 440, height: 760}}>
      <svg width={440} height={760} style={{overflow: 'visible'}}>
        <defs><clipPath id={`head-${who}`}><circle cx={220} cy={232} r={96} /></clipPath></defs>
        <ellipse cx={220} cy={744} rx={140} ry={16} fill="rgba(0,0,0,0.4)" />
        <g transform={`translate(0 ${breathe * 0.4})`}>
          <Arm x={290} y={392} a1={-8 - Math.sin(t * 2.1) * 3} a2={-6} color={shirtDark} />
          <path d="M170 570 L166 712" stroke="#15222b" strokeWidth={52} strokeLinecap="round" />
          <path d="M270 570 L274 712" stroke="#15222b" strokeWidth={52} strokeLinecap="round" />
          <ellipse cx={156} cy={732} rx={44} ry={17} fill="#070e12" />
          <ellipse cx={284} cy={732} rx={44} ry={17} fill="#070e12" />
          <path d={`M146 610 C134 480 146 392 220 ${370 + breathe * 0.3} C294 392 306 480 294 610 Z`} fill={shirt} />
          <path d="M146 610 C140 520 150 450 176 410 L176 610 Z" fill="#000" opacity={0.12} />
          {who === 'sopir'
            ? <path d="M186 382 L220 420 L254 382" fill="none" stroke="#dcefee" strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" />
            : <><path d="M190 382 L220 450 L250 382 Z" fill="#eef2f4" /><path d="M215 396 h10 l7 64 l-12 16 l-12 -16 z" fill={C.orange} /></>}
          <rect x={144} y={598} width={152} height={18} rx={8} fill="#121c22" />
          <g transform={`rotate(${tilt} 220 350)`}>
            <path d="M202 300 h36 v70 h-36z" fill={C.skinShade} />
            <circle cx={220} cy={232} r={96} fill={C.skin} />
            <ellipse cx={124} cy={240} rx={13} ry={20} fill={C.skinShade} />
            {who === 'sopir' ? (
              <>
                <g clipPath={`url(#head-${who})`}>
                  <rect x={110} y={120} width={220} height={74} fill={C.orange} />
                  <rect x={110} y={186} width={220} height={10} fill={C.orangeDeep} />
                </g>
                <path d="M318 190 C350 192 372 202 378 212 C350 216 322 208 302 196 Z" fill={C.orangeDeep} />
              </>
            ) : (
              <path d="M124 212 C118 122 180 128 222 132 C276 128 322 136 316 212 C296 172 260 162 222 164 C182 162 142 172 124 212 Z" fill="#1f2a33" />
            )}
            {/* alis: naik saat cemas */}
            <path d={`M176 ${206 - (pose === 'cemas' ? 8 : 0)} q20 -10 38 0`} stroke="#1c2127" strokeWidth={8} strokeLinecap="round" fill="none" />
            <path d={`M240 ${206 - (pose === 'cemas' ? 8 : 0)} q20 -10 38 0`} stroke="#1c2127" strokeWidth={8} strokeLinecap="round" fill="none" />
            <ellipse cx={196} cy={242} rx={17} ry={19 * blink} fill="#fff" />
            <ellipse cx={258} cy={242} rx={17} ry={19 * blink} fill="#fff" />
            {blink > 0.5 && <><circle cx={203} cy={245} r={9.5} fill="#1c2127" /><circle cx={265} cy={245} r={9.5} fill="#1c2127" /><circle cx={200} cy={240} r={3} fill="#fff" /><circle cx={262} cy={240} r={3} fill="#fff" /></>}
            <path d="M236 256 q12 16 -2 24" stroke={C.skinShade} strokeWidth={6} fill="none" strokeLinecap="round" />
            {who === 'bos'
              ? <path d="M190 294 q30 -24 60 -6 q30 -18 60 6 q-30 14 -60 4 q-30 10 -60 -4z" fill="#1c2127" transform="translate(-14 0)" />
              : null}
            <path d={pose === 'cemas' ? 'M210 312 q18 -10 36 0' : 'M210 310 q18 10 36 0'} stroke="#7d2b2b" strokeWidth={6} fill="none" strokeLinecap="round" />
          </g>
          <Arm x={150} y={398} a1={arm.a1} a2={arm.a2} color={shirt} />
          {pose === 'telepon' && (
            <g transform="translate(286 446) rotate(-12)">
              <rect x={-42} y={-74} width={84} height={150} rx={14} fill="#0b1418" />
              <rect x={-36} y={-66} width={72} height={134} rx={10} fill={C.mint} opacity={0.9} />
              <circle cx={0} cy={0} r={90} fill="rgba(127,240,214,0.18)" />
            </g>
          )}
          {pose === 'cemas' && [0, 1].map((i) => (
            <path key={i} d={`M${120 + i * 210} ${170 + ((f / 2 + i * 9) % 30)} q6 10 0 16 q-6 -6 0 -16z`} fill="#bde8f2" opacity={0.8} />
          ))}
        </g>
      </svg>
    </div>
  );
};

// Kartu kertas (gaya "rule card" di referensi)
export const Paper: React.FC<{x: number; y: number; w: number; h: number; rot?: number; children: React.ReactNode; pop?: number}> = ({x, y, w, h, rot = 0, children, pop = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, transform: `rotate(${rot}deg) scale(${pop})`, background: `linear-gradient(180deg, ${C.cream}, ${C.creamShade})`, borderRadius: 10, boxShadow: '0 30px 60px rgba(0,0,0,0.55), 0 2px 0 rgba(255,255,255,0.4) inset', padding: 40, boxSizing: 'border-box', fontFamily: 'Outfit', color: C.ink}}>
    {children}
  </div>
);
