// Reels PRODUK (B) naskah 13-30 Nov 2026: gaya Iklan3D, data-driven. Layar app dari aplikasi asli (data simulasi).
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {C} from './theme';
import {Stage, Phone, Head, Tag, Chip, Simulasi, Trans, S1Logo, S8CTA, S4WA, F, cl, sp, useOutfit} from './Iklan3D';

export type ProdukChip = {text: string; sub?: string; icon?: string; x: number; y: number; warna?: 'orange'};
export type ProdukScene = {key: string; from: number; dur: number; narasi?: string; chunks?: {text: string; from: number; to: number}[];
  head?: string; headSize?: number; tag?: string; n?: string; shot?: string; shot2?: string; chips?: ProdukChip[]; simulasi?: boolean; ry?: number};
export type ProdukProps = {scenes: ProdukScene[]; durationInFrames: number; narasi?: string | null; musik?: string; whoosh?: string};

const SubC: React.FC<{chunks: {text: string; from: number; to: number}[]}> = ({chunks}) => {
  const f = useCurrentFrame();
  const c = chunks.find((x) => f >= x.from && f < x.to);
  if (!c) return null;
  const o = interpolate(f, [c.from, c.from + 4], [0, 1], cl);
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: 1590, textAlign: 'center', opacity: o}}>
      <span style={{fontFamily: F, fontWeight: 700, fontSize: 44, lineHeight: 1.3, color: '#eafaf6', background: 'rgba(4,13,19,0.7)', padding: '8px 20px', borderRadius: 14, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'}}>{c.text.split('*').map((t, i) => (i % 2 ? <span key={i} style={{color: C.mint}}>{t}</span> : t))}</span>
    </div>
  );
};

const Layar: React.FC<{s: ProdukScene}> = ({s}) => {
  const f = useCurrentFrame();
  const a = sp(f, 16, 90);
  const hook = s.key === 'hook';
  const ry = (s.ry ?? -16) + (1 - a) * -34 + f * 0.1;
  return (
    <>
      {s.tag && <Tag n={s.n ?? '01'} label={s.tag} />}
      {s.head && <Head text={s.head} top={hook ? 250 : 210} size={s.headSize ?? (hook ? 104 : 92)} />}
      {s.shot && <Phone src={s.shot} x={540 + (1 - a) * 420} y={hook ? 1130 : 1060} w={hook ? 520 : 540} ry={ry} rx={6} />}
      {s.shot2 && <Phone src={s.shot2} x={300} y={1100} w={400} ry={26 - f * 0.08} rx={4} o={sp(f - 14, 16, 90)} />}
      {(s.chips ?? []).map((c, i) => <Chip key={i} x={c.x} y={c.y} text={c.text} sub={c.sub} icon={c.icon} delay={10 + i * 7} color={c.warna === 'orange' ? C.orange : C.mint} />)}
      {s.simulasi !== false && <Simulasi />}
    </>
  );
};

export const Produk: React.FC<ProdukProps> = ({scenes, narasi, musik, whoosh}) => {
  useOutfit();
  return (
    <AbsoluteFill style={{background: C.night0}}>
      <Stage />
      {scenes.map((s, i) => (
        <Sequence key={i} from={s.from} durationInFrames={s.dur}>
          <Trans dur={s.dur} last={i === scenes.length - 1}>
            {s.key === 'cta' ? <S8CTA dur={s.dur} /> : s.key === 'logo' ? <S1Logo dur={s.dur} /> : s.key === 'wa' ? <S4WA dur={s.dur} /> : <Layar s={s} />}
          </Trans>
          {s.chunks && s.chunks.length > 0 && <SubC chunks={s.chunks} />}
          {whoosh && i > 0 && <Audio src={staticFile(whoosh)} volume={0.25} />}
        </Sequence>
      ))}
      {narasi && <Sequence from={6}><Audio src={staticFile(narasi)} /></Sequence>}
      {musik && <Audio src={staticFile(musik)} volume={narasi ? 0.16 : 0.5} />}
      <div style={{position: 'absolute', left: 50, top: 62, display: 'flex', alignItems: 'center', gap: 12, fontFamily: F, fontWeight: 700, fontSize: 28, color: '#cfe8e3'}}>
        <Img src={staticFile('icon.png')} style={{width: 48, height: 48, borderRadius: 12}} />Ghostrip
      </div>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.5) 100%)', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
